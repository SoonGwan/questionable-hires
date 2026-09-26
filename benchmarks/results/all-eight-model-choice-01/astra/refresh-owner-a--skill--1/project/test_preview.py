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
        self.prior = {"display": "prior"}
        task, call = await self.start_refresh(self.preview, "seed", self.fetch)
        call.complete(self.prior)
        self.assertIs(await self.tasks.wait(task), self.prior)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)

    async def start_refresh(self, preview, key, fetch):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    async def overlap(self):
        # Identical keys must still enter both supplied callbacks independently.
        old = await self.start_refresh(self.preview, "same", self.fetch)
        latest_fetch = ControlledCall()
        latest = await self.start_refresh(self.preview, "same", latest_fetch)
        self.assertEqual(len(self.fetch.calls), 2)  # seed and old
        self.assertEqual(len(latest_fetch.calls), 1)
        self.assertFalse(old[0].done())
        self.assertFalse(latest[0].done())
        self.assertIs(self.preview.value, self.prior)
        return old, latest

    async def settle(self, task, call, outcome):
        if outcome == "success":
            payload = {"payload": object()}
            call.complete(payload)
            self.assertIs(await self.tasks.wait(task), payload)
            return payload
        if outcome == "failure":
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as raised:
                await self.tasks.wait(task)
            self.assertIs(raised.exception, error)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
            self.assertTrue(task.cancelled())

    async def earlier_settles_first(self, outcome):
        old, latest = await self.overlap()
        pending_before = self.preview.pending
        value_before = self.preview.value
        await self.settle(*old, outcome)
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(latest[0].done())
        result = await self.settle(*latest, "success")
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)

    async def test_earlier_success_while_latest_pending(self):
        await self.earlier_settles_first("success")

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_settles_first("failure")

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_settles_first("cancellation")

    async def test_latest_success_before_earlier_success(self):
        old, latest = await self.overlap()
        result = await self.settle(*latest, "success")
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)
        self.assertFalse(old[0].done())
        pending_before = self.preview.pending
        value_before = self.preview.value
        await self.settle(*old, "success")
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)

    async def latest_unsuccessful_and_retry(self, outcome):
        old, latest = await self.overlap()
        value_before = self.preview.value
        await self.settle(*latest, outcome)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(old[0].done())
        retry = await self.start_refresh(self.preview, "retry", self.fetch)
        self.assertIs(self.preview.value, value_before)
        pending_before = self.preview.pending
        await self.settle(*old, "success")
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)
        result = await self.settle(*retry, "success")
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry("failure")

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry("cancellation")

    async def test_synchronous_callback_failure_and_retry(self):
        old = await self.start_refresh(self.preview, "old", self.fetch)
        error = ValueError("synchronous failure")
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertTrue(self.preview.pending)
            raise error

        value_before = self.preview.value
        task = self.tasks.start(self.preview.refresh("sync", raising_fetch))
        with self.assertRaises(ValueError) as raised:
            await self.tasks.wait(task)
        self.assertIs(raised.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, value_before)
        self.assertFalse(old[0].done())
        pending_before = self.preview.pending
        await self.settle(*old, "success")
        self.assertEqual(self.preview.pending, pending_before)
        self.assertIs(self.preview.value, value_before)
        retry = await self.start_refresh(self.preview, "retry", self.fetch)
        self.assertIs(self.preview.value, value_before)
        result = await self.settle(*retry, "success")
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, result)

    async def test_instance_isolation(self):
        other = Preview()
        self.assertFalse(other.pending)
        self.assertIsNone(other.value)
        first = await self.start_refresh(self.preview, "first", self.fetch)
        second = await self.start_refresh(other, "second", self.fetch)
        first_pending = self.preview.pending
        first_value = self.preview.value
        second_value = await self.settle(*second, "success")
        self.assertFalse(other.pending)
        self.assertIs(other.value, second_value)
        self.assertEqual(self.preview.pending, first_pending)
        self.assertIs(self.preview.value, first_value)
        self.assertFalse(first[0].done())
        other_pending = other.pending
        other_value = other.value
        first_value = await self.settle(*first, "success")
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, first_value)
        self.assertEqual(other.pending, other_pending)
        self.assertIs(other.value, other_value)


if __name__ == "__main__":
    unittest.main()
