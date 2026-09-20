import asyncio
import unittest

from preview import Preview
from test_support import ControlledCall, OwnedTasks


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

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def overlapping_refreshes(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        older, first = await self.start_refresh(preview, fetch, 'same-key')
        self.assert_state(preview, True, prior)
        latest, second = await self.start_refresh(preview, fetch, 'same-key')
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertFalse(latest.done())
        self.assert_state(preview, True, prior)
        return preview, prior, fetch, older, first, latest, second

    async def test_earlier_success_while_latest_pending(self):
        preview, prior, _, older, first, latest, second = await self.overlapping_refreshes()
        pending_before, value_before = preview.pending, preview.value
        old_result = {'result': 'older'}
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertFalse(latest.done())
        self.assert_state(preview, pending_before, value_before)
        new_result = {'result': 'latest'}
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assert_state(preview, False, new_result)
        self.assertEqual(prior, {'display': ['prior']})

    async def test_latest_success_before_earlier_success(self):
        preview, _, _, older, first, latest, second = await self.overlapping_refreshes()
        new_result = {'result': 'latest'}
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assertFalse(older.done())
        self.assert_state(preview, False, new_result)
        pending_before, value_before = preview.pending, preview.value
        old_result = {'result': 'older'}
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assert_state(preview, pending_before, value_before)

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

    async def earlier_unsuccessful(self, cancel):
        preview, _, _, older, first, latest, second = await self.overlapping_refreshes()
        pending_before, value_before = preview.pending, preview.value
        await self.settle_unsuccessfully(older, first, cancel)
        self.assertFalse(latest.done())
        self.assert_state(preview, pending_before, value_before)
        result = object()
        second.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_state(preview, False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        preview, prior, fetch, older, first, latest, second = await self.overlapping_refreshes()
        value_before = preview.value
        await self.settle_unsuccessfully(latest, second, cancel)
        self.assertFalse(older.done())
        self.assert_state(preview, False, value_before)
        retry, third = await self.start_refresh(preview, fetch, 'same-key')
        self.assertEqual(len(fetch.calls), 3)
        self.assert_state(preview, True, prior)
        pending_before, value_before = preview.pending, preview.value
        old_result = object()
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertFalse(retry.done())
        self.assert_state(preview, pending_before, value_before)
        result = object()
        third.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_state(preview, False, result)
        self.assertEqual(prior, {'display': ['prior']})

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        older, first = await self.start_refresh(preview, fetch, 'older')
        error = ValueError('synchronous failure')
        entries = []

        def synchronous_failure(key):
            entries.append(key)
            self.assert_state(preview, True, prior)
            raise error

        latest = self.tasks.start(preview.refresh('sync', synchronous_failure))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(latest)
        self.assertIs(caught.exception, error)
        self.assertEqual(entries, ['sync'])
        self.assertFalse(older.done())
        self.assert_state(preview, False, prior)
        retry, second = await self.start_refresh(preview, fetch, 'retry')
        self.assert_state(preview, True, prior)
        result = object()
        second.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_state(preview, False, result)
        pending_before, value_before = preview.pending, preview.value
        await self.settle_unsuccessfully(older, first, cancel=False)
        self.assert_state(preview, pending_before, value_before)

    async def test_instances_are_independent(self):
        left, left_prior = await self.seeded_preview()
        right, right_prior = await self.seeded_preview()
        fetch = ControlledCall()
        left_task, left_call = await self.start_refresh(left, fetch, 'same-key')
        right_task, right_call = await self.start_refresh(right, fetch, 'same-key')
        right_pending, right_value = right.pending, right.value
        left_result = object()
        left_call.complete(left_result)
        self.assertIs(await self.tasks.wait(left_task), left_result)
        self.assert_state(left, False, left_result)
        self.assertFalse(right_task.done())
        self.assert_state(right, right_pending, right_value)
        left_pending, left_value = left.pending, left.value
        await self.settle_unsuccessfully(right_task, right_call, cancel=False)
        self.assert_state(right, False, right_prior)
        self.assert_state(left, left_pending, left_value)
        retry, retry_call = await self.start_refresh(right, fetch, 'retry')
        self.assert_state(right, True, right_prior)
        self.assert_state(left, left_pending, left_value)
        right_result = object()
        retry_call.complete(right_result)
        self.assertIs(await self.tasks.wait(retry), right_result)
        self.assert_state(right, False, right_result)
        self.assert_state(left, left_pending, left_value)
        self.assertEqual(left_prior, {'display': ['prior']})


if __name__ == '__main__':
    unittest.main()
