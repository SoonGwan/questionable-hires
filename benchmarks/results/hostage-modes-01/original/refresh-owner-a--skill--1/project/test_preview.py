import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.drain_tasks)
        self.preview = Preview()
        self.fetch = ControlledCall()
        self.prior = object()
        task, call = await self.start()
        call.complete(self.prior)
        self.assertIs(await self.result(task), self.prior)
        self.assertFalse(self.preview.pending)

    async def drain_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True), 1
        )

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    async def start(self, preview=None, fetch=None, key='same-key'):
        preview = self.preview if preview is None else preview
        fetch = self.fetch if fetch is None else fetch
        prior = preview.value
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        return task, call

    def snapshot(self, preview=None):
        preview = self.preview if preview is None else preview
        return preview.pending, preview.value, preview.generation

    def assert_state(self, before, preview=None):
        after = self.snapshot(preview)
        self.assertEqual(after[0], before[0])
        self.assertIs(after[1], before[1])
        self.assertEqual(after[2], before[2])

    async def settle_unsuccessfully(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('fetch failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(task)
            self.assertIs(caught.exception, error)

    async def test_earlier_success_before_latest_success(self):
        old, old_call = await self.start()
        latest, latest_call = await self.start()
        self.assertEqual(len(self.fetch.calls), 3)
        before = self.snapshot()
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_state(before)
        self.assertFalse(latest.done())
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.result(latest), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_latest_success_before_earlier_success(self):
        old, old_call = await self.start()
        latest, latest_call = await self.start()
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.result(latest), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)
        self.assertFalse(old.done())
        before = self.snapshot()
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_state(before)

    async def earlier_unsuccessful(self, cancel):
        old, old_call = await self.start()
        latest, latest_call = await self.start()
        before = self.snapshot()
        await self.settle_unsuccessfully(old, old_call, cancel)
        self.assert_state(before)
        self.assertTrue(self.preview.pending)
        self.assertFalse(latest.done())
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.result(latest), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_earlier_failure_keeps_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_keeps_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        old, old_call = await self.start()
        latest, latest_call = await self.start()
        before = self.snapshot()
        await self.settle_unsuccessfully(latest, latest_call, cancel)
        self.assert_state((False, before[1], before[2]))
        self.assertFalse(old.done())
        retry, retry_call = await self.start()
        before = self.snapshot()
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_state(before)
        self.assertFalse(retry.done())
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_latest_failure_clears_pending_and_allows_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_clears_pending_and_allows_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        old, old_call = await self.start()
        error = RuntimeError('synchronous failure')
        keys = []
        before = self.snapshot()

        def fail(key):
            keys.append(key)
            self.assertTrue(self.preview.pending)
            self.assertIs(self.preview.value, before[1])
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await asyncio.wait_for(self.preview.refresh('sync', fail), 1)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assert_state((False, before[1], before[2] + 1))
        self.assertFalse(old.done())
        retry, retry_call = await self.start()
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)
        before = self.snapshot()
        old_call.complete(self.prior)
        self.assertIs(await self.result(old), self.prior)
        self.assert_state(before)

    async def test_instance_isolation(self):
        other = Preview()
        other_fetch = ControlledCall()
        self.assert_state((False, None, 0), other)
        first, first_call = await self.start()
        first_before = self.snapshot()
        second, second_call = await self.start(other, other_fetch)
        self.assert_state(first_before)
        other_before = self.snapshot(other)
        value = object()
        first_call.complete(value)
        self.assertIs(await self.result(first), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)
        self.assert_state(other_before, other)
        self.assertFalse(second.done())
        first_before = self.snapshot()
        other_value = object()
        second_call.complete(other_value)
        self.assertIs(await self.result(second), other_value)
        self.assertIs(other.value, other_value)
        self.assertFalse(other.pending)
        self.assert_state(first_before)


if __name__ == '__main__':
    unittest.main()
