import ast
import asyncio
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'skills/hostage-negotiator/assets/controlled_call.py'
spec = importlib.util.spec_from_file_location('owned_tasks_asset', ASSET)
asset = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asset)


class OwnedTaskTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.owner = asset.OwnedTasks(timeout=0.05)
        self.addAsyncCleanup(self.owner.close)

    async def test_exact_value_error_and_independent_calls(self):
        callback = asset.ControlledCall()
        first = self.owner.start(callback('same'))
        second = self.owner.start(callback('same'))
        a, b = await callback.started(), await callback.started()
        value, error = object(), ValueError('owned error')
        b.complete(value)
        self.assertIs(await self.owner.wait(second), value)
        self.assertFalse(first.done())
        a.fail(error)
        with self.assertRaises(ValueError) as caught:
            await self.owner.wait(first)
        self.assertIs(caught.exception, error)

    async def test_wait_timeout_does_not_cancel_application(self):
        callback = asset.ControlledCall()
        task = self.owner.start(callback())
        call = await callback.started()
        with self.assertRaises(asyncio.TimeoutError):
            await self.owner.wait(task)
        self.assertFalse(task.done())
        call.complete('later')
        self.assertEqual(await self.owner.wait(task), 'later')

    async def test_waiter_cancellation_does_not_cancel_application(self):
        callback = asset.ControlledCall()
        task = self.owner.start(callback())
        call = await callback.started()
        waiter = asyncio.create_task(self.owner.wait(task))
        await asyncio.sleep(0)
        waiter.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await waiter
        self.assertFalse(task.done())
        call.complete(42)
        self.assertEqual(await self.owner.wait(task), 42)

    async def test_close_drains_only_owned_tasks_and_is_repeatable(self):
        entered, drained = asyncio.Event(), asyncio.Event()
        async def pending():
            entered.set()
            try:
                await asyncio.Future()
            finally:
                drained.set()
        task = self.owner.start(pending())
        await entered.wait()
        foreign = asyncio.create_task(asyncio.Event().wait())
        try:
            await self.owner.close()
            self.assertTrue(task.cancelled())
            self.assertTrue(drained.is_set())
            self.assertFalse(foreign.done())
            await self.owner.close()
        finally:
            foreign.cancel()
            await asyncio.gather(foreign, return_exceptions=True)

    async def test_cleanup_timeout_is_honest_and_owner_can_drain_later(self):
        entered, cancellation, release = asyncio.Event(), asyncio.Event(), asyncio.Event()
        async def resistant():
            entered.set()
            try:
                await asyncio.Future()
            except asyncio.CancelledError:
                cancellation.set()
                await release.wait()
                return 'drained later'
        task = self.owner.start(resistant())
        await entered.wait()
        try:
            with self.assertRaisesRegex(asyncio.TimeoutError, 'cleanup incomplete: 1 pending'):
                await self.owner.close()
            self.assertTrue(cancellation.is_set())
            self.assertFalse(task.done())
        finally:
            release.set()
        self.assertEqual(await self.owner.wait(task), 'drained later')
        await self.owner.close()

    async def test_no_foreign_wait_or_new_start_after_close(self):
        future = asyncio.get_running_loop().create_future()
        try:
            with self.assertRaisesRegex(ValueError, 'not owned'):
                await self.owner.wait(future)
            self.assertFalse(future.done())
        finally:
            future.cancel()
        await self.owner.close()
        coroutine = asyncio.sleep(0)
        try:
            with self.assertRaisesRegex(RuntimeError, 'closed'):
                self.owner.start(coroutine)
        finally:
            coroutine.close()

    async def test_invalid_deadlines_and_empty_cleanup(self):
        for timeout in (0, -1, 31, float('nan'), float('inf')):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                asset.OwnedTasks(timeout=timeout)
        await self.owner.close()


