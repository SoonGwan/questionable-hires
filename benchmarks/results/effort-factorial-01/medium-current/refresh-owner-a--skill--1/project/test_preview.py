import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def begin(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    async def seeded_preview(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        fetch = ControlledCall()
        task, call = await self.begin(preview, fetch, 'seed')
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def reject(self, task, call, mode):
        if mode == 'failure':
            error = RuntimeError('fetch failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)

    async def test_both_success_completion_orders(self):
        for first in ('earlier', 'latest'):
            with self.subTest(first=first):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                earlier, old_call = await self.begin(preview, fetch, 'same-key')
                latest, new_call = await self.begin(preview, fetch, 'same-key')
                self.assertEqual(len(fetch.calls), 2)
                self.assertFalse(earlier.done())
                self.assertFalse(latest.done())
                self.assertIs(preview.value, prior)
                old_value, new_value = object(), object()
                if first == 'earlier':
                    before = preview.pending, preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(earlier), old_value)
                    self.assertIs(preview.pending, before[0])
                    self.assertIs(preview.value, before[1])
                    self.assertFalse(latest.done())
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                else:
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertFalse(preview.pending)
                    self.assertIs(preview.value, new_value)
                    self.assertFalse(earlier.done())
                    before = preview.pending, preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(earlier), old_value)
                    self.assertIs(preview.pending, before[0])
                    self.assertIs(preview.value, before[1])
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, new_value)

    async def test_earlier_failure_or_cancellation_leaves_latest_pending(self):
        for mode in ('failure', 'cancellation'):
            with self.subTest(mode=mode):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                earlier, old_call = await self.begin(preview, fetch, 'earlier')
                latest, new_call = await self.begin(preview, fetch, 'latest')
                before = preview.pending, preview.value
                await self.reject(earlier, old_call, mode)
                self.assertIs(preview.pending, before[0])
                self.assertIs(preview.value, before[1])
                self.assertIs(preview.value, prior)
                self.assertFalse(latest.done())
                result = object()
                new_call.complete(result)
                self.assertIs(await self.tasks.wait(latest), result)
                self.assertIs(preview.value, result)
                self.assertFalse(preview.pending)

    async def test_latest_failure_or_cancellation_and_retry(self):
        for mode in ('failure', 'cancellation'):
            with self.subTest(mode=mode):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                earlier, old_call = await self.begin(preview, fetch, 'earlier')
                latest, new_call = await self.begin(preview, fetch, 'latest')
                await self.reject(latest, new_call, mode)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, prior)
                self.assertFalse(earlier.done())
                before = preview.pending, preview.value
                stale_result = object()
                old_call.complete(stale_result)
                self.assertIs(await self.tasks.wait(earlier), stale_result)
                self.assertIs(preview.pending, before[0])
                self.assertIs(preview.value, before[1])
                retry, retry_call = await self.begin(preview, fetch, 'latest')
                self.assertIs(preview.value, prior)
                result = object()
                retry_call.complete(result)
                self.assertIs(await self.tasks.wait(retry), result)
                self.assertIs(preview.value, result)
                self.assertFalse(preview.pending)
                self.assertEqual(len(fetch.calls), 3)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        earlier, old_call = await self.begin(preview, fetch, 'earlier')
        error = ValueError('synchronous fetch failure')
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            raise error

        task = self.tasks.start(preview.refresh('sync', raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(earlier.done())
        retry, retry_call = await self.begin(preview, fetch, 'sync')
        before = preview.pending, preview.value
        old_result = object()
        old_call.complete(old_result)
        self.assertIs(await self.tasks.wait(earlier), old_result)
        self.assertIs(preview.pending, before[0])
        self.assertIs(preview.value, before[1])
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assertIs(preview.value, result)
        self.assertFalse(preview.pending)

    async def test_instances_are_independent(self):
        left, left_prior = await self.seeded_preview()
        right, right_prior = await self.seeded_preview()
        fetch = ControlledCall()
        left_old, left_old_call = await self.begin(left, fetch, 'same')
        left_new, left_new_call = await self.begin(left, fetch, 'same')
        right_task, right_call = await self.begin(right, fetch, 'same')
        self.assertIs(left.value, left_prior)
        self.assertIs(right.value, right_prior)
        left_before = left.pending, left.value
        right_result = object()
        right_call.complete(right_result)
        self.assertIs(await self.tasks.wait(right_task), right_result)
        self.assertFalse(right.pending)
        self.assertIs(right.value, right_result)
        self.assertIs(left.pending, left_before[0])
        self.assertIs(left.value, left_before[1])
        right_before = right.pending, right.value
        left_result = object()
        left_new_call.complete(left_result)
        self.assertIs(await self.tasks.wait(left_new), left_result)
        self.assertFalse(left.pending)
        self.assertIs(left.value, left_result)
        self.assertFalse(left_old.done())
        await self.reject(left_old, left_old_call, 'failure')
        self.assertFalse(left.pending)
        self.assertIs(left.value, left_result)
        self.assertIs(right.pending, right_before[0])
        self.assertIs(right.value, right_before[1])
        self.assertEqual(len(fetch.calls), 3)
