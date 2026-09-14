import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.drain_tasks)
        self.preview = Preview()
        self.assertFalse(self.preview.pending)
        self.assertIsNone(self.preview.value)
        self.prior = object()

        async def initial_fetch(key):
            return self.prior

        result = await asyncio.wait_for(
            self.preview.refresh("initial", initial_fetch), 1
        )
        self.assertIs(result, self.prior)
        self.assert_state(self.preview, False, self.prior)

    async def drain_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), 1
            )

    def own(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.tasks.append(task)
        return task

    async def start(self, preview, fetch, key="same-key"):
        task = self.own(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def overlap(self):
        fetch = ControlledCall()
        older, old_call = await self.start(self.preview, fetch)
        latest, latest_call = await self.start(self.preview, fetch)
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assert_state(self.preview, True, self.prior)
        return older, old_call, latest, latest_call

    async def settle_unsuccessfully(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("controlled failure")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(task)
            self.assertIs(caught.exception, error)

    async def test_older_success_then_latest_success(self):
        older, old_call, latest, latest_call = await self.overlap()
        pending, value = self.preview.pending, self.preview.value
        old_result = object()
        old_call.complete(old_result)
        self.assertIs(await self.result(older), old_result)
        self.assert_state(self.preview, pending, value)
        self.assertFalse(latest.done())
        latest_result = object()
        latest_call.complete(latest_result)
        self.assertIs(await self.result(latest), latest_result)
        self.assert_state(self.preview, False, latest_result)

    async def test_latest_success_then_older_success(self):
        older, old_call, latest, latest_call = await self.overlap()
        latest_result = object()
        latest_call.complete(latest_result)
        self.assertIs(await self.result(latest), latest_result)
        self.assert_state(self.preview, False, latest_result)
        self.assertFalse(older.done())
        pending, value = self.preview.pending, self.preview.value
        old_result = object()
        old_call.complete(old_result)
        self.assertIs(await self.result(older), old_result)
        self.assert_state(self.preview, pending, value)

    async def earlier_unsuccessful(self, cancelled):
        older, old_call, latest, latest_call = await self.overlap()
        pending, value = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(older, old_call, cancelled)
        self.assert_state(self.preview, pending, value)
        self.assertFalse(latest.done())
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.result(latest), result)
        self.assert_state(self.preview, False, result)

    async def test_earlier_failure_keeps_latest_pending(self):
        await self.earlier_unsuccessful(cancelled=False)

    async def test_earlier_cancellation_keeps_latest_pending(self):
        await self.earlier_unsuccessful(cancelled=True)

    async def latest_unsuccessful_and_retry(self, cancelled):
        older, old_call, latest, latest_call = await self.overlap()
        value = self.preview.value
        await self.settle_unsuccessfully(latest, latest_call, cancelled)
        self.assert_state(self.preview, False, value)
        self.assertFalse(older.done())
        retry_fetch = ControlledCall()
        retry, retry_call = await self.start(self.preview, retry_fetch)
        self.assert_state(self.preview, True, value)
        pending, value = self.preview.pending, self.preview.value
        old_result = object()
        old_call.complete(old_result)
        self.assertIs(await self.result(older), old_result)
        self.assert_state(self.preview, pending, value)
        self.assertFalse(retry.done())
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.result(retry), result)
        self.assert_state(self.preview, False, result)
        self.assertEqual(len(retry_fetch.calls), 1)

    async def test_latest_failure_clears_pending_and_allows_retry(self):
        await self.latest_unsuccessful_and_retry(cancelled=False)

    async def test_latest_cancellation_clears_pending_and_allows_retry(self):
        await self.latest_unsuccessful_and_retry(cancelled=True)

    async def test_synchronous_callback_failure_and_retry(self):
        fetch = ControlledCall()
        older, old_call = await self.start(self.preview, fetch)
        error = ValueError("synchronous failure")
        keys = []

        def fail(key):
            keys.append(key)
            raise error

        value = self.preview.value
        failed = self.own(self.preview.refresh("sync-key", fail))
        with self.assertRaises(ValueError) as caught:
            await self.result(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync-key"])
        self.assert_state(self.preview, False, value)
        self.assertFalse(older.done())
        retry, retry_call = await self.start(self.preview, fetch)
        self.assert_state(self.preview, True, value)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.result(retry), result)
        self.assert_state(self.preview, False, result)
        pending, value = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(older, old_call, cancelled=False)
        self.assert_state(self.preview, pending, value)
        self.assertEqual(len(fetch.calls), 2)

    async def test_instances_are_independent(self):
        other = Preview()
        other_fetch = ControlledCall()
        other_task, other_call = await self.start(other, other_fetch)
        self.assert_state(other, True, None)
        self.assert_state(self.preview, False, self.prior)
        other_pending, other_value = other.pending, other.value
        older, old_call, latest, latest_call = await self.overlap()
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.result(latest), result)
        self.assert_state(self.preview, False, result)
        self.assert_state(other, other_pending, other_value)
        self.assertFalse(other_task.done())
        pending, value = self.preview.pending, self.preview.value
        other_result = object()
        other_call.complete(other_result)
        self.assertIs(await self.result(other_task), other_result)
        self.assert_state(other, False, other_result)
        self.assert_state(self.preview, pending, value)
        other_pending, other_value = other.pending, other.value
        await self.settle_unsuccessfully(older, old_call, cancelled=True)
        self.assert_state(self.preview, pending, value)
        self.assert_state(other, other_pending, other_value)


if __name__ == "__main__":
    unittest.main()
