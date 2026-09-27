import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def start_refresh(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        return task, call

    async def seeded_preview(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        fetch = ControlledCall()
        task, call = await self.start_refresh(preview, fetch, 'seed')
        self.assertTrue(preview.pending)
        prior = {'prior': []}
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    def assert_display(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def settle_unsuccessfully(self, task, call, outcome):
        if outcome == 'failure':
            error = RuntimeError('controlled failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as raised:
                await self.tasks.wait(task)
            self.assertIs(raised.exception, error)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                # Identical keys must still invoke both callbacks concurrently.
                older, old_call = await self.start_refresh(preview, fetch, 'same')
                latest, new_call = await self.start_refresh(preview, fetch, 'same')
                self.assertEqual(len(fetch.calls), 2)
                self.assertFalse(older.done())
                self.assertFalse(latest.done())
                self.assert_display(preview, True, prior)
                old_value, new_value = {'old': []}, {'new': []}
                if latest_first:
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertFalse(older.done())
                    self.assert_display(preview, False, new_value)
                    saved_pending, saved_value = preview.pending, preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assert_display(preview, saved_pending, saved_value)
                else:
                    saved_pending, saved_value = preview.pending, preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assertFalse(latest.done())
                    self.assert_display(preview, saved_pending, saved_value)
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assert_display(preview, False, new_value)

    async def test_earlier_failure_or_cancellation_preserves_latest_pending(self):
        for outcome in ('failure', 'cancellation'):
            with self.subTest(outcome=outcome):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                older, old_call = await self.start_refresh(preview, fetch, 'older')
                latest, new_call = await self.start_refresh(preview, fetch, 'latest')
                self.assert_display(preview, True, prior)
                saved_pending, saved_value = preview.pending, preview.value
                await self.settle_unsuccessfully(older, old_call, outcome)
                self.assertFalse(latest.done())
                self.assert_display(preview, saved_pending, saved_value)
                value = object()
                new_call.complete(value)
                self.assertIs(await self.tasks.wait(latest), value)
                self.assert_display(preview, False, value)

    async def test_latest_failure_or_cancellation_and_retry(self):
        for outcome in ('failure', 'cancellation'):
            with self.subTest(outcome=outcome):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                older, old_call = await self.start_refresh(preview, fetch, 'older')
                latest, new_call = await self.start_refresh(preview, fetch, 'latest')
                self.assert_display(preview, True, prior)
                await self.settle_unsuccessfully(latest, new_call, outcome)
                self.assertFalse(older.done())
                self.assert_display(preview, False, prior)
                retry, retry_call = await self.start_refresh(preview, fetch, 'latest')
                self.assert_display(preview, True, prior)
                saved_pending, saved_value = preview.pending, preview.value
                old_value = object()
                old_call.complete(old_value)
                self.assertIs(await self.tasks.wait(older), old_value)
                self.assertFalse(retry.done())
                self.assert_display(preview, saved_pending, saved_value)
                value = object()
                retry_call.complete(value)
                self.assertIs(await self.tasks.wait(retry), value)
                self.assert_display(preview, False, value)
                self.assertEqual(len(fetch.calls), 3)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        older, old_call = await self.start_refresh(preview, fetch, 'older')
        error = ValueError('synchronous failure')
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assert_display(preview, True, prior)
            raise error

        latest = self.tasks.start(preview.refresh('sync', raising_fetch))
        with self.assertRaises(ValueError) as raised:
            await self.tasks.wait(latest)
        self.assertIs(raised.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assertFalse(older.done())
        self.assert_display(preview, False, prior)
        saved_pending, saved_value = preview.pending, preview.value
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(older), old_value)
        self.assert_display(preview, saved_pending, saved_value)
        retry, retry_call = await self.start_refresh(preview, fetch, 'sync')
        self.assert_display(preview, True, prior)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assert_display(preview, False, value)

    async def test_instance_isolation(self):
        first, first_prior = await self.seeded_preview()
        second, second_prior = await self.seeded_preview()
        fetch = ControlledCall()
        first_task, first_call = await self.start_refresh(first, fetch, 'same')
        second_task, second_call = await self.start_refresh(second, fetch, 'same')
        self.assert_display(first, True, first_prior)
        self.assert_display(second, True, second_prior)
        saved_pending, saved_value = second.pending, second.value
        value = object()
        first_call.complete(value)
        self.assertIs(await self.tasks.wait(first_task), value)
        self.assert_display(first, False, value)
        self.assertFalse(second_task.done())
        self.assert_display(second, saved_pending, saved_value)
        await self.settle_unsuccessfully(second_task, second_call, 'failure')
        self.assert_display(second, False, second_prior)
        self.assert_display(first, False, value)
        self.assertEqual(len(fetch.calls), 2)


if __name__ == '__main__':
    unittest.main()
