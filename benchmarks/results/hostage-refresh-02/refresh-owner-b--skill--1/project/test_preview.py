import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 1

    def own(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.addAsyncCleanup(self.drain, task)
        return task

    async def drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), self.TIMEOUT
        )

    async def outcome(self, task):
        return await asyncio.wait_for(asyncio.shield(task), self.TIMEOUT)

    async def start(self, preview, fetch, key):
        task = self.own(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=self.TIMEOUT)
        self.assertEqual(len(call.args), 1)
        self.assertIs(call.args[0], key)
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    def snapshot(self, preview):
        return preview.pending, preview.value, preview.generation

    def assertUnchanged(self, preview, before):
        pending, value, generation = before
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)
        self.assertEqual(preview.generation, generation)

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = {"prior": []}
        fetch = ControlledCall()
        task, call = await self.start(preview, fetch, object())
        call.complete(prior)
        self.assertIs(await self.outcome(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def overlapping(self):
        preview, prior = await self.seeded()
        fetch, key = ControlledCall(), object()
        older, first = await self.start(preview, fetch, key)
        self.assertIs(preview.value, prior)
        latest, second = await self.start(preview, fetch, key)
        self.assertIs(preview.value, prior)
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertFalse(latest.done())
        return preview, prior, fetch, older, first, latest, second

    async def test_earlier_success_then_latest_success(self):
        preview, prior, fetch, older, first, latest, second = await self.overlapping()
        old_value, new_value = {"old": []}, {"new": []}
        before = self.snapshot(preview)
        first.complete(old_value)
        self.assertIs(await self.outcome(older), old_value)
        self.assertUnchanged(preview, before)
        self.assertFalse(latest.done())
        second.complete(new_value)
        self.assertIs(await self.outcome(latest), new_value)
        self.assertIs(preview.value, new_value)
        self.assertFalse(preview.pending)

    async def test_latest_success_then_earlier_success(self):
        preview, prior, fetch, older, first, latest, second = await self.overlapping()
        old_value, new_value = {"old": []}, {"new": []}
        second.complete(new_value)
        self.assertIs(await self.outcome(latest), new_value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, new_value)
        self.assertFalse(older.done())
        before = self.snapshot(preview)
        first.complete(old_value)
        self.assertIs(await self.outcome(older), old_value)
        self.assertUnchanged(preview, before)

    async def settle_unsuccessfully(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("controlled failure")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)

    async def earlier_unsuccessful(self, cancel):
        preview, prior, fetch, older, first, latest, second = await self.overlapping()
        before = self.snapshot(preview)
        await self.settle_unsuccessfully(older, first, cancel)
        self.assertUnchanged(preview, before)
        self.assertFalse(latest.done())
        value = object()
        second.complete(value)
        self.assertIs(await self.outcome(latest), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        preview, prior, fetch, older, first, latest, second = await self.overlapping()
        before = self.snapshot(preview)
        await self.settle_unsuccessfully(latest, second, cancel)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, before[1])
        self.assertEqual(preview.generation, before[2])
        self.assertFalse(older.done())
        retry, third = await self.start(preview, fetch, object())
        self.assertEqual(len(fetch.calls), 3)
        self.assertIs(preview.value, prior)
        before = self.snapshot(preview)
        old_value = object()
        first.complete(old_value)
        self.assertIs(await self.outcome(older), old_value)
        self.assertUnchanged(preview, before)
        self.assertFalse(retry.done())
        value = object()
        third.complete(value)
        self.assertIs(await self.outcome(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, first = await self.start(preview, fetch, object())
        error, key = ValueError("synchronous failure"), object()
        calls = []

        def fail(actual_key):
            calls.append(actual_key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        before = self.snapshot(preview)
        failed = self.own(preview.refresh(key, fail))
        with self.assertRaises(ValueError) as caught:
            await self.outcome(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0], key)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, before[1])
        self.assertFalse(older.done())
        before = self.snapshot(preview)
        first.complete(prior)
        self.assertIs(await self.outcome(older), prior)
        self.assertUnchanged(preview, before)
        retry, call = await self.start(preview, fetch, key)
        self.assertIs(preview.value, prior)
        value = object()
        call.complete(value)
        self.assertIs(await self.outcome(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instance_isolation(self):
        left, left_prior = await self.seeded()
        right, right_prior = await self.seeded()
        left_fetch, right_fetch = ControlledCall(), ControlledCall()
        right_before = self.snapshot(right)
        left_task, left_call = await self.start(left, left_fetch, object())
        self.assertUnchanged(right, right_before)
        self.assertIs(left.value, left_prior)
        left_pending = self.snapshot(left)
        right_task, right_call = await self.start(right, right_fetch, object())
        self.assertUnchanged(left, left_pending)
        self.assertIs(right.value, right_prior)
        right_pending = self.snapshot(right)
        left_value = object()
        left_call.complete(left_value)
        self.assertIs(await self.outcome(left_task), left_value)
        self.assertIs(left.value, left_value)
        self.assertFalse(left.pending)
        self.assertUnchanged(right, right_pending)
        self.assertFalse(right_task.done())
        left_settled = self.snapshot(left)
        right_value = object()
        right_call.complete(right_value)
        self.assertIs(await self.outcome(right_task), right_value)
        self.assertIs(right.value, right_value)
        self.assertFalse(right.pending)
        self.assertUnchanged(left, left_settled)


if __name__ == "__main__":
    unittest.main()
