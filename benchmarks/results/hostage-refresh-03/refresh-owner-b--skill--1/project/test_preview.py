import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.drain_tasks)

    async def drain_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True), timeout=1
        )

    async def start(self, preview, fetch, key):
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), timeout=1)

    def snapshot(self, preview):
        return preview.pending, preview.value, preview.generation

    def assert_unchanged(self, preview, before):
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
        task, call = await self.start(preview, fetch, "seed")
        call.complete(prior)
        self.assertIs(await self.result(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def overlap(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, first = await self.start(preview, fetch, "same-key")
        latest, second = await self.start(preview, fetch, "same-key")
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertFalse(latest.done())
        self.assertIs(preview.value, prior)
        return preview, prior, older, first, latest, second

    async def test_older_success_while_latest_pending(self):
        preview, prior, older, first, latest, second = await self.overlap()
        before = self.snapshot(preview)
        old_value, new_value = {}, {}
        first.complete(old_value)
        self.assertIs(await self.result(older), old_value)
        self.assert_unchanged(preview, before)
        self.assertFalse(latest.done())
        second.complete(new_value)
        self.assertIs(await self.result(latest), new_value)
        self.assertIs(preview.value, new_value)
        self.assertFalse(preview.pending)

    async def test_latest_success_before_older_success(self):
        preview, prior, older, first, latest, second = await self.overlap()
        new_value, old_value = {}, {}
        second.complete(new_value)
        self.assertIs(await self.result(latest), new_value)
        self.assertIs(preview.value, new_value)
        self.assertFalse(preview.pending)
        self.assertFalse(older.done())
        before = self.snapshot(preview)
        first.complete(old_value)
        self.assertIs(await self.result(older), old_value)
        self.assert_unchanged(preview, before)

    async def settle_unsuccessfully(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(task)
            self.assertIs(caught.exception, error)

    async def earlier_unsuccessful(self, cancel):
        preview, prior, older, first, latest, second = await self.overlap()
        before = self.snapshot(preview)
        await self.settle_unsuccessfully(older, first, cancel)
        self.assert_unchanged(preview, before)
        self.assertFalse(latest.done())
        value = {}
        second.complete(value)
        self.assertIs(await self.result(latest), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        preview, prior, older, first, latest, second = await self.overlap()
        await self.settle_unsuccessfully(latest, second, cancel)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        before = self.snapshot(preview)
        old_value = {}
        first.complete(old_value)
        self.assertIs(await self.result(older), old_value)
        self.assert_unchanged(preview, before)
        fetch = ControlledCall()
        retry, call = await self.start(preview, fetch, "retry")
        self.assertIs(preview.value, prior)
        value = {}
        call.complete(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_failure_and_retry(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        older, first = await self.start(preview, fetch, "older")
        error = RuntimeError("synchronous failure")
        keys = []

        def fail(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        task = asyncio.create_task(preview.refresh("sync", fail))
        self.tasks.append(task)
        with self.assertRaises(RuntimeError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        retry, call = await self.start(preview, fetch, "retry")
        self.assertIs(preview.value, prior)
        before = self.snapshot(preview)
        first.complete(prior)
        self.assertIs(await self.result(older), prior)
        self.assert_unchanged(preview, before)
        value = {}
        call.complete(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instance_isolation(self):
        left, left_prior = await self.seeded()
        right, right_prior = await self.seeded()
        fetch = ControlledCall()
        left_task, left_call = await self.start(left, fetch, "left")
        left_before = self.snapshot(left)
        right_task, right_call = await self.start(right, fetch, "right")
        self.assert_unchanged(left, left_before)
        right_before = self.snapshot(right)
        left_value = {}
        left_call.complete(left_value)
        self.assertIs(await self.result(left_task), left_value)
        self.assertIs(left.value, left_value)
        self.assertFalse(left.pending)
        self.assert_unchanged(right, right_before)
        self.assertFalse(right_task.done())
        left_before = self.snapshot(left)
        await self.settle_unsuccessfully(right_task, right_call, cancel=False)
        self.assertFalse(right.pending)
        self.assertIs(right.value, right_prior)
        self.assert_unchanged(left, left_before)


if __name__ == "__main__":
    unittest.main()
