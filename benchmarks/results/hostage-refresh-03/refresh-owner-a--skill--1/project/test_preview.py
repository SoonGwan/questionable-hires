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
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), 1
            )

    def spawn(self, preview, key, fetch):
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        return task

    async def start(self, preview, fetch, key="same-key"):
        task = self.spawn(preview, key, fetch)
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    def snapshot(self, preview):
        return preview.pending, preview.value, preview.generation

    def assert_unchanged(self, preview, before):
        self.assertIs(preview.pending, before[0])
        self.assertIs(preview.value, before[1])
        self.assertEqual(preview.generation, before[2])

    async def seeded(self):
        preview, fetch, prior = Preview(), ControlledCall(), {"prior": []}
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        task, call = await self.start(preview, fetch, "seed")
        call.complete(prior)
        self.assertIs(await self.result(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def settle_unsuccessfully(self, task, call, mode):
        if mode == "failure":
            error = RuntimeError("fetch failed")
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(task)
            self.assertIs(caught.exception, error)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(task)
            self.assertTrue(task.cancelled())

    async def test_both_success_completion_orders(self):
        for order in ((0, 1), (1, 0)):
            with self.subTest(order=order):
                preview, prior = await self.seeded()
                fetch = ControlledCall()
                old = await self.start(preview, fetch)
                latest = await self.start(preview, fetch)
                self.assertEqual(len(fetch.calls), 2)
                self.assertFalse(old[0].done())
                self.assertIs(preview.value, prior)
                values = [{"old": []}, {"latest": []}]
                calls = (old, latest)
                for index in order:
                    before = self.snapshot(preview)
                    task, call = calls[index]
                    call.complete(values[index])
                    self.assertIs(await self.result(task), values[index])
                    if index == 0:
                        self.assert_unchanged(preview, before)
                    else:
                        self.assertFalse(preview.pending)
                        self.assertIs(preview.value, values[1])
                self.assertIs(preview.value, values[1])

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful("failure")

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful("cancellation")

    async def earlier_unsuccessful(self, mode):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        old_task, old_call = await self.start(preview, fetch)
        latest_task, latest_call = await self.start(preview, fetch)
        self.assertEqual(len(fetch.calls), 2)
        self.assertIs(preview.value, prior)
        before = self.snapshot(preview)
        await self.settle_unsuccessfully(old_task, old_call, mode)
        self.assert_unchanged(preview, before)
        self.assertFalse(latest_task.done())
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.result(latest_task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful("failure")

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful("cancellation")

    async def latest_unsuccessful(self, mode):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        old_task, old_call = await self.start(preview, fetch)
        latest_task, latest_call = await self.start(preview, fetch)
        before = self.snapshot(preview)
        await self.settle_unsuccessfully(latest_task, latest_call, mode)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, before[1])
        self.assertEqual(preview.generation, before[2])
        self.assertFalse(old_task.done())
        retry_task, retry_call = await self.start(preview, fetch)
        self.assertIs(preview.value, prior)
        before = self.snapshot(preview)
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old_task), old_value)
        self.assert_unchanged(preview, before)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.result(retry_task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)
        self.assertEqual(len(fetch.calls), 3)

    async def test_synchronous_failure_and_retry(self):
        preview, prior = await self.seeded()
        fetch = ControlledCall()
        old_task, old_call = await self.start(preview, fetch)
        error = ValueError("synchronous failure")
        entries = []

        def fail(key):
            entries.append((key, preview.pending))
            raise error

        before = self.snapshot(preview)
        task = self.spawn(preview, "sync", fail)
        with self.assertRaises(ValueError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(entries, [("sync", True)])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, before[1])
        self.assertFalse(old_task.done())
        retry_task, retry_call = await self.start(preview, fetch)
        self.assertIs(preview.value, prior)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.result(retry_task), value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)
        before = self.snapshot(preview)
        await self.settle_unsuccessfully(old_task, old_call, "failure")
        self.assert_unchanged(preview, before)

    async def test_instance_isolation(self):
        first, first_prior = await self.seeded()
        second, second_prior = await self.seeded()
        fetch = ControlledCall()
        first_task, first_call = await self.start(first, fetch, "first")
        first_before = self.snapshot(first)
        second_task, second_call = await self.start(second, fetch, "second")
        self.assert_unchanged(first, first_before)
        second_before = self.snapshot(second)
        value = object()
        first_call.complete(value)
        self.assertIs(await self.result(first_task), value)
        self.assertFalse(first.pending)
        self.assertIs(first.value, value)
        self.assert_unchanged(second, second_before)
        self.assertIs(second.value, second_prior)
        self.assertFalse(second_task.done())
        first_before = self.snapshot(first)
        await self.settle_unsuccessfully(second_task, second_call, "failure")
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assert_unchanged(first, first_before)


if __name__ == "__main__":
    unittest.main()
