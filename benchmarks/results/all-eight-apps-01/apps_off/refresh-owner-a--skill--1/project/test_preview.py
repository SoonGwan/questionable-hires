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

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        fetch = ControlledCall()
        task, call = await self.begin(preview, fetch, 'seed')
        self.assertIsNone(preview.value)
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def check_completion_order(self, latest_first):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        # Identical keys must still enter independently while both are pending.
        old, old_call = await self.begin(preview, fetch, 'same')
        latest, latest_call = await self.begin(preview, fetch, 'same')
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(old.done())
        self.assertFalse(latest.done())
        self.assertIs(preview.value, prior)
        old_value, latest_value = object(), object()
        if latest_first:
            latest_call.complete(latest_value)
            self.assertIs(await self.tasks.wait(latest), latest_value)
            self.assertFalse(old.done())
            self.assertFalse(preview.pending)
            self.assertIs(preview.value, latest_value)
            pending_before, value_before = preview.pending, preview.value
            old_call.complete(old_value)
            self.assertIs(await self.tasks.wait(old), old_value)
            self.assertEqual(preview.pending, pending_before)
            self.assertIs(preview.value, value_before)
        else:
            pending_before, value_before = preview.pending, preview.value
            old_call.complete(old_value)
            self.assertIs(await self.tasks.wait(old), old_value)
            self.assertFalse(latest.done())
            self.assertEqual(preview.pending, pending_before)
            self.assertIs(preview.value, value_before)
            latest_call.complete(latest_value)
            self.assertIs(await self.tasks.wait(latest), latest_value)
            self.assertFalse(preview.pending)
            self.assertIs(preview.value, latest_value)

    async def test_earlier_success_first(self):
        await self.check_completion_order(latest_first=False)

    async def test_latest_success_first(self):
        await self.check_completion_order(latest_first=True)

    async def settle_unsuccessfully(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError('fetch failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def check_earlier_unsuccessful(self, cancel):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        old, old_call = await self.begin(preview, fetch, 'old')
        latest, latest_call = await self.begin(preview, fetch, 'latest')
        self.assertIs(preview.value, prior)
        pending_before, value_before = preview.pending, preview.value
        await self.settle_unsuccessfully(old, old_call, cancel)
        self.assertFalse(latest.done())
        self.assertEqual(preview.pending, pending_before)
        self.assertIs(preview.value, value_before)
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.tasks.wait(latest), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.check_earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.check_earlier_unsuccessful(cancel=True)

    async def check_latest_unsuccessful_and_retry(self, cancel):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        old, old_call = await self.begin(preview, fetch, 'old')
        latest, latest_call = await self.begin(preview, fetch, 'latest')
        self.assertIs(preview.value, prior)
        await self.settle_unsuccessfully(latest, latest_call, cancel)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(old.done())
        retry, retry_call = await self.begin(preview, fetch, 'retry')
        self.assertIs(preview.value, prior)
        pending_before, value_before = preview.pending, preview.value
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(old), old_value)
        self.assertFalse(retry.done())
        self.assertEqual(preview.pending, pending_before)
        self.assertIs(preview.value, value_before)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.check_latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.check_latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        old, old_call = await self.begin(preview, fetch, 'old')
        error = ValueError('synchronous failure')
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        failed = self.tasks.start(preview.refresh('sync', raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(old.done())
        pending_before, value_before = preview.pending, preview.value
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(old), old_value)
        self.assertEqual(preview.pending, pending_before)
        self.assertIs(preview.value, value_before)
        retry, retry_call = await self.begin(preview, fetch, 'retry')
        self.assertIs(preview.value, prior)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instance_isolation(self):
        first, first_prior = await self.seeded()
        second, second_prior = await self.seeded()
        fetch = ControlledCall()
        first_task, first_call = await self.begin(first, fetch, 'first')
        second_task, second_call = await self.begin(second, fetch, 'second')
        second_pending, second_value = second.pending, second.value
        first_value = object()
        first_call.complete(first_value)
        self.assertIs(await self.tasks.wait(first_task), first_value)
        self.assertFalse(first.pending)
        self.assertIs(first.value, first_value)
        self.assertFalse(second_task.done())
        self.assertEqual(second.pending, second_pending)
        self.assertIs(second.value, second_value)
        self.assertIs(second.value, second_prior)
        first_pending, first_display = first.pending, first.value
        await self.settle_unsuccessfully(second_task, second_call, cancel=False)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertEqual(first.pending, first_pending)
        self.assertIs(first.value, first_display)


if __name__ == '__main__':
    unittest.main()
