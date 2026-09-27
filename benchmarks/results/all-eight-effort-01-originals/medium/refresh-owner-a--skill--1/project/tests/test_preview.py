import asyncio
import unittest

from preview import Preview
from tests.controlled_call import ControlledCall, OwnedTasks


class PreviewRefreshTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    def assert_display(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def enter(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    async def seeded_preview(self):
        preview = Preview()
        self.assert_display(preview, False, None)
        fetch = ControlledCall()
        task, call = await self.enter(preview, fetch, 'seed')
        self.assert_display(preview, True, None)
        prior = object()
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assert_display(preview, False, prior)
        return preview

    async def overlap(self):
        preview = await self.seeded_preview()
        prior = preview.value
        fetch = ControlledCall()
        # Identical keys must still invoke fetch independently.
        older, old_call = await self.enter(preview, fetch, 'same-key')
        self.assert_display(preview, True, prior)
        latest, latest_call = await self.enter(preview, fetch, 'same-key')
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assert_display(preview, True, prior)
        return preview, older, old_call, latest, latest_call

    async def test_earlier_success_while_latest_pending(self):
        preview, older, old_call, latest, latest_call = await self.overlap()
        pending, value = preview.pending, preview.value
        stale_result = object()
        old_call.complete(stale_result)
        self.assertIs(await self.tasks.wait(older), stale_result)
        self.assert_display(preview, pending, value)
        self.assertFalse(latest.done())
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_display(preview, False, result)

    async def test_latest_success_before_earlier_success(self):
        preview, older, old_call, latest, latest_call = await self.overlap()
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_display(preview, False, result)
        self.assertFalse(older.done())
        pending, value = preview.pending, preview.value
        stale_result = object()
        old_call.complete(stale_result)
        self.assertIs(await self.tasks.wait(older), stale_result)
        self.assert_display(preview, pending, value)

    async def settle_unsuccessfully(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError('fetch failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as raised:
                await self.tasks.wait(task)
            self.assertIs(raised.exception, error)

    async def earlier_unsuccessful(self, cancelled):
        preview, older, old_call, latest, latest_call = await self.overlap()
        pending, value = preview.pending, preview.value
        await self.settle_unsuccessfully(older, old_call, cancelled)
        self.assert_display(preview, pending, value)
        self.assertFalse(latest.done())
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_display(preview, False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancelled=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancelled=True)

    async def latest_unsuccessful_and_retry(self, cancelled):
        preview, older, old_call, latest, latest_call = await self.overlap()
        prior = preview.value
        await self.settle_unsuccessfully(latest, latest_call, cancelled)
        self.assert_display(preview, False, prior)
        self.assertFalse(older.done())
        fetch = ControlledCall()
        retry, retry_call = await self.enter(preview, fetch, 'retry')
        self.assert_display(preview, True, prior)
        pending, value = preview.pending, preview.value
        stale_result = object()
        old_call.complete(stale_result)
        self.assertIs(await self.tasks.wait(older), stale_result)
        self.assert_display(preview, pending, value)
        self.assertFalse(retry.done())
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_display(preview, False, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancelled=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancelled=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview = await self.seeded_preview()
        prior = preview.value
        fetch = ControlledCall()
        older, old_call = await self.enter(preview, fetch, 'older')
        error = ValueError('synchronous fetch failure')
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assert_display(preview, True, prior)
            raise error

        failed = self.tasks.start(preview.refresh('sync', raising_fetch))
        with self.assertRaises(ValueError) as raised:
            await self.tasks.wait(failed)
        self.assertIs(raised.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assert_display(preview, False, prior)
        self.assertFalse(older.done())
        pending, value = preview.pending, preview.value
        stale_result = object()
        old_call.complete(stale_result)
        self.assertIs(await self.tasks.wait(older), stale_result)
        self.assert_display(preview, pending, value)
        retry, retry_call = await self.enter(preview, fetch, 'retry')
        self.assert_display(preview, True, prior)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_display(preview, False, result)

    async def test_instance_isolation(self):
        first = await self.seeded_preview()
        second = await self.seeded_preview()
        first_prior, second_prior = first.value, second.value
        first_fetch, second_fetch = ControlledCall(), ControlledCall()
        first_task, first_call = await self.enter(first, first_fetch, 'first')
        self.assert_display(second, False, second_prior)
        second_task, second_call = await self.enter(second, second_fetch, 'second')
        self.assert_display(first, True, first_prior)
        self.assert_display(second, True, second_prior)
        first_result = object()
        first_call.complete(first_result)
        self.assertIs(await self.tasks.wait(first_task), first_result)
        self.assert_display(first, False, first_result)
        self.assert_display(second, True, second_prior)
        self.assertFalse(second_task.done())
        second_result = object()
        second_call.complete(second_result)
        self.assertIs(await self.tasks.wait(second_task), second_result)
        self.assert_display(second, False, second_result)
        self.assert_display(first, False, first_result)
