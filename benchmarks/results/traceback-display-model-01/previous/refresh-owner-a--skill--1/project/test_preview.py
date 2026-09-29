import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def begin(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        self.assertFalse(task.done())
        return task, call

    async def seeded_preview(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        fetch = ControlledCall()
        task, call = await self.begin(preview, fetch, "seed")
        value = {"display": ["prior"]}
        call.complete(value)
        self.assertIs(await self.tasks.wait(task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)
        return preview

    def assert_display(self, preview, value, contents):
        self.assertIs(preview.value, value)
        self.assertEqual(preview.value, contents)

    async def settle_error(self, task, call, cancel):
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

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview = await self.seeded_preview()
                prior = preview.value
                prior_contents = {"display": list(prior["display"])}
                fetch = ControlledCall()
                # Identical keys must still cause two concurrent callback entries.
                older, old_call = await self.begin(preview, fetch, "same")
                latest, new_call = await self.begin(preview, fetch, "same")
                self.assertEqual(len(fetch.calls), 2)
                self.assertFalse(older.done())
                self.assert_display(preview, prior, prior_contents)
                old_value = {"display": ["old"]}
                new_value = {"display": ["new"]}
                if latest_first:
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertFalse(preview.pending)
                    self.assertFalse(older.done())
                    displayed = preview.value
                    contents = {"display": list(displayed["display"])}
                    self.assertIs(displayed, new_value)
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assertFalse(preview.pending)
                    self.assert_display(preview, displayed, contents)
                else:
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assertTrue(preview.pending)
                    self.assertFalse(latest.done())
                    self.assert_display(preview, prior, prior_contents)
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertFalse(preview.pending)
                    self.assertIs(preview.value, new_value)

    async def test_earlier_failure_or_cancellation_keeps_latest_pending(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                preview = await self.seeded_preview()
                fetch = ControlledCall()
                older, old_call = await self.begin(preview, fetch, "old")
                latest, new_call = await self.begin(preview, fetch, "new")
                prior = preview.value
                contents = {"display": list(prior["display"])}
                await self.settle_error(older, old_call, cancel)
                self.assertTrue(preview.pending)
                self.assertFalse(latest.done())
                self.assert_display(preview, prior, contents)
                result = object()
                new_call.complete(result)
                self.assertIs(await self.tasks.wait(latest), result)
                self.assertIs(preview.value, result)
                self.assertFalse(preview.pending)

    async def test_latest_failure_or_cancellation_retains_display_and_retries(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                preview = await self.seeded_preview()
                fetch = ControlledCall()
                older, old_call = await self.begin(preview, fetch, "old")
                latest, new_call = await self.begin(preview, fetch, "new")
                prior = preview.value
                contents = {"display": list(prior["display"])}
                await self.settle_error(latest, new_call, cancel)
                self.assertFalse(preview.pending)
                self.assertFalse(older.done())
                self.assert_display(preview, prior, contents)
                retry, retry_call = await self.begin(preview, fetch, "new")
                self.assertEqual(len(fetch.calls), 3)
                self.assert_display(preview, prior, contents)
                old_value = object()
                old_call.complete(old_value)
                self.assertIs(await self.tasks.wait(older), old_value)
                self.assertTrue(preview.pending)
                self.assertFalse(retry.done())
                self.assert_display(preview, prior, contents)
                result = object()
                retry_call.complete(result)
                self.assertIs(await self.tasks.wait(retry), result)
                self.assertIs(preview.value, result)
                self.assertFalse(preview.pending)

    async def test_synchronous_callback_failure_and_retry(self):
        preview = await self.seeded_preview()
        fetch = ControlledCall()
        older, old_call = await self.begin(preview, fetch, "old")
        prior = preview.value
        contents = {"display": list(prior["display"])}
        error = ValueError("synchronous failure")
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            raise error

        failed = self.tasks.start(preview.refresh("sync", raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(preview.pending)
        self.assertFalse(older.done())
        self.assert_display(preview, prior, contents)
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(older), old_value)
        self.assertFalse(preview.pending)
        self.assert_display(preview, prior, contents)
        retry, retry_call = await self.begin(preview, fetch, "sync")
        self.assert_display(preview, prior, contents)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, result)

    async def test_instances_are_independent(self):
        first = await self.seeded_preview()
        second = await self.seeded_preview()
        first_fetch, second_fetch = ControlledCall(), ControlledCall()
        first_task, first_call = await self.begin(first, first_fetch, "same")
        second_task, second_call = await self.begin(second, second_fetch, "same")
        second_prior = second.value
        contents = {"display": list(second_prior["display"])}
        first_value = {"display": ["first"]}
        first_call.complete(first_value)
        self.assertIs(await self.tasks.wait(first_task), first_value)
        self.assertIs(first.value, first_value)
        self.assertFalse(first.pending)
        self.assertTrue(second.pending)
        self.assertFalse(second_task.done())
        self.assert_display(second, second_prior, contents)
        first_contents = {"display": list(first_value["display"])}
        await self.settle_error(second_task, second_call, cancel=False)
        self.assertFalse(second.pending)
        self.assert_display(second, second_prior, contents)
        self.assertFalse(first.pending)
        self.assert_display(first, first_value, first_contents)
        retry, retry_call = await self.begin(second, second_fetch, "same")
        self.assertFalse(first.pending)
        second_value = object()
        retry_call.complete(second_value)
        self.assertIs(await self.tasks.wait(retry), second_value)
        self.assertIs(second.value, second_value)
        self.assertFalse(second.pending)
        self.assert_display(first, first_value, first_contents)


if __name__ == "__main__":
    unittest.main()
