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
        self.assertTrue(preview.pending)
        return task, call

    async def seeded_preview(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        fetch = ControlledCall()
        task, call = await self.start_refresh(preview, fetch, 'seed')
        prior = {'display': ['prior']}
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def assert_unsuccessful(self, task, call, cancellation):
        if cancellation:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('controlled failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview, prior = await self.seeded_preview()
                fetch = ControlledCall()
                # Repeated keys must still invoke the callback independently.
                old, old_call = await self.start_refresh(preview, fetch, 'same')
                latest, latest_call = await self.start_refresh(preview, fetch, 'same')
                self.assertEqual(len(fetch.calls), 2)
                self.assertFalse(old.done())
                self.assertFalse(latest.done())
                self.assertIs(preview.value, prior)
                old_value, new_value = {'old': []}, {'new': []}
                if latest_first:
                    latest_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertFalse(old.done())
                    self.assertFalse(preview.pending)
                    self.assertIs(preview.value, new_value)
                    retained, pending = preview.value, preview.pending
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(old), old_value)
                    self.assertIs(preview.value, retained)
                    self.assertEqual(preview.pending, pending)
                else:
                    retained, pending = preview.value, preview.pending
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(old), old_value)
                    self.assertFalse(latest.done())
                    self.assertIs(preview.value, retained)
                    self.assertEqual(preview.pending, pending)
                    latest_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertIs(preview.value, new_value)
                    self.assertFalse(preview.pending)

    async def earlier_unsuccessful(self, cancellation):
        preview, prior = await self.seeded_preview()
        old_fetch, latest_fetch = ControlledCall(), ControlledCall()
        old, old_call = await self.start_refresh(preview, old_fetch, 'old')
        latest, latest_call = await self.start_refresh(preview, latest_fetch, 'latest')
        retained, pending = preview.value, preview.pending
        await self.assert_unsuccessful(old, old_call, cancellation)
        self.assertFalse(latest.done())
        self.assertIs(preview.value, retained)
        self.assertEqual(preview.pending, pending)
        self.assertIs(retained, prior)
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.tasks.wait(latest), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_earlier_failure_keeps_latest_pending(self):
        await self.earlier_unsuccessful(False)

    async def test_earlier_cancellation_keeps_latest_pending(self):
        await self.earlier_unsuccessful(True)

    async def latest_unsuccessful_and_retry(self, cancellation):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        old, old_call = await self.start_refresh(preview, fetch, 'old')
        latest, latest_call = await self.start_refresh(preview, fetch, 'latest')
        retained = preview.value
        await self.assert_unsuccessful(latest, latest_call, cancellation)
        self.assertFalse(preview.pending)
        self.assertFalse(old.done())
        self.assertIs(preview.value, retained)
        retry, retry_call = await self.start_refresh(preview, fetch, 'latest')
        self.assertEqual(len(fetch.calls), 3)
        self.assertIs(preview.value, prior)
        retained, pending = preview.value, preview.pending
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(old), old_value)
        self.assertFalse(retry.done())
        self.assertIs(preview.value, retained)
        self.assertEqual(preview.pending, pending)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        old, old_call = await self.start_refresh(preview, fetch, 'old')
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
        retained, pending = preview.value, preview.pending
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(old), old_value)
        self.assertIs(preview.value, retained)
        self.assertEqual(preview.pending, pending)
        retry, retry_call = await self.start_refresh(preview, fetch, 'sync')
        self.assertIs(preview.value, prior)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instances_are_independent(self):
        first, first_prior = await self.seeded_preview()
        second, second_prior = await self.seeded_preview()
        fetch = ControlledCall()
        first_task, first_call = await self.start_refresh(first, fetch, 'same')
        second_task, second_call = await self.start_refresh(second, fetch, 'same')
        first_latest, first_latest_call = await self.start_refresh(first, fetch, 'same')
        self.assertEqual(len(fetch.calls), 3)
        first_state = first.value, first.pending
        second_value = object()
        second_call.complete(second_value)
        self.assertIs(await self.tasks.wait(second_task), second_value)
        self.assertIs(second.value, second_value)
        self.assertFalse(second.pending)
        self.assertIs(first.value, first_state[0])
        self.assertEqual(first.pending, first_state[1])
        self.assertIs(first.value, first_prior)
        self.assertIsNot(first_prior, second_prior)
        second_state = second.value, second.pending
        first_value = object()
        first_latest_call.complete(first_value)
        self.assertIs(await self.tasks.wait(first_latest), first_value)
        self.assertIs(first.value, first_value)
        self.assertFalse(first.pending)
        await self.assert_unsuccessful(first_task, first_call, False)
        self.assertIs(first.value, first_value)
        self.assertFalse(first.pending)
        self.assertIs(second.value, second_state[0])
        self.assertEqual(second.pending, second_state[1])


if __name__ == '__main__':
    unittest.main()
