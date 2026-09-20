import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), 1
            )

    def launch(self, preview, key, fetch):
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        return task

    async def outcome(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    async def enter(self, preview, fetch, key):
        task = self.launch(preview, key, fetch)
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
        task, call = await self.enter(preview, fetch, "seed")
        prior = {"display": ["prior"]}
        call.complete(prior)
        self.assertIs(await self.outcome(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    def state(self, preview):
        # Capture field values, not an alias to the mutable Preview owner.
        return preview.pending, preview.value

    def assert_state(self, preview, state):
        pending, value = state
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def overlap(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        # Identical keys must still enter the callback independently.
        older, old_call = await self.enter(preview, fetch, "same")
        self.assertIs(preview.value, prior)
        latest, latest_call = await self.enter(preview, fetch, "same")
        self.assertIs(preview.value, prior)
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        return preview, older, old_call, latest, latest_call

    async def settle_unsuccessfully(self, task, call, cancellation):
        if cancellation:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)

    async def test_earlier_success_while_latest_pending(self):
        preview, older, old_call, latest, latest_call = await self.overlap()
        before = self.state(preview)
        old_result = {"old": []}
        old_call.complete(old_result)
        self.assertIs(await self.outcome(older), old_result)
        self.assert_state(preview, before)
        self.assertFalse(latest.done())
        new_result = {"new": []}
        latest_call.complete(new_result)
        self.assertIs(await self.outcome(latest), new_result)
        self.assert_state(preview, (False, new_result))

    async def test_latest_success_before_earlier_success(self):
        preview, older, old_call, latest, latest_call = await self.overlap()
        new_result = {"new": []}
        latest_call.complete(new_result)
        self.assertIs(await self.outcome(latest), new_result)
        self.assert_state(preview, (False, new_result))
        self.assertFalse(older.done())
        before = self.state(preview)
        old_result = {"old": []}
        old_call.complete(old_result)
        self.assertIs(await self.outcome(older), old_result)
        self.assert_state(preview, before)

    async def earlier_unsuccessful(self, cancellation):
        preview, older, old_call, latest, latest_call = await self.overlap()
        before = self.state(preview)
        await self.settle_unsuccessfully(older, old_call, cancellation)
        self.assert_state(preview, before)
        self.assertFalse(latest.done())
        result = object()
        latest_call.complete(result)
        self.assertIs(await self.outcome(latest), result)
        self.assert_state(preview, (False, result))

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancellation=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancellation=True)

    async def latest_unsuccessful_and_retry(self, cancellation):
        preview, older, old_call, latest, latest_call = await self.overlap()
        prior = preview.value
        await self.settle_unsuccessfully(latest, latest_call, cancellation)
        self.assert_state(preview, (False, prior))
        self.assertFalse(older.done())
        before = self.state(preview)
        old_result = object()
        old_call.complete(old_result)
        self.assertIs(await self.outcome(older), old_result)
        self.assert_state(preview, before)
        fetch = ControlledCall()
        retry, retry_call = await self.enter(preview, fetch, "retry")
        self.assertIs(preview.value, prior)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.outcome(retry), result)
        self.assert_state(preview, (False, result))

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancellation=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancellation=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        older, old_call = await self.enter(preview, fetch, "older")
        error = ValueError("synchronous failure")
        entered = []

        def raising_fetch(key):
            entered.append(key)
            self.assert_state(preview, (True, prior))
            raise error

        failed = self.launch(preview, "sync", raising_fetch)
        with self.assertRaises(ValueError) as caught:
            await self.outcome(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(entered, ["sync"])
        self.assert_state(preview, (False, prior))
        self.assertFalse(older.done())
        retry, retry_call = await self.enter(preview, fetch, "retry")
        before = self.state(preview)
        old_result = object()
        old_call.complete(old_result)
        self.assertIs(await self.outcome(older), old_result)
        self.assert_state(preview, before)
        self.assertFalse(retry.done())
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.outcome(retry), result)
        self.assert_state(preview, (False, result))

    async def test_instances_are_independent(self):
        first, first_prior = await self.seeded_preview()
        second, second_prior = await self.seeded_preview()
        first_fetch, second_fetch = ControlledCall(), ControlledCall()
        first_task, first_call = await self.enter(first, first_fetch, "key")
        second_task, second_call = await self.enter(second, second_fetch, "key")
        first_before = self.state(first)
        second_result = object()
        second_call.complete(second_result)
        self.assertIs(await self.outcome(second_task), second_result)
        self.assert_state(second, (False, second_result))
        self.assert_state(first, first_before)
        self.assertFalse(first_task.done())
        second_before = self.state(second)
        first_result = object()
        first_call.complete(first_result)
        self.assertIs(await self.outcome(first_task), first_result)
        self.assert_state(first, (False, first_result))
        self.assert_state(second, second_before)
        second_task, second_call = await self.enter(second, second_fetch, "again")
        first_before = self.state(first)
        await self.settle_unsuccessfully(second_task, second_call, False)
        self.assert_state(second, (False, second_result))
        self.assert_state(first, first_before)

    async def test_none_result_replaces_prior_display(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledCall()
        task, call = await self.enter(preview, fetch, "none")
        self.assertIs(preview.value, prior)
        call.complete(None)
        self.assertIsNone(await self.outcome(task))
        self.assert_state(preview, (False, None))


if __name__ == "__main__":
    unittest.main()
