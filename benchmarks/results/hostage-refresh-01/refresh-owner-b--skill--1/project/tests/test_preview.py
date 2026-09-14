import asyncio
import unittest

from preview import Preview
from tests.controlled_call import ControlledCall


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.drain_tasks)

    async def drain_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), 1
            )

    def launch(self, preview, key, fetch):
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        return task

    async def outcome(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    async def enter(self, preview, fetch, key):
        task = self.launch(preview, key, fetch)
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    def snapshot(self, preview):
        return preview.pending, preview.value, preview.generation

    def assert_unchanged(self, preview, before):
        self.assertIs(preview.pending, before[0])
        self.assertIs(preview.value, before[1])
        self.assertEqual(preview.generation, before[2])

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        fetch = ControlledCall()
        task, call = await self.enter(preview, fetch, 'seed')
        value = {'prior': []}
        call.complete(value)
        self.assertIs(await self.outcome(task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)
        return preview, value

    async def overlap(self, preview):
        fetch = ControlledCall()
        older, first = await self.enter(preview, fetch, 'same-key')
        latest, second = await self.enter(preview, fetch, 'same-key')
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertFalse(latest.done())
        return older, first, latest, second

    async def check_success_order(self, latest_first):
        preview, prior = await self.seeded()
        older, first, latest, second = await self.overlap(preview)
        self.assertIs(preview.value, prior)
        old_value, new_value = {'old': []}, {'new': []}
        if latest_first:
            second.complete(new_value)
            self.assertIs(await self.outcome(latest), new_value)
            self.assertFalse(preview.pending)
            self.assertIs(preview.value, new_value)
            self.assertFalse(older.done())
            before = self.snapshot(preview)
            first.complete(old_value)
            self.assertIs(await self.outcome(older), old_value)
            self.assert_unchanged(preview, before)
        else:
            before = self.snapshot(preview)
            first.complete(old_value)
            self.assertIs(await self.outcome(older), old_value)
            self.assert_unchanged(preview, before)
            self.assertFalse(latest.done())
            second.complete(new_value)
            self.assertIs(await self.outcome(latest), new_value)
            self.assertFalse(preview.pending)
            self.assertIs(preview.value, new_value)

    async def test_earlier_success_then_latest_success(self):
        await self.check_success_order(latest_first=False)

    async def test_latest_success_then_earlier_success(self):
        await self.check_success_order(latest_first=True)

    async def reject(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('controlled failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)

    async def check_earlier_rejection(self, cancelled):
        preview, prior = await self.seeded()
        older, first, latest, second = await self.overlap(preview)
        self.assertIs(preview.value, prior)
        before = self.snapshot(preview)
        await self.reject(older, first, cancelled)
        self.assert_unchanged(preview, before)
        self.assertFalse(latest.done())
        value = object()
        second.complete(value)
        self.assertIs(await self.outcome(latest), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.check_earlier_rejection(cancelled=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.check_earlier_rejection(cancelled=True)

    async def check_latest_rejection_and_retry(self, cancelled):
        preview, prior = await self.seeded()
        older, first, latest, second = await self.overlap(preview)
        before = self.snapshot(preview)
        await self.reject(latest, second, cancelled)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, before[1])
        self.assertEqual(preview.generation, before[2])
        self.assertFalse(older.done())
        fetch = ControlledCall()
        retry, retry_call = await self.enter(preview, fetch, 'retry')
        self.assertIs(preview.value, prior)
        before = self.snapshot(preview)
        stale_value = object()
        first.complete(stale_value)
        self.assertIs(await self.outcome(older), stale_value)
        self.assert_unchanged(preview, before)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.outcome(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.check_latest_rejection_and_retry(cancelled=False)

    async def test_latest_cancellation_and_retry(self):
        await self.check_latest_rejection_and_retry(cancelled=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, first = await self.enter(preview, fetch, 'older')
        error = ValueError('synchronous failure')
        seen = []

        def fail(key):
            seen.append((key, preview.pending, preview.value))
            raise error

        before = self.snapshot(preview)
        failed = self.launch(preview, 'sync', fail)
        with self.assertRaises(ValueError) as caught:
            await self.outcome(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0][0], 'sync')
        self.assertIs(seen[0][1], True)
        self.assertIs(seen[0][2], prior)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, before[1])
        self.assertFalse(older.done())
        before = self.snapshot(preview)
        stale_value = object()
        first.complete(stale_value)
        self.assertIs(await self.outcome(older), stale_value)
        self.assert_unchanged(preview, before)
        retry, call = await self.enter(preview, fetch, 'retry')
        self.assertIs(preview.value, prior)
        value = object()
        call.complete(value)
        self.assertIs(await self.outcome(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instances_are_independent(self):
        left, left_prior = await self.seeded()
        right, right_prior = await self.seeded()
        fetch = ControlledCall()
        left_task, left_call = await self.enter(left, fetch, 'left')
        right_before = self.snapshot(right)
        latest, latest_call = await self.enter(left, fetch, 'left-latest')
        self.assert_unchanged(right, right_before)
        left_before = self.snapshot(left)
        right_task, right_call = await self.enter(right, fetch, 'right')
        self.assert_unchanged(left, left_before)
        right_before = self.snapshot(right)
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.outcome(latest), value)
        self.assertIs(left.value, value)
        self.assertFalse(left.pending)
        self.assert_unchanged(right, right_before)
        self.assertIs(right.value, right_prior)
        self.assertFalse(right_task.done())
        left_before = self.snapshot(left)
        await self.reject(right_task, right_call, cancelled=False)
        self.assert_unchanged(left, left_before)
        self.assertFalse(right.pending)
        self.assertIs(right.value, right_prior)
        right_before = self.snapshot(right)
        left_call.complete(left_prior)
        self.assertIs(await self.outcome(left_task), left_prior)
        self.assert_unchanged(left, left_before)
        self.assert_unchanged(right, right_before)


if __name__ == '__main__':
    unittest.main()
