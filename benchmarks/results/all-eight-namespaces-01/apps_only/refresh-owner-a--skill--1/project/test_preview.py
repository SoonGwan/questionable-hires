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

    async def begin(self, preview=None, fetch=None, key="same-key"):
        preview = self.preview if preview is None else preview
        fetch = self.fetch if fetch is None else fetch
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        self.assertFalse(task.done())
        return task, call

    async def seed(self, preview=None):
        preview = self.preview if preview is None else preview
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        task, call = await self.begin(preview)
        value = {"prior": []}
        call.complete(value)
        self.assertIs(await self.tasks.wait(task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)
        return value

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def settle_error(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError("controlled failure")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def test_earlier_success_while_latest_pending(self):
        prior = await self.seed()
        earlier, first = await self.begin()
        latest, second = await self.begin()
        self.assertEqual(len(self.fetch.calls), 3)
        pending, displayed = self.preview.pending, self.preview.value
        self.assertIs(displayed, prior)
        first_value, second_value = {}, {}
        first.complete(first_value)
        self.assertIs(await self.tasks.wait(earlier), first_value)
        self.assert_state(self.preview, pending, displayed)
        self.assertFalse(latest.done())
        second.complete(second_value)
        self.assertIs(await self.tasks.wait(latest), second_value)
        self.assert_state(self.preview, False, second_value)

    async def test_latest_success_before_earlier_success(self):
        prior = await self.seed()
        earlier, first = await self.begin()
        latest, second = await self.begin()
        self.assert_state(self.preview, True, prior)
        first_value, second_value = {}, {}
        second.complete(second_value)
        self.assertIs(await self.tasks.wait(latest), second_value)
        self.assert_state(self.preview, False, second_value)
        self.assertFalse(earlier.done())
        pending, displayed = self.preview.pending, self.preview.value
        first.complete(first_value)
        self.assertIs(await self.tasks.wait(earlier), first_value)
        self.assert_state(self.preview, pending, displayed)

    async def earlier_error(self, cancel):
        prior = await self.seed()
        earlier, first = await self.begin()
        latest, second = await self.begin()
        pending, displayed = self.preview.pending, self.preview.value
        self.assertIs(displayed, prior)
        await self.settle_error(earlier, first, cancel)
        self.assert_state(self.preview, pending, displayed)
        self.assertFalse(latest.done())
        value = object()
        second.complete(value)
        self.assertIs(await self.tasks.wait(latest), value)
        self.assert_state(self.preview, False, value)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_error(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_error(cancel=True)

    async def latest_error_and_retry(self, cancel):
        prior = await self.seed()
        earlier, first = await self.begin()
        latest, second = await self.begin()
        self.assert_state(self.preview, True, prior)
        await self.settle_error(latest, second, cancel)
        self.assert_state(self.preview, False, prior)
        self.assertFalse(earlier.done())
        retry, third = await self.begin()
        pending, displayed = self.preview.pending, self.preview.value
        self.assertIs(displayed, prior)
        stale_value = object()
        first.complete(stale_value)
        self.assertIs(await self.tasks.wait(earlier), stale_value)
        self.assert_state(self.preview, pending, displayed)
        self.assertFalse(retry.done())
        value = object()
        third.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assert_state(self.preview, False, value)

    async def test_latest_failure_and_retry(self):
        await self.latest_error_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_error_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        prior = await self.seed()
        earlier, first = await self.begin()
        error = ValueError("synchronous failure")
        keys = []

        def raise_immediately(key):
            keys.append(key)
            self.assert_state(self.preview, True, prior)
            raise error

        failed = self.tasks.start(self.preview.refresh("sync", raise_immediately))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assert_state(self.preview, False, prior)
        self.assertFalse(earlier.done())
        pending, displayed = self.preview.pending, self.preview.value
        first.complete(None)
        self.assertIsNone(await self.tasks.wait(earlier))
        self.assert_state(self.preview, pending, displayed)
        retry, call = await self.begin()
        self.assertIs(self.preview.value, prior)
        value = object()
        call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assert_state(self.preview, False, value)

    async def test_instances_are_independent(self):
        other = Preview()
        prior = await self.seed()
        other_prior = await self.seed(other)
        first_task, first = await self.begin()
        other_task, second = await self.begin(other)
        self.assert_state(self.preview, True, prior)
        self.assert_state(other, True, other_prior)
        other_pending, other_displayed = other.pending, other.value
        value = object()
        first.complete(value)
        self.assertIs(await self.tasks.wait(first_task), value)
        self.assert_state(self.preview, False, value)
        self.assert_state(other, other_pending, other_displayed)
        self.assertFalse(other_task.done())
        pending, displayed = self.preview.pending, self.preview.value
        await self.settle_error(other_task, second, cancel=False)
        self.assert_state(other, False, other_prior)
        self.assert_state(self.preview, pending, displayed)


if __name__ == "__main__":
    unittest.main()
