import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewRefreshTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)
        self.preview = Preview()
        self.fetch = ControlledCall()
        self.assertIsNone(self.preview.value)
        self.assertIs(self.preview.pending, False)
        self.prior = await self.seed(self.preview)

    async def start_call(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    async def seed(self, preview):
        fetch = ControlledCall()
        value = object()
        task, call = await self.start_call(preview, fetch, 'seed')
        call.complete(value)
        self.assertIs(await self.tasks.wait(task), value)
        self.assert_state(preview, False, value)
        return value

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def settle(self, task, call, outcome):
        if outcome == 'success':
            value = object()
            call.complete(value)
            self.assertIs(await self.tasks.wait(task), value)
            return value
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
            self.assertTrue(task.cancelled())

    async def check_order(self, latest_first, earlier_outcome):
        # Identical keys must still enter two independent callback invocations.
        earlier, first_call = await self.start_call(self.preview, self.fetch, 'same')
        self.assert_state(self.preview, True, self.prior)
        latest, last_call = await self.start_call(self.preview, self.fetch, 'same')
        self.assertEqual(len(self.fetch.calls), 2)
        self.assertFalse(earlier.done())
        self.assert_state(self.preview, True, self.prior)
        if latest_first:
            value = await self.settle(latest, last_call, 'success')
            self.assertFalse(earlier.done())
            self.assert_state(self.preview, False, value)
            pending_before, value_before = self.preview.pending, self.preview.value
            await self.settle(earlier, first_call, earlier_outcome)
            self.assert_state(self.preview, pending_before, value_before)
        else:
            pending_before, value_before = self.preview.pending, self.preview.value
            await self.settle(earlier, first_call, earlier_outcome)
            self.assertFalse(latest.done())
            self.assert_state(self.preview, pending_before, value_before)
            value = await self.settle(latest, last_call, 'success')
            self.assert_state(self.preview, False, value)

    async def test_earlier_success_while_latest_pending(self):
        await self.check_order(False, 'success')

    async def test_earlier_failure_while_latest_pending(self):
        await self.check_order(False, 'failure')

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.check_order(False, 'cancellation')

    async def test_latest_success_before_earlier_success(self):
        await self.check_order(True, 'success')

    async def test_latest_success_before_earlier_failure(self):
        await self.check_order(True, 'failure')

    async def test_latest_success_before_earlier_cancellation(self):
        await self.check_order(True, 'cancellation')

    async def check_latest_failure_and_retry(self, outcome):
        earlier, first_call = await self.start_call(self.preview, self.fetch, 'old')
        latest, last_call = await self.start_call(self.preview, self.fetch, 'latest')
        self.assert_state(self.preview, True, self.prior)
        await self.settle(latest, last_call, outcome)
        self.assert_state(self.preview, False, self.prior)
        self.assertFalse(earlier.done())
        retry, retry_call = await self.start_call(self.preview, self.fetch, 'latest')
        self.assertEqual(len(self.fetch.calls), 3)
        self.assert_state(self.preview, True, self.prior)
        pending_before, value_before = self.preview.pending, self.preview.value
        await self.settle(earlier, first_call, 'success')
        self.assertFalse(retry.done())
        self.assert_state(self.preview, pending_before, value_before)
        value = await self.settle(retry, retry_call, 'success')
        self.assert_state(self.preview, False, value)

    async def test_latest_failure_and_retry(self):
        await self.check_latest_failure_and_retry('failure')

    async def test_latest_cancellation_and_retry(self):
        await self.check_latest_failure_and_retry('cancellation')

    async def test_synchronous_callback_failure_and_retry(self):
        earlier, first_call = await self.start_call(self.preview, self.fetch, 'old')
        error = ValueError('synchronous failure')
        keys = []

        def failing_fetch(key):
            keys.append(key)
            self.assert_state(self.preview, True, self.prior)
            raise error

        failed = self.tasks.start(self.preview.refresh('sync', failing_fetch))
        with self.assertRaises(ValueError) as raised:
            await self.tasks.wait(failed)
        self.assertIs(raised.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assert_state(self.preview, False, self.prior)
        self.assertFalse(earlier.done())
        retry, retry_call = await self.start_call(self.preview, self.fetch, 'retry')
        self.assert_state(self.preview, True, self.prior)
        value = await self.settle(retry, retry_call, 'success')
        self.assert_state(self.preview, False, value)
        pending_before, value_before = self.preview.pending, self.preview.value
        await self.settle(earlier, first_call, 'success')
        self.assert_state(self.preview, pending_before, value_before)

    async def test_instance_isolation(self):
        other = Preview()
        other_prior = await self.seed(other)
        first, first_call = await self.start_call(self.preview, self.fetch, 'same')
        second, second_call = await self.start_call(other, self.fetch, 'same')
        self.assert_state(self.preview, True, self.prior)
        self.assert_state(other, True, other_prior)
        other_pending, other_value = other.pending, other.value
        value = await self.settle(first, first_call, 'success')
        self.assert_state(self.preview, False, value)
        self.assertFalse(second.done())
        self.assert_state(other, other_pending, other_value)
        pending_before, value_before = self.preview.pending, self.preview.value
        await self.settle(second, second_call, 'failure')
        self.assert_state(other, False, other_prior)
        self.assert_state(self.preview, pending_before, value_before)
        retry, retry_call = await self.start_call(other, self.fetch, 'retry')
        self.assert_state(other, True, other_prior)
        self.assert_state(self.preview, pending_before, value_before)
        other_value = await self.settle(retry, retry_call, 'success')
        self.assert_state(other, False, other_value)
        self.assert_state(self.preview, pending_before, value_before)


if __name__ == '__main__':
    unittest.main()
