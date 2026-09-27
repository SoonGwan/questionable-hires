import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)
        self.preview = Preview()
        self.fetch = ControlledCall()
        self.prior = object()
        self.assertFalse(self.preview.pending)
        self.assertIsNone(self.preview.value)
        await self.succeed(self.prior)

    async def start_call(self, preview=None, key="same-key"):
        preview = self.preview if preview is None else preview
        task = self.tasks.start(preview.refresh(key, self.fetch))
        call = await self.fetch.started_before(task)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    async def succeed(self, value):
        task, call = await self.start_call()
        call.complete(value)
        self.assertIs(await self.tasks.wait(task), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def settle(self, task, call, outcome):
        if outcome == "success":
            value = object()
            call.complete(value)
            self.assertIs(await self.tasks.wait(task), value)
            return value
        if outcome == "failure":
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)

    async def earlier_settles_first(self, outcome):
        older, old_call = await self.start_call()
        latest, latest_call = await self.start_call()
        self.assertEqual(len(self.fetch.calls), 3)
        before_value = self.preview.value
        before_pending = self.preview.pending
        self.assertIs(before_value, self.prior)
        await self.settle(older, old_call, outcome)
        self.assertFalse(latest.done())
        self.assertIs(self.preview.value, before_value)
        self.assertEqual(self.preview.pending, before_pending)
        value = await self.settle(latest, latest_call, "success")
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_earlier_success_while_latest_pending(self):
        await self.earlier_settles_first("success")

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_settles_first("failure")

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_settles_first("cancellation")

    async def latest_settles_first(self, outcome):
        older, old_call = await self.start_call()
        latest, latest_call = await self.start_call()
        self.assertIs(self.preview.value, self.prior)
        result = await self.settle(latest, latest_call, outcome)
        self.assertFalse(older.done())
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result if outcome == "success" else self.prior)
        if outcome != "success":
            await self.succeed(object())
        before_value = self.preview.value
        before_pending = self.preview.pending
        await self.settle(older, old_call, "success")
        self.assertIs(self.preview.value, before_value)
        self.assertEqual(self.preview.pending, before_pending)

    async def test_latest_success_before_earlier_success(self):
        await self.latest_settles_first("success")

    async def test_latest_failure_and_retry(self):
        await self.latest_settles_first("failure")

    async def test_latest_cancellation_and_retry(self):
        await self.latest_settles_first("cancellation")

    async def test_synchronous_callback_failure_and_retry(self):
        older, old_call = await self.start_call()
        error = ValueError("synchronous failure")
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertTrue(self.preview.pending)
            self.assertIs(self.preview.value, self.prior)
            raise error

        task = self.tasks.start(self.preview.refresh("sync", raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        self.assertFalse(older.done())
        retry, retry_call = await self.start_call()
        before_value = self.preview.value
        before_pending = self.preview.pending
        await self.settle(older, old_call, "success")
        self.assertIs(self.preview.value, before_value)
        self.assertEqual(self.preview.pending, before_pending)
        value = await self.settle(retry, retry_call, "success")
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_instance_isolation(self):
        other = Preview()
        first, first_call = await self.start_call()
        second, second_call = await self.start_call(other)
        self.assertIsNone(other.value)
        value = await self.settle(first, first_call, "success")
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)
        self.assertTrue(other.pending)
        self.assertIsNone(other.value)
        other_value = await self.settle(second, second_call, "success")
        self.assertIs(other.value, other_value)
        self.assertFalse(other.pending)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)


if __name__ == "__main__":
    unittest.main()
