import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def begin(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    async def seeded(self):
        preview = Preview()
        self.assert_state(preview, False, None)
        fetch = ControlledCall()
        task, call = await self.begin(preview, fetch, "seed")
        self.assert_state(preview, True, None)
        value = {"prior": []}
        call.complete(value)
        self.assertIs(await self.tasks.wait(task), value)
        self.assert_state(preview, False, value)
        return preview

    async def test_earlier_success_while_latest_pending(self):
        preview = await self.seeded()
        prior = preview.value
        fetch = ControlledCall()
        older, first = await self.begin(preview, fetch, "same-key")
        latest, second = await self.begin(preview, fetch, "same-key")
        self.assertEqual(len(fetch.calls), 2)
        self.assert_state(preview, True, prior)
        old_result, new_result = object(), object()
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertFalse(latest.done())
        self.assert_state(preview, True, prior)
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assert_state(preview, False, new_result)

    async def test_latest_success_before_earlier_success(self):
        preview = await self.seeded()
        prior = preview.value
        fetch = ControlledCall()
        older, first = await self.begin(preview, fetch, "older")
        latest, second = await self.begin(preview, fetch, "latest")
        self.assert_state(preview, True, prior)
        new_result = {"latest": []}
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assertFalse(older.done())
        self.assert_state(preview, False, new_result)
        pending, displayed = preview.pending, preview.value
        old_result = object()
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assert_state(preview, pending, displayed)

    async def settle_unsuccessfully(self, task, call, cancelled):
        if cancelled:
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

    async def earlier_unsuccessful(self, cancelled):
        preview = await self.seeded()
        fetch = ControlledCall()
        older, first = await self.begin(preview, fetch, "older")
        latest, second = await self.begin(preview, fetch, "latest")
        pending, displayed = preview.pending, preview.value
        self.assertIs(pending, True)
        await self.settle_unsuccessfully(older, first, cancelled)
        self.assertFalse(latest.done())
        self.assert_state(preview, pending, displayed)
        result = object()
        second.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_state(preview, False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancelled=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancelled=True)

    async def latest_unsuccessful_and_retry(self, cancelled):
        preview = await self.seeded()
        prior = preview.value
        fetch = ControlledCall()
        older, first = await self.begin(preview, fetch, "older")
        latest, second = await self.begin(preview, fetch, "latest")
        self.assert_state(preview, True, prior)
        await self.settle_unsuccessfully(latest, second, cancelled)
        self.assertFalse(older.done())
        self.assert_state(preview, False, prior)
        retry, third = await self.begin(preview, fetch, "latest")
        self.assertEqual(len(fetch.calls), 3)
        pending, displayed = preview.pending, preview.value
        self.assertIs(pending, True)
        stale_result = object()
        first.complete(stale_result)
        self.assertIs(await self.tasks.wait(older), stale_result)
        self.assertFalse(retry.done())
        self.assert_state(preview, pending, displayed)
        result = object()
        third.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_state(preview, False, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancelled=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancelled=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview = await self.seeded()
        prior = preview.value
        fetch = ControlledCall()
        older, first = await self.begin(preview, fetch, "older")
        error = ValueError("synchronous failure")
        keys = []

        def broken_fetch(key):
            keys.append(key)
            self.assert_state(preview, True, prior)
            raise error

        latest = self.tasks.start(preview.refresh("sync", broken_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(latest)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(older.done())
        self.assert_state(preview, False, prior)
        stale_result = object()
        first.complete(stale_result)
        self.assertIs(await self.tasks.wait(older), stale_result)
        self.assert_state(preview, False, prior)
        retry, next_call = await self.begin(preview, fetch, "sync")
        self.assert_state(preview, True, prior)
        result = object()
        next_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_state(preview, False, result)

    async def test_instance_isolation(self):
        left, right = await self.seeded(), await self.seeded()
        left_prior, right_prior = left.value, right.value
        left_fetch, right_fetch = ControlledCall(), ControlledCall()
        left_task, left_call = await self.begin(left, left_fetch, "same")
        right_task, right_call = await self.begin(right, right_fetch, "same")
        self.assert_state(left, True, left_prior)
        self.assert_state(right, True, right_prior)
        left_result = object()
        left_call.complete(left_result)
        self.assertIs(await self.tasks.wait(left_task), left_result)
        self.assert_state(left, False, left_result)
        self.assertFalse(right_task.done())
        self.assert_state(right, True, right_prior)
        await self.settle_unsuccessfully(right_task, right_call, cancelled=False)
        self.assert_state(right, False, right_prior)
        self.assert_state(left, False, left_result)


if __name__ == "__main__":
    unittest.main()
