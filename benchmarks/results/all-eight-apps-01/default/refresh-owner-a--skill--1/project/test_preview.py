import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)
        self.preview = Preview()
        self.assertIsNone(self.preview.value)
        self.assertIs(self.preview.pending, False)
        self.prior = object()
        task, call = await self.begin(self.preview, ControlledCall(), "seed")
        call.complete(self.prior)
        self.assertIs(await self.tasks.wait(task), self.prior)
        self.assertState(self.preview, False, self.prior)

    def assertState(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def begin(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    async def overlap(self):
        fetch = ControlledCall()
        older, first = await self.begin(self.preview, fetch, "same-key")
        latest, second = await self.begin(self.preview, fetch, "same-key")
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertFalse(latest.done())
        self.assertState(self.preview, True, self.prior)
        return older, first, latest, second

    async def settle_unsuccessfully(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def test_earlier_success_then_latest_success(self):
        older, first, latest, second = await self.overlap()
        pending, value = self.preview.pending, self.preview.value
        old_result, new_result = object(), object()
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertFalse(latest.done())
        self.assertState(self.preview, pending, value)
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assertState(self.preview, False, new_result)

    async def test_latest_success_then_earlier_success(self):
        older, first, latest, second = await self.overlap()
        new_result, old_result = object(), object()
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assertFalse(older.done())
        self.assertState(self.preview, False, new_result)
        pending, value = self.preview.pending, self.preview.value
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertState(self.preview, pending, value)

    async def earlier_unsuccessful(self, cancel):
        older, first, latest, second = await self.overlap()
        pending, value = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(older, first, cancel)
        self.assertFalse(latest.done())
        self.assertState(self.preview, pending, value)
        result = object()
        second.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assertState(self.preview, False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        older, first, latest, second = await self.overlap()
        value = self.preview.value
        await self.settle_unsuccessfully(latest, second, cancel)
        self.assertState(self.preview, False, value)
        self.assertFalse(older.done())
        retry, third = await self.begin(self.preview, ControlledCall(), "retry")
        self.assertState(self.preview, True, value)
        pending, value = self.preview.pending, self.preview.value
        old_result = object()
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertFalse(retry.done())
        self.assertState(self.preview, pending, value)
        result = object()
        third.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assertState(self.preview, False, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        older, first = await self.begin(self.preview, ControlledCall(), "older")
        error = ValueError("synchronous fetch failure")
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertState(self.preview, True, self.prior)
            raise error

        failed = self.tasks.start(self.preview.refresh("sync", raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertState(self.preview, False, self.prior)
        self.assertFalse(older.done())
        pending, value = self.preview.pending, self.preview.value
        first.complete(None)
        self.assertIsNone(await self.tasks.wait(older))
        self.assertState(self.preview, pending, value)
        retry, call = await self.begin(self.preview, ControlledCall(), "retry")
        self.assertState(self.preview, True, self.prior)
        call.complete(None)
        self.assertIsNone(await self.tasks.wait(retry))
        self.assertState(self.preview, False, None)

    async def test_instances_are_independent(self):
        other = Preview()
        fetch = ControlledCall()
        first, call_one = await self.begin(self.preview, fetch, "one")
        pending, value = self.preview.pending, self.preview.value
        second, call_two = await self.begin(other, fetch, "two")
        self.assertState(self.preview, pending, value)
        self.assertState(other, True, None)
        result_one, result_two = object(), object()
        call_one.complete(result_one)
        self.assertIs(await self.tasks.wait(first), result_one)
        self.assertState(self.preview, False, result_one)
        self.assertFalse(second.done())
        self.assertState(other, True, None)
        pending, value = self.preview.pending, self.preview.value
        call_two.complete(result_two)
        self.assertIs(await self.tasks.wait(second), result_two)
        self.assertState(other, False, result_two)
        self.assertState(self.preview, pending, value)


if __name__ == "__main__":
    unittest.main()
