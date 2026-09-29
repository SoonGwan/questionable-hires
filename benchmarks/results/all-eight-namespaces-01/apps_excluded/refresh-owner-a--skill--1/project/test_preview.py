import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def begin(self, preview, fetch, key="same-key"):
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
        fetch = ControlledCall()
        task, call = await self.begin(preview, fetch)
        prior = object()
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def settle(self, task, call, outcome):
        if outcome == "cancel":
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        elif outcome == "failure":
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)
        else:
            result = object()
            call.complete(result)
            self.assertIs(await self.tasks.wait(task), result)
            return result

    async def earlier_settles_first(self, outcome):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, old_call = await self.begin(preview, fetch)
        latest, new_call = await self.begin(preview, fetch)
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertIs(preview.value, prior)
        before_pending, before_value = preview.pending, preview.value
        await self.settle(older, old_call, outcome)
        self.assertFalse(latest.done())
        self.assertEqual(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        result = await self.settle(latest, new_call, "success")
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, result)

    async def test_earlier_success_while_latest_pending(self):
        await self.earlier_settles_first("success")

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_settles_first("failure")

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_settles_first("cancel")

    async def test_latest_success_before_earlier_settlement(self):
        for outcome in ("success", "failure", "cancel"):
            with self.subTest(earlier_outcome=outcome):
                preview, prior = await self.seeded()
                fetch = ControlledCall()
                older, old_call = await self.begin(preview, fetch, "old")
                latest, new_call = await self.begin(preview, fetch, "new")
                self.assertIs(preview.value, prior)
                result = await self.settle(latest, new_call, "success")
                self.assertFalse(older.done())
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, result)
                before_pending, before_value = preview.pending, preview.value
                await self.settle(older, old_call, outcome)
                self.assertEqual(preview.pending, before_pending)
                self.assertIs(preview.value, before_value)

    async def latest_unsuccessful_and_retry(self, outcome):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, old_call = await self.begin(preview, fetch)
        latest, new_call = await self.begin(preview, fetch)
        await self.settle(latest, new_call, outcome)
        self.assertFalse(older.done())
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        retry, retry_call = await self.begin(preview, fetch)
        self.assertEqual(len(fetch.calls), 3)
        self.assertIs(preview.value, prior)
        before_pending, before_value = preview.pending, preview.value
        await self.settle(older, old_call, "success")
        self.assertFalse(retry.done())
        self.assertEqual(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        result = await self.settle(retry, retry_call, "success")
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry("failure")

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry("cancel")

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, old_call = await self.begin(preview, fetch)
        error = ValueError("synchronous failure")
        keys = []

        def raise_synchronously(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        latest = self.tasks.start(preview.refresh("sync", raise_synchronously))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(latest)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        before_pending, before_value = preview.pending, preview.value
        await self.settle(older, old_call, "success")
        self.assertEqual(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        retry, retry_call = await self.begin(preview, fetch)
        result = await self.settle(retry, retry_call, "success")
        self.assertIs(preview.value, result)
        self.assertFalse(preview.pending)

    async def test_instance_isolation(self):
        left, left_prior = await self.seeded()
        right, right_prior = await self.seeded()
        left_fetch, right_fetch = ControlledCall(), ControlledCall()
        left_task, left_call = await self.begin(left, left_fetch)
        right_task, right_call = await self.begin(right, right_fetch)
        self.assertIs(left.value, left_prior)
        self.assertIs(right.value, right_prior)
        right_pending, right_value = right.pending, right.value
        left_result = await self.settle(left_task, left_call, "success")
        self.assertFalse(left.pending)
        self.assertIs(left.value, left_result)
        self.assertFalse(right_task.done())
        self.assertEqual(right.pending, right_pending)
        self.assertIs(right.value, right_value)
        left_pending, left_value = left.pending, left.value
        right_result = await self.settle(right_task, right_call, "success")
        self.assertFalse(right.pending)
        self.assertIs(right.value, right_result)
        self.assertEqual(left.pending, left_pending)
        self.assertIs(left.value, left_value)
