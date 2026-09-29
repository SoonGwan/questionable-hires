import asyncio
import unittest

from preview import Preview
from preview_test_support import ControlledCall, OwnedTasks


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def begin(self, preview, key, fetch=None):
        if fetch is None:
            fetch = ControlledCall()
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(len(call.args), 1)
        self.assertIs(call.args[0], key)
        self.assertEqual(call.kwargs, {})
        return task, call

    async def seeded_preview(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        task, call = await self.begin(preview, object())
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    def assert_display(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def settle_unsuccessfully(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('controlled failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as raised:
                await self.tasks.wait(task)
            self.assertIs(raised.exception, error)

    async def check_completion_order(self, latest_first):
        preview, prior = await self.seeded_preview()
        # Reusing the exact key also guards against duplicate suppression.
        key = object()
        fetch = ControlledCall()
        earlier, earlier_call = await self.begin(preview, key, fetch)
        self.assert_display(preview, True, prior)
        latest, latest_call = await self.begin(preview, key, fetch)
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(earlier.done())
        self.assertFalse(latest.done())
        self.assert_display(preview, True, prior)
        earlier_value, latest_value = object(), object()

        if latest_first:
            latest_call.complete(latest_value)
            self.assertIs(await self.tasks.wait(latest), latest_value)
            self.assertFalse(earlier.done())
            self.assert_display(preview, False, latest_value)
            pending_before, value_before = preview.pending, preview.value
            earlier_call.complete(earlier_value)
            self.assertIs(await self.tasks.wait(earlier), earlier_value)
            self.assert_display(preview, pending_before, value_before)
        else:
            pending_before, value_before = preview.pending, preview.value
            earlier_call.complete(earlier_value)
            self.assertIs(await self.tasks.wait(earlier), earlier_value)
            self.assertFalse(latest.done())
            self.assert_display(preview, pending_before, value_before)
            latest_call.complete(latest_value)
            self.assertIs(await self.tasks.wait(latest), latest_value)
            self.assert_display(preview, False, latest_value)

    async def test_earlier_success_before_latest_success(self):
        await self.check_completion_order(latest_first=False)

    async def test_latest_success_before_earlier_success(self):
        await self.check_completion_order(latest_first=True)

    async def check_earlier_unsuccessful(self, cancelled):
        preview, prior = await self.seeded_preview()
        earlier, earlier_call = await self.begin(preview, object())
        latest, latest_call = await self.begin(preview, object())
        self.assert_display(preview, True, prior)
        pending_before, value_before = preview.pending, preview.value
        await self.settle_unsuccessfully(earlier, earlier_call, cancelled)
        self.assertFalse(latest.done())
        self.assert_display(preview, pending_before, value_before)
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_display(preview, False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.check_earlier_unsuccessful(cancelled=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.check_earlier_unsuccessful(cancelled=True)

    async def check_latest_unsuccessful_and_retry(self, cancelled):
        preview, prior = await self.seeded_preview()
        earlier, earlier_call = await self.begin(preview, object())
        latest, latest_call = await self.begin(preview, object())
        self.assert_display(preview, True, prior)
        value_before = preview.value
        await self.settle_unsuccessfully(latest, latest_call, cancelled)
        self.assertFalse(earlier.done())
        self.assert_display(preview, False, value_before)

        retry, retry_call = await self.begin(preview, object())
        self.assert_display(preview, True, prior)
        pending_before, value_before = preview.pending, preview.value
        stale_result = object()
        earlier_call.complete(stale_result)
        self.assertIs(await self.tasks.wait(earlier), stale_result)
        self.assertFalse(retry.done())
        self.assert_display(preview, pending_before, value_before)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_display(preview, False, result)

    async def test_latest_failure_and_retry(self):
        await self.check_latest_unsuccessful_and_retry(cancelled=False)

    async def test_latest_cancellation_and_retry(self):
        await self.check_latest_unsuccessful_and_retry(cancelled=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        earlier, earlier_call = await self.begin(preview, object())
        error = LookupError('synchronous failure')
        key = object()
        seen = []

        def raising_fetch(actual_key):
            seen.append(actual_key)
            self.assert_display(preview, True, prior)
            raise error

        task = self.tasks.start(preview.refresh(key, raising_fetch))
        with self.assertRaises(LookupError) as raised:
            await self.tasks.wait(task)
        self.assertIs(raised.exception, error)
        self.assertEqual(len(seen), 1)
        self.assertIs(seen[0], key)
        self.assertFalse(earlier.done())
        self.assert_display(preview, False, prior)
        pending_before, value_before = preview.pending, preview.value
        stale_result = object()
        earlier_call.complete(stale_result)
        self.assertIs(await self.tasks.wait(earlier), stale_result)
        self.assert_display(preview, pending_before, value_before)

        retry, retry_call = await self.begin(preview, key)
        self.assert_display(preview, True, prior)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_display(preview, False, result)

    async def test_instances_are_independent(self):
        first, first_prior = await self.seeded_preview()
        second, second_prior = await self.seeded_preview()
        first_task, first_call = await self.begin(first, object())
        second_task, second_call = await self.begin(second, object())
        self.assert_display(first, True, first_prior)
        self.assert_display(second, True, second_prior)
        second_pending, second_value = second.pending, second.value
        first_result = object()
        first_call.complete(first_result)
        self.assertIs(await self.tasks.wait(first_task), first_result)
        self.assert_display(first, False, first_result)
        self.assertFalse(second_task.done())
        self.assert_display(second, second_pending, second_value)

        first_retry, first_retry_call = await self.begin(first, object())
        first_pending, first_value = first.pending, first.value
        await self.settle_unsuccessfully(second_task, second_call, False)
        self.assert_display(second, False, second_prior)
        self.assertFalse(first_retry.done())
        self.assert_display(first, first_pending, first_value)
        result = object()
        first_retry_call.complete(result)
        self.assertIs(await self.tasks.wait(first_retry), result)
        self.assert_display(first, False, result)
        self.assert_display(second, False, second_prior)


if __name__ == '__main__':
    unittest.main()
