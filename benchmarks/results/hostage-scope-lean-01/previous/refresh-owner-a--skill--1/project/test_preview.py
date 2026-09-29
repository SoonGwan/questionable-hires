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
        self.assertFalse(self.preview.pending)
        self.assertIsNone(self.preview.value)
        self.prior = {"display": "prior"}
        task, call = await self.start_refresh()
        call.complete(self.prior)
        self.assertIs(await self.tasks.wait(task), self.prior)
        self.assert_state(False, self.prior)

    def assert_state(self, pending, value, preview=None):
        preview = self.preview if preview is None else preview
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def start_refresh(self, preview=None, fetch=None, key=None):
        preview = self.preview if preview is None else preview
        fetch = self.fetch if fetch is None else fetch
        key = object() if key is None else key
        count = len(fetch.calls)
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(len(fetch.calls), count + 1)
        self.assertIs(call.args[0], key)
        self.assertEqual(call.kwargs, {})
        return task, call

    async def overlapping(self):
        # Identical keys must still invoke both supplied callbacks immediately.
        key = object()
        old, old_call = await self.start_refresh(key=key)
        self.assert_state(True, self.prior)
        latest, latest_call = await self.start_refresh(
            key=key, fetch=ControlledCall())
        self.assertFalse(old.done())
        self.assertFalse(latest.done())
        self.assert_state(True, self.prior)
        return old, old_call, latest, latest_call

    async def test_earlier_success_while_latest_pending(self):
        old, old_call, latest, latest_call = await self.overlapping()
        before_pending, before_value = self.preview.pending, self.preview.value
        old_result, latest_result = {}, {}
        old_call.complete(old_result)
        self.assertIs(await self.tasks.wait(old), old_result)
        self.assertFalse(latest.done())
        self.assert_state(before_pending, before_value)
        latest_call.complete(latest_result)
        self.assertIs(await self.tasks.wait(latest), latest_result)
        self.assert_state(False, latest_result)

    async def test_latest_success_before_earlier_success(self):
        old, old_call, latest, latest_call = await self.overlapping()
        latest_result, old_result = {}, {}
        latest_call.complete(latest_result)
        self.assertIs(await self.tasks.wait(latest), latest_result)
        self.assertFalse(old.done())
        self.assert_state(False, latest_result)
        before_pending, before_value = self.preview.pending, self.preview.value
        old_call.complete(old_result)
        self.assertIs(await self.tasks.wait(old), old_result)
        self.assert_state(before_pending, before_value)

    async def settle_unsuccessfully(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def earlier_unsuccessful(self, cancel):
        old, old_call, latest, latest_call = await self.overlapping()
        before_pending, before_value = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(old, old_call, cancel)
        self.assertFalse(latest.done())
        self.assert_state(before_pending, before_value)
        result = {}
        latest_call.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assert_state(False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        old, old_call, latest, latest_call = await self.overlapping()
        before_value = self.preview.value
        await self.settle_unsuccessfully(latest, latest_call, cancel)
        self.assertFalse(old.done())
        self.assert_state(False, before_value)
        retry, retry_call = await self.start_refresh()
        self.assert_state(True, before_value)
        before_pending = self.preview.pending
        old_result = {}
        old_call.complete(old_result)
        self.assertIs(await self.tasks.wait(old), old_result)
        self.assert_state(before_pending, before_value)
        result = {}
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_state(False, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        old, old_call = await self.start_refresh()
        key, error = object(), RuntimeError("synchronous failure")
        calls = []

        def raising_fetch(actual_key):
            calls.append(actual_key)
            self.assert_state(True, self.prior)
            raise error

        task = self.tasks.start(self.preview.refresh(key, raising_fetch))
        with self.assertRaises(RuntimeError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0], key)
        self.assertFalse(old.done())
        self.assert_state(False, self.prior)
        before_pending, before_value = self.preview.pending, self.preview.value
        old_result = {}
        old_call.complete(old_result)
        self.assertIs(await self.tasks.wait(old), old_result)
        self.assert_state(before_pending, before_value)
        retry, retry_call = await self.start_refresh()
        self.assert_state(True, self.prior)
        result = {}
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assert_state(False, result)

    async def test_instance_isolation(self):
        other = Preview()
        other_fetch = ControlledCall()
        task, call = await self.start_refresh()
        other_task, other_call = await self.start_refresh(other, other_fetch)
        self.assert_state(True, self.prior)
        self.assert_state(True, None, other)
        before_pending, before_value = other.pending, other.value
        result = {}
        call.complete(result)
        self.assertIs(await self.tasks.wait(task), result)
        self.assert_state(False, result)
        self.assertFalse(other_task.done())
        self.assert_state(before_pending, before_value, other)
        next_task, next_call = await self.start_refresh()
        other_result = {}
        other_call.complete(other_result)
        self.assertIs(await self.tasks.wait(other_task), other_result)
        self.assert_state(False, other_result, other)
        self.assertFalse(next_task.done())
        self.assert_state(True, result)
        next_result = {}
        next_call.complete(next_result)
        self.assertIs(await self.tasks.wait(next_task), next_result)
        self.assert_state(False, next_result)
        self.assert_state(False, other_result, other)


if __name__ == "__main__":
    unittest.main()