class NativeOwnedTaskTests(unittest.TestCase):
    def test_retained_application_assertions_work_with_owned_task_support(self):
        original = ROOT / 'benchmarks/results/all-eight-current-02/current/refresh-owner-a--skill--1/project'
        source = (original / 'test_preview.py').read_text()
        definitions = next(n.body for n in ast.parse(source).body
                           if isinstance(n, ast.ClassDef) and n.name == 'PreviewTests')
        # Replace only the four plumbing methods, not application assertions.
        names = {'asyncSetUp', 'cleanup_tasks', 'launch', 'outcome'}
        methods = [n for n in definitions if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        selected = [n for n in methods if n.name in names]
        self.assertEqual({n.name for n in selected}, names)
        start, end = min(n.lineno for n in selected), max(n.end_lineno for n in selected)
        replacement = '''    async def asyncSetUp(self):
        self.owner = OwnedTasks()
        self.addAsyncCleanup(self.owner.close)

    def launch(self, preview, key, fetch):
        return self.owner.start(preview.refresh(key, fetch))

    async def outcome(self, task):
        return await self.owner.wait(task)
'''
        lines = source.splitlines(keepends=True)
        revised = ''.join(lines[:start-1]) + replacement + ''.join(lines[end:])
        revised = revised.replace('from controlled_call import ControlledCall',
                                  'from controlled_call import ControlledCall, OwnedTasks')
        remaining = lambda text: {n.name: ast.dump(n, include_attributes=False)
            for c in ast.parse(text).body if isinstance(c, ast.ClassDef)
            for n in c.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name not in names}
        self.assertEqual(remaining(source), remaining(revised))
        fixed = (original / 'preview.py').read_text()
        before = {name: (original/name).read_bytes() for name in ('preview.py', 'test_preview.py', 'controlled_call.py')}
        guard = '            if generation == self.generation:\n                self.pending = False'
        self.assertEqual(fixed.count(guard), 1)
        variants = [('correct', fixed, 0),
                    ('broken', fixed.replace(guard, '            self.pending = False'), 1),
                    ('valid_counter_step', fixed.replace('self.generation += 1', 'self.generation += 2'), 0)]
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch:
            project = Path(scratch)
            shutil.copy2(ASSET, project/'controlled_call.py')
            (project/'test_preview.py').write_text(revised)
            for name, implementation, expected in variants:
                with self.subTest(variant=name):
                    (project/'preview.py').write_text(implementation)
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                                            cwd=project, capture_output=True, text=True, timeout=10)
                    output = result.stdout + result.stderr
                    self.assertEqual(result.returncode, expected, output)
                    self.assertIn('Ran 9 tests', output)
                    self.assertNotIn('ERROR:', output)
                    if expected:
                        self.assertIn('FAILED (failures=4)', output)
                        self.assertIn('AssertionError: False is not True', output)
        for name, content in before.items():
            self.assertEqual((original/name).read_bytes(), content)

    def test_native_assertion_survives_pending_task_cleanup_in_standalone_copy(self):
        code = '''import asyncio
import unittest
from controlled_call import ControlledCall, OwnedTasks

class Native(unittest.IsolatedAsyncioTestCase):
    async def test_contract(self):
        owner = OwnedTasks()
        self.addAsyncCleanup(owner.close)
        callback = ControlledCall()
        stopped = asyncio.Event()
        async def application():
            try:
                return await callback()
            finally:
                stopped.set()
        task = owner.start(application())
        await callback.started_before(task)
        async def verify_cleanup():
            self.assertTrue(task.cancelled())
            self.assertTrue(stopped.is_set())
            print('OWNED_TASK_DRAINED')
        # Cleanup is LIFO: drain before verifying the actual task's outcome.
        self.addAsyncCleanup(verify_cleanup)
        self.addAsyncCleanup(owner.close)
        self.assertEqual('observed', EXPECTED)

if __name__ == '__main__':
    unittest.main(verbosity=2)
'''
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks/local-runs') as scratch:
            project = Path(scratch)
            shutil.copy2(ASSET, project / 'controlled_call.py')
            for expected, exit_code in (('observed', 0), ('expected', 1)):
                result = subprocess.run([sys.executable, '-B', '-c', code.replace('EXPECTED', repr(expected))],
                                        cwd=project, capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
                self.assertEqual(result.returncode, exit_code, output)
                self.assertIn('Ran 1 test', output)
                self.assertIn('OWNED_TASK_DRAINED', output)
                self.assertNotIn('ERROR:', output)
                if exit_code:
                    self.assertIn("AssertionError: 'observed' != 'expected'", output)
            self.assertEqual((project / 'controlled_call.py').read_bytes(), ASSET.read_bytes())
