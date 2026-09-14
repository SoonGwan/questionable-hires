import asyncio
import ast
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ASSET = Path(__file__).resolve().parents[1] / 'skills/hostage-negotiator/assets/controlled_call.py'
spec = importlib.util.spec_from_file_location('controlled_call_asset', ASSET)
asset = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asset)


class ControlledCallTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.callback = asset.ControlledCall()
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(asyncio.gather(*self.tasks, return_exceptions=True), 1)

    def start(self, *args, **kwargs):
        task = asyncio.create_task(self.callback(*args, **kwargs))
        self.tasks.append(task)
        return task

    async def test_zero_argument_entry_and_result_identity(self):
        task = self.start()
        call = await self.callback.started()
        self.assertEqual((call.args, call.kwargs), ((), {}))
        self.assertFalse(task.done())
        value = object()
        call.complete(value)
        self.assertIs(await asyncio.wait_for(task, 1), value)
        self.assertEqual(self.callback.calls, [call])

    async def test_identical_arguments_have_distinct_reverse_completion(self):
        argument = object()
        first_task = self.start(argument, flag=argument)
        first = await self.callback.started()
        second_task = self.start(argument, flag=argument)
        second = await self.callback.started()
        self.assertIs(first.args[0], argument)
        self.assertIs(second.kwargs['flag'], argument)
        self.assertIsNot(first.response, second.response)
        second.complete('new')
        self.assertEqual(await asyncio.wait_for(second_task, 1), 'new')
        self.assertFalse(first_task.done())
        first.complete('old')
        self.assertEqual(await asyncio.wait_for(first_task, 1), 'old')
        self.assertEqual(len(self.callback.calls), 2)

    async def test_exception_identity_then_recovery(self):
        task = self.start()
        call = await self.callback.started()
        error = ValueError('failure')
        call.fail(error)
        with self.assertRaises(ValueError) as caught:
            await asyncio.wait_for(task, 1)
        self.assertIs(caught.exception, error)
        retry = self.start()
        recovered = await self.callback.started()
        recovered.complete()
        self.assertIsNone(await asyncio.wait_for(retry, 1))

    async def test_cancellation_isolated_and_late_completion_rejected(self):
        task = self.start()
        first = await self.callback.started()
        sibling = self.start()
        second = await self.callback.started()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, 1)
        self.assertTrue(first.response.cancelled())
        self.assertFalse(second.response.done())
        with self.assertRaises(asyncio.InvalidStateError):
            first.complete('late')
        second.complete('ok')
        self.assertEqual(await asyncio.wait_for(sibling, 1), 'ok')
        with self.assertRaises(asyncio.InvalidStateError):
            second.complete('twice')

    async def test_entry_timeout_does_not_consume_future_entry(self):
        for timeout in (0, -1, 31, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                await self.callback.started(timeout)
        with self.assertRaises(asyncio.TimeoutError):
            await self.callback.started(0.01)
        task = self.start()
        call = await self.callback.started()
        call.complete('after timeout')
        self.assertEqual(await asyncio.wait_for(task, 1), 'after timeout')


class StandaloneTests(unittest.TestCase):
    def test_documentation_move_preserves_frozen_executable_ast(self):
        frozen = ASSET.parents[3] / 'benchmarks/results/hostage-keyed-publish-01/keyed-publish--skill--1/project/tests/controlled_call.py'
        old, current = ast.parse(frozen.read_text()), ast.parse(ASSET.read_text())
        self.assertIsInstance(old.body[0], ast.Expr)
        self.assertIsInstance(current.body[0], ast.Expr)
        self.assertIsInstance(old.body[0].value.value, str)
        self.assertIsInstance(current.body[0].value.value, str)
        old.body.pop(0)
        current.body.pop(0)
        self.assertEqual(ast.dump(old), ast.dump(current))

    def test_copy_runs_without_skill_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copyfile(ASSET, root / 'controlled_call.py')
            code = '''import asyncio
from controlled_call import ControlledCall
async def main():
    callback = ControlledCall()
    task = asyncio.create_task(callback())
    try:
        call = await callback.started()
        call.complete(42)
        assert await asyncio.wait_for(task, 1) == 42
    finally:
        if not task.done(): task.cancel()
        await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
asyncio.run(main())
'''
            result = subprocess.run([sys.executable, '-E', '-B', '-c', code], cwd=root,
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual({p.name for p in root.iterdir()}, {'controlled_call.py'})


class ApplicationControls(unittest.IsolatedAsyncioTestCase):
    async def exercise(self, source):
        namespace = {}
        exec(compile(source, '<retained-form-control>', 'exec'), namespace)
        form = namespace['Form']()
        callback = asset.ControlledCall()
        tasks = []
        try:
            self.assertIs(form.pending, False)
            task = asyncio.create_task(form.submit(callback))
            tasks.append(task)
            call = await callback.started()
            self.assertIs(form.pending, True)

            async def forbidden_duplicate():
                raise AssertionError('duplicate callback invoked while original pending')

            await asyncio.wait_for(form.submit(forbidden_duplicate), 1)
            self.assertIs(form.pending, True)
            self.assertFalse(task.done())
            value = object()
            call.complete(value)
            self.assertIs(await asyncio.wait_for(task, 1), value)
            self.assertIs(form.pending, False)
            task = asyncio.create_task(form.submit(callback))
            tasks.append(task)
            call = await callback.started()
            error = RuntimeError('save failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await asyncio.wait_for(task, 1)
            self.assertIs(caught.exception, error)
            self.assertIs(form.pending, False)
            task = asyncio.create_task(form.submit(callback))
            tasks.append(task)
            call = await callback.started()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, 1)
            self.assertTrue(call.response.cancelled())
            self.assertIs(form.pending, False)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)

    async def test_retained_real_form_passes_and_missing_guard_is_detected(self):
        source_path = ASSET.parents[3] / 'benchmarks/results/bundle-contract-06/necessary-state--skill--1/project/form.py'
        source = source_path.read_text()
        await self.exercise(source)
        guard = '        if self.pending:\n            return None\n'
        self.assertEqual(source.count(guard), 1)
        with self.assertRaisesRegex(AssertionError, 'duplicate callback invoked'):
            await self.exercise(source.replace(guard, ''))
        self.assertEqual(source_path.read_text(), source)
