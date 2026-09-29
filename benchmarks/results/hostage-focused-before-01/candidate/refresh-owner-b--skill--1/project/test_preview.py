import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)
        self.preview = Preview()
        self.assertFalse(self.preview.pending)
        self.assertIsNone(self.preview.value)
        self.prior = object()
        task, call = await self.begin(self.preview)
        call.complete(self.prior)
        self.assertIs(await self.tasks.wait(task), self.prior)
        self.assert_state(self.preview, False, self.prior)

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def begin(self, preview, fetch=None, key="same-key"):
        if fetch is None:
            fetch = ControlledCall()
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    async def overlapping(self):
        fetch = ControlledCall()
        older, first = await self.begin(self.preview, fetch)
        self.assert_state(self.preview, True, self.prior)
        latest, second = await self.begin(self.preview, fetch)
        self.assertEqual(len(fetch.calls), 2)
        self.assertIsNot(first, second)
        self.assertFalse(older.done())
        self.assert_state(self.preview, True, self.prior)
        return older, first, latest, second

    async def check_success_order(self, latest_first):
        older, first, latest, second = await self.overlapping()
        old_value, new_value = object(), object()
        if latest_first:
            second.complete(new_value)
            self.assertIs(await self.tasks.wait(latest), new_value)
            self.assertFalse(older.done())
            self.assert_state(self.preview, False, new_value)
            pending, displayed = self.preview.pending, self.preview.value
            first.complete(old_value)
            self.assertIs(await self.tasks.wait(older), old_value)
            self.assert_state(self.preview, pending, displayed)
        else:
            pending, displayed = self.preview.pending, self.preview.value
            first.complete(old_value)
            self.assertIs(await self.tasks.wait(older), old_value)
            self.assertFalse(latest.done())
            self.assert_state(self.preview, pending, displayed)
            second.complete(new_value)
            self.assertIs(await self.tasks.wait(latest), new_value)
            self.assert_state(self.preview, False, new_value)

    async def test_older_success_before_latest(self):
        await self.check_success_order(latest_first=False)

    async def test_latest_success_before_older(self):
        await self.check_success_order(latest_first=True)

    async def settle_unsuccessfully(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError("controlled failure")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def check_earlier_unsuccessful(self, cancelled):
        older, first, latest, second = await self.overlapping()
        pending, displayed = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(older, first, cancelled)
        self.assertFalse(latest.done())
        self.assert_state(self.preview, pending, displayed)
        value = object()
        second.complete(value)
        self.assertIs(await self.tasks.wait(latest), value)
        self.assert_state(self.preview, False, value)

    async def test_earlier_failure_while_latest_pending(self):
        await self.check_earlier_unsuccessful(cancelled=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.check_earlier_unsuccessful(cancelled=True)

    async def check_latest_unsuccessful_and_retry(self, cancelled):
        older, first, latest, second = await self.overlapping()
        displayed = self.preview.value
        await self.settle_unsuccessfully(latest, second, cancelled)
        self.assertFalse(older.done())
        self.assert_state(self.preview, False, displayed)
        # An older success cannot publish even after the owner has failed.
        pending, displayed = self.preview.pending, self.preview.value
        old_value = object()
        first.complete(old_value)
        self.assertIs(await self.tasks.wait(older), old_value)
        self.assert_state(self.preview, pending, displayed)
        retry, call = await self.begin(self.preview)
        self.assert_state(self.preview, True, displayed)
        value = object()
        call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assert_state(self.preview, False, value)

    async def test_latest_failure_and_retry(self):
        await self.check_latest_unsuccessful_and_retry(cancelled=False)

    async def test_latest_cancellation_and_retry(self):
        await self.check_latest_unsuccessful_and_retry(cancelled=True)

    async def test_synchronous_callback_failure_and_retry(self):
        older, first = await self.begin(self.preview)
        error = ValueError("synchronous failure")
        key = object()
        entries = []

        def raising_fetch(actual_key):
            entries.append(actual_key)
            self.assert_state(self.preview, True, self.prior)
            raise error

        latest = self.tasks.start(self.preview.refresh(key, raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(latest)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(entries), 1)
        self.assertIs(entries[0], key)
        self.assertFalse(older.done())
        self.assert_state(self.preview, False, self.prior)
        retry, call = await self.begin(self.preview)
        self.assert_state(self.preview, True, self.prior)
        pending, displayed = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(older, first, cancelled=False)
        self.assertFalse(retry.done())
        self.assert_state(self.preview, pending, displayed)
        value = object()
        call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assert_state(self.preview, False, value)

    async def test_instance_isolation(self):
        other = Preview()
        fetch = ControlledCall()
        first_task, first = await self.begin(self.preview, fetch, "first")
        other_task, second = await self.begin(other, fetch, "other")
        self.assertEqual(len(fetch.calls), 2)
        self.assert_state(self.preview, True, self.prior)
        self.assert_state(other, True, None)
        other_pending, other_displayed = other.pending, other.value
        value = object()
        first.complete(value)
        self.assertIs(await self.tasks.wait(first_task), value)
        self.assert_state(self.preview, False, value)
        self.assertFalse(other_task.done())
        self.assert_state(other, other_pending, other_displayed)
        retry, third = await self.begin(self.preview)
        pending, displayed = self.preview.pending, self.preview.value
        other_value = object()
        second.complete(other_value)
        self.assertIs(await self.tasks.wait(other_task), other_value)
        self.assert_state(other, False, other_value)
        self.assertFalse(retry.done())
        self.assert_state(self.preview, pending, displayed)
        await self.settle_unsuccessfully(retry, third, cancelled=True)
        self.assert_state(self.preview, False, value)
        self.assert_state(other, False, other_value)


if __name__ == "__main__":
    unittest.main()
