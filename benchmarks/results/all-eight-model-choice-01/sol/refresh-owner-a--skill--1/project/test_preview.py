import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


async def return_value(_key, value):
    return value


class PreviewRefreshTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def seed(self, preview, value):
        self.assertIs(await preview.refresh("seed", lambda key: return_value(key, value)), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def start_pair(self, preview, fetch):
        earlier = self.tasks.start(preview.refresh("earlier", fetch))
        earlier_call = await fetch.started_before(earlier)
        latest = self.tasks.start(preview.refresh("latest", fetch))
        latest_call = await fetch.started_before(latest)
        self.assertEqual(earlier_call.args, ("earlier",))
        self.assertEqual(latest_call.args, ("latest",))
        self.assertIsNot(earlier_call, latest_call)
        self.assertTrue(preview.pending)
        return earlier, earlier_call, latest, latest_call

    async def test_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview = Preview()
                prior = object()
                await self.seed(preview, prior)
                fetch = ControlledCall()
                earlier, earlier_call, latest, latest_call = await self.start_pair(preview, fetch)
                self.assertIs(preview.value, prior)
                earlier_value = object()
                latest_value = object()

                if latest_first:
                    latest_call.complete(latest_value)
                    self.assertIs(await self.tasks.wait(latest), latest_value)
                    self.assertIs(preview.value, latest_value)
                    self.assertFalse(preview.pending)
                    displayed = preview.value
                    earlier_call.complete(earlier_value)
                    self.assertIs(await self.tasks.wait(earlier), earlier_value)
                    self.assertIs(preview.value, displayed)
                    self.assertFalse(preview.pending)
                else:
                    earlier_call.complete(earlier_value)
                    self.assertIs(await self.tasks.wait(earlier), earlier_value)
                    self.assertIs(preview.value, prior)
                    self.assertTrue(preview.pending)
                    latest_call.complete(latest_value)
                    self.assertIs(await self.tasks.wait(latest), latest_value)
                    self.assertIs(preview.value, latest_value)
                    self.assertFalse(preview.pending)

    async def test_earlier_failure_or_cancellation_preserves_latest_pending(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                preview = Preview()
                prior = object()
                await self.seed(preview, prior)
                fetch = ControlledCall()
                earlier, earlier_call, latest, latest_call = await self.start_pair(preview, fetch)
                displayed = preview.value

                if cancel:
                    earlier.cancel()
                    with self.assertRaises(asyncio.CancelledError):
                        await self.tasks.wait(earlier)
                else:
                    error = ValueError("earlier failed")
                    earlier_call.fail(error)
                    with self.assertRaises(ValueError) as raised:
                        await self.tasks.wait(earlier)
                    self.assertIs(raised.exception, error)
                self.assertIs(preview.value, displayed)
                self.assertTrue(preview.pending)

                latest_value = object()
                latest_call.complete(latest_value)
                self.assertIs(await self.tasks.wait(latest), latest_value)
                self.assertIs(preview.value, latest_value)
                self.assertFalse(preview.pending)

    async def test_latest_failure_or_cancellation_allows_retry(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                preview = Preview()
                prior = object()
                await self.seed(preview, prior)
                fetch = ControlledCall()
                earlier, earlier_call, latest, latest_call = await self.start_pair(preview, fetch)
                displayed = preview.value

                if cancel:
                    latest.cancel()
                    with self.assertRaises(asyncio.CancelledError):
                        await self.tasks.wait(latest)
                else:
                    error = RuntimeError("latest failed")
                    latest_call.fail(error)
                    with self.assertRaises(RuntimeError) as raised:
                        await self.tasks.wait(latest)
                    self.assertIs(raised.exception, error)
                self.assertIs(preview.value, displayed)
                self.assertFalse(preview.pending)

                retry = self.tasks.start(preview.refresh("retry", fetch))
                retry_call = await fetch.started_before(retry)
                self.assertEqual(retry_call.args, ("retry",))
                self.assertTrue(preview.pending)
                earlier_value = object()
                earlier_call.complete(earlier_value)
                self.assertIs(await self.tasks.wait(earlier), earlier_value)
                self.assertIs(preview.value, displayed)
                self.assertTrue(preview.pending)
                retry_value = object()
                retry_call.complete(retry_value)
                self.assertIs(await self.tasks.wait(retry), retry_value)
                self.assertIs(preview.value, retry_value)
                self.assertFalse(preview.pending)

    async def test_synchronous_callback_failure_clears_pending_and_allows_retry(self):
        preview = Preview()
        prior = object()
        await self.seed(preview, prior)
        error = LookupError("callback failed before returning")

        def fail_synchronously(key):
            self.assertEqual(key, "failure")
            self.assertTrue(preview.pending)
            raise error

        with self.assertRaises(LookupError) as raised:
            await preview.refresh("failure", fail_synchronously)
        self.assertIs(raised.exception, error)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)

        fetch = ControlledCall()
        retry = self.tasks.start(preview.refresh("retry", fetch))
        retry_call = await fetch.started_before(retry)
        self.assertTrue(preview.pending)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.tasks.wait(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instances_keep_independent_display_and_pending(self):
        first, second = Preview(), Preview()
        first_prior, second_prior = object(), object()
        await self.seed(first, first_prior)
        await self.seed(second, second_prior)
        fetch = ControlledCall()
        first_task = self.tasks.start(first.refresh("first", fetch))
        first_call = await fetch.started_before(first_task)
        second_task = self.tasks.start(second.refresh("second", fetch))
        second_call = await fetch.started_before(second_task)
        self.assertEqual(first_call.args, ("first",))
        self.assertEqual(second_call.args, ("second",))
        self.assertTrue(first.pending)
        self.assertTrue(second.pending)

        first_value = object()
        first_call.complete(first_value)
        self.assertIs(await self.tasks.wait(first_task), first_value)
        self.assertIs(first.value, first_value)
        self.assertFalse(first.pending)
        self.assertIs(second.value, second_prior)
        self.assertTrue(second.pending)

        second_value = object()
        second_call.complete(second_value)
        self.assertIs(await self.tasks.wait(second_task), second_value)
        self.assertIs(second.value, second_value)
        self.assertFalse(second.pending)
        self.assertIs(first.value, first_value)
