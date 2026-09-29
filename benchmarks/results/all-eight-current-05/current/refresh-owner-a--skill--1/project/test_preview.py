import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewRefreshTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)
        self.preview = Preview()
        self.prior = object()
        task, call = await self.start_refresh(self.preview, ControlledCall(), 'seed')
        call.complete(self.prior)
        self.assertIs(await self.tasks.wait(task), self.prior)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)

    async def start_refresh(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        self.assertFalse(task.done())
        return task, call

    async def overlapping(self):
        fetch = ControlledCall()
        older = await self.start_refresh(self.preview, fetch, 'same-key')
        latest = await self.start_refresh(self.preview, fetch, 'same-key')
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older[0].done())
        self.assertIs(self.preview.value, self.prior)
        return older, latest

    async def settle(self, task, call, outcome, payload):
        if outcome == 'success':
            call.complete(payload)
            self.assertIs(await self.tasks.wait(task), payload)
        elif outcome == 'failure':
            call.fail(payload)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, payload)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)

    async def earlier_settles_first(self, outcome):
        (older, old_call), (latest, new_call) = await self.overlapping()
        pending_before, value_before = self.preview.pending, self.preview.value
        payload = RuntimeError('earlier failure') if outcome == 'failure' else object()
        await self.settle(older, old_call, outcome, payload)
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(latest.done())
        result = object()
        await self.settle(latest, new_call, 'success', result)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)

    async def test_earlier_success_while_latest_pending(self):
        await self.earlier_settles_first('success')

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_settles_first('failure')

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_settles_first('cancellation')

    async def test_latest_success_before_earlier_success(self):
        (older, old_call), (latest, new_call) = await self.overlapping()
        result = object()
        await self.settle(latest, new_call, 'success', result)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)
        self.assertFalse(older.done())
        pending_before, value_before = self.preview.pending, self.preview.value
        await self.settle(older, old_call, 'success', object())
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)

    async def latest_unsuccessful_then_retry(self, outcome):
        (older, old_call), (latest, new_call) = await self.overlapping()
        value_before = self.preview.value
        await self.settle(latest, new_call, outcome, RuntimeError('latest failure'))
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(older.done())
        retry, retry_call = await self.start_refresh(self.preview, ControlledCall(), 'retry')
        pending_before, value_before = self.preview.pending, self.preview.value
        await self.settle(older, old_call, 'success', object())
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(retry.done())
        result = object()
        await self.settle(retry, retry_call, 'success', result)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_then_retry('failure')

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_then_retry('cancellation')

    async def test_synchronous_callback_failure_and_retry(self):
        older, old_call = await self.start_refresh(self.preview, ControlledCall(), 'older')
        error = RuntimeError('synchronous failure')
        keys = []

        def raising_fetch(key):
            keys.append(key)
            raise error

        value_before = self.preview.value
        task = self.tasks.start(self.preview.refresh('sync', raising_fetch))
        with self.assertRaises(RuntimeError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(older.done())
        retry, retry_call = await self.start_refresh(self.preview, ControlledCall(), 'retry')
        self.assertIs(self.preview.value, value_before)
        result = object()
        await self.settle(retry, retry_call, 'success', result)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)
        pending_before, value_before = self.preview.pending, self.preview.value
        await self.settle(older, old_call, 'failure', RuntimeError('stale failure'))
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)

    async def test_instance_isolation(self):
        other = Preview()
        self.assertFalse(other.pending)
        self.assertIsNone(other.value)
        first, first_call = await self.start_refresh(self.preview, ControlledCall(), 'first')
        second, second_call = await self.start_refresh(other, ControlledCall(), 'second')
        first_pending, first_value = self.preview.pending, self.preview.value
        second_result = object()
        await self.settle(second, second_call, 'success', second_result)
        self.assertFalse(other.pending)
        self.assertIs(other.value, second_result)
        self.assertEqual(self.preview.pending, first_pending)
        self.assertIs(self.preview.value, first_value)
        self.assertFalse(first.done())
        other_pending, other_value = other.pending, other.value
        first_result = object()
        await self.settle(first, first_call, 'success', first_result)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, first_result)
        self.assertEqual(other.pending, other_pending)
        self.assertIs(other.value, other_value)


if __name__ == '__main__':
    unittest.main()
