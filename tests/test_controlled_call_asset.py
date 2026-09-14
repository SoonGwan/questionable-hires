import asyncio
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
    async def test_plain_entry_wait_cannot_observe_already_completed_application(self):
        task = asyncio.create_task(asyncio.sleep(0, result='skipped callback'))
        self.tasks.append(task)
        self.assertEqual(await task, 'skipped callback')
        with self.assertRaises(asyncio.TimeoutError):
            await self.callback.started(0.01)

    async def test_task_aware_wait_reports_exact_outcomes_without_timeout(self):
        value, error = object(), ValueError('callback skipped')
        for status, result in [('completed', value), ('failed', error), ('cancelled', None)]:
            task = asyncio.get_running_loop().create_future()
            if status == 'completed': task.set_result(result)
            elif status == 'failed': task.set_exception(result)
            else: task.cancel()
            with self.assertRaises(asset.EntryNotObserved) as caught:
                await self.callback.started_before(task, timeout=30)
            self.assertEqual(caught.exception.outcome['status'], status)
            if status != 'cancelled':
                self.assertIs(caught.exception.outcome['error' if status == 'failed' else 'value'], result)

    async def test_task_aware_wait_preserves_entry_arguments_results_and_errors(self):
        for queued in (False, True):
            argument = object()
            task = self.start(argument, named=argument)
            if queued: await asyncio.sleep(0)
            call = await self.callback.started_before(task)
            self.assertIs(call.args[0], argument)
            self.assertIs(call.kwargs['named'], argument)
            value = object()
            call.complete(value)
            self.assertIs(await task, value)

    async def test_task_aware_timeout_and_cancellation_leave_application_alive(self):
        gate = asyncio.Event()
        async def application():
            await gate.wait()
            return await self.callback('later')
        task = asyncio.create_task(application())
        self.tasks.append(task)
        with self.assertRaises(asyncio.TimeoutError):
            await self.callback.started_before(task, timeout=0.01)
        waiter = asyncio.create_task(self.callback.started_before(task, timeout=30))
        await asyncio.sleep(0)
        waiter.cancel()
        with self.assertRaises(asyncio.CancelledError): await waiter
        self.assertFalse(task.done())
        gate.set()
        call = await self.callback.started_before(task)
        self.assertEqual(call.args, ('later',))
        call.complete('result')
        self.assertEqual(await task, 'result')

    async def test_cancelled_waiter_does_not_consume_entry_queued_during_wakeup(self):
        task = asyncio.get_running_loop().create_future()
        waiter = asyncio.create_task(self.callback.started_before(task))
        await asyncio.sleep(0)
        application = self.start('preserved')
        await asyncio.sleep(0)
        self.assertEqual(len(self.callback.calls), 1)
        waiter.cancel()
        with self.assertRaises(asyncio.CancelledError): await waiter
        call = await self.callback.started()
        self.assertEqual(call.args, ('preserved',))
        call.complete()
        await application
        task.set_result(None)

    async def test_queued_entry_wins_and_competing_waits_do_not_duplicate_calls(self):
        task = self.start('first')
        await asyncio.sleep(0)
        finished = asyncio.get_running_loop().create_future()
        finished.set_result(None)
        call = await self.callback.started_before(finished)
        self.assertEqual(call.args, ('first',))
        call.complete()
        await task
        with self.assertRaises(asset.EntryNotObserved):
            await self.callback.started_before(finished)
        app = self.start('second')
        waits = [asyncio.create_task(self.callback.started_before(app)) for _ in range(2)]
        done, pending = await asyncio.wait(waits, return_when=asyncio.FIRST_COMPLETED)
        self.assertEqual(len(done), 1)
        entry = done.pop().result()
        entry.complete('finished')
        with self.assertRaises(asset.EntryNotObserved): await pending.pop()
        self.assertEqual(await app, 'finished')

    async def test_task_aware_wait_rejects_wrong_loop_and_non_task_without_scheduling(self):
        for task in (None, object()):
            with self.assertRaises(TypeError): await self.callback.started_before(task)
        other = asyncio.new_event_loop()
        try:
            with self.assertRaises(TypeError): await self.callback.started_before(other.create_future())
        finally: other.close()
        for timeout in (0, -1, 31, float('nan'), float('inf')):
            with self.assertRaises(ValueError): await self.callback.started_before(None, timeout)

    async def test_application_cancellation_wakes_entry_wait_without_becoming_waiter_cancellation(self):
        gate = asyncio.Event()
        task = asyncio.create_task(gate.wait())
        self.tasks.append(task)
        waiter = asyncio.create_task(self.callback.started_before(task, timeout=30))
        await asyncio.sleep(0)
        task.cancel()
        with self.assertRaises(asset.EntryNotObserved) as caught:
            await asyncio.wait_for(waiter, 1)
        self.assertEqual(caught.exception.outcome, {'status': 'cancelled'})
        self.assertTrue(task.cancelled())

    async def test_real_two_stage_operation_keeps_results_and_rejects_skipped_decode(self):
        for skip in (False, True):
            fetch, decode = asset.ControlledCall(), asset.ControlledCall()
            payload, result = object(), object()
            async def application():
                received = await fetch()
                if skip: return received
                return await decode(received)
            task = asyncio.create_task(application())
            self.tasks.append(task)
            (await fetch.started_before(task)).complete(payload)
            if skip:
                with self.assertRaises(asset.EntryNotObserved) as caught:
                    await asyncio.wait_for(decode.started_before(task, timeout=30), 1)
                self.assertEqual(caught.exception.outcome['status'], 'completed')
                self.assertIs(caught.exception.outcome['value'], payload)
                self.assertIs(await task, payload)
                self.assertEqual(decode.calls, [])
            else:
                entry = await decode.started_before(task)
                self.assertIs(entry.args[0], payload)
                entry.complete(result)
                self.assertIs(await task, result)

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
        call = await callback.started_before(task)
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
