import asyncio
import importlib.util
from pathlib import Path
import sys
import shutil
import subprocess
import tempfile
import unittest


path = Path(__file__).resolve().parents[1] / 'skills/mother-in-law/assets/controlled_fetch.py'
spec = importlib.util.spec_from_file_location('controlled_fetch_asset', path)
asset = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = asset
spec.loader.exec_module(asset)


class StandaloneAssetTests(unittest.TestCase):
    def test_copied_support_runs_without_an_installed_skill(self):
        with tempfile.TemporaryDirectory(prefix='native QA ') as temporary:
            project = Path(temporary)
            shutil.copyfile(path, project / 'controlled_fetch.py')
            code = '''import asyncio
from controlled_fetch import ControlledFetch

async def main():
    fetch = ControlledFetch()
    task = asyncio.create_task(fetch('same'))
    try:
        request = await fetch.started('same')
        request.complete({'items': ['payload']})
        assert await asyncio.wait_for(task, 1) == {'items': ['payload']}
    finally:
        if not task.done():
            task.cancel()
        await asyncio.gather(task, return_exceptions=True)
asyncio.run(main())
print('standalone support passed')
'''
            result = subprocess.run([sys.executable, '-E', '-B', '-c', code],
                                    cwd=project, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout.strip(), 'standalone support passed')
            self.assertEqual({p.name for p in project.iterdir()}, {'controlled_fetch.py'})


class ControlledFetchAssetTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.fetch = asset.ControlledFetch()
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def start_task(self, key):
        task = asyncio.create_task(self.fetch(key))
        self.tasks.append(task)
        return task

    async def test_cancelled_entry_wait_preserves_request_during_wakeup(self):
        waiter = asyncio.create_task(self.fetch.started('same'))
        self.tasks.append(waiter)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        application = self.start_task('same')
        asyncio.get_running_loop().call_soon(waiter.cancel)
        with self.assertRaises(asyncio.CancelledError):
            await waiter
        self.assertFalse(application.done())
        request = await self.fetch.started('same')
        value = object()
        request.complete(value)
        self.assertIs(await asyncio.wait_for(application, 1), value)
        self.assertTrue(self.fetch.calls.empty())

    async def test_competing_entry_waiters_keep_distinct_requests(self):
        waiters = [asyncio.create_task(self.fetch.started('same')) for _ in range(2)]
        self.tasks.extend(waiters)
        await asyncio.sleep(0)
        first_task = self.start_task('same')
        done, pending = await asyncio.wait(waiters, timeout=1, return_when=asyncio.FIRST_COMPLETED)
        self.assertEqual(len(done), 1)
        first = done.pop().result()
        first.complete('first')
        self.assertEqual(await asyncio.wait_for(first_task, 1), 'first')
        second_task = self.start_task('same')
        second = await asyncio.wait_for(pending.pop(), 1)
        self.assertIsNot(first.response, second.response)
        second.complete('second')
        self.assertEqual(await asyncio.wait_for(second_task, 1), 'second')
        self.assertTrue(self.fetch.calls.empty())

    async def test_identical_keys_keep_distinct_reverse_completion_payloads(self):
        older = self.start_task('same')
        first = await self.fetch.started('same')
        newer = self.start_task('same')
        second = await self.fetch.started('same')
        self.assertIsNot(first.response, second.response)
        second.complete({'items': ['new'], 'count': 1})
        self.assertEqual(await asyncio.wait_for(newer, 1), {'items': ['new'], 'count': 1})
        self.assertFalse(older.done())
        first.complete({'items': ['old'], 'count': 1})
        self.assertEqual(await asyncio.wait_for(older, 1), {'items': ['old'], 'count': 1})

    async def test_controlled_error_and_later_success_are_independent(self):
        failed = self.start_task('account')
        request = await self.fetch.started('account')
        error = RuntimeError('offline')
        request.fail_request(error)
        with self.assertRaises(RuntimeError) as caught:
            await asyncio.wait_for(failed, 1)
        self.assertIs(caught.exception, error)
        recovery = self.start_task('account')
        recovered = await self.fetch.started('account')
        recovered.complete({'name': 'recovered'})
        self.assertEqual(await asyncio.wait_for(recovery, 1), {'name': 'recovered'})

    async def test_wrong_key_preserves_actual_expected_assertion(self):
        self.start_task('observed')
        with self.assertRaises(AssertionError) as caught:
            await self.fetch.started('expected')
        self.assertEqual(str(caught.exception),
                         "request key: expected 'expected', observed 'observed'")

    async def test_wait_is_bounded_and_invalid_bounds_rejected(self):
        with self.assertRaises(asyncio.TimeoutError):
            await self.fetch.started('absent', timeout=0.01)
        for timeout in (0, -1, 31, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                await self.fetch.started('absent', timeout=timeout)

    async def test_cancelled_request_does_not_cancel_same_key_sibling(self):
        older = self.start_task('same')
        first = await self.fetch.started('same')
        newer = self.start_task('same')
        second = await self.fetch.started('same')
        older.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await older
        self.assertTrue(first.response.cancelled())
        self.assertFalse(second.response.done())
        second.complete('new')
        self.assertEqual(await asyncio.wait_for(newer, 1), 'new')
        with self.assertRaises(asyncio.InvalidStateError):
            first.complete('too late')
        with self.assertRaises(asyncio.InvalidStateError):
            second.complete('twice')
