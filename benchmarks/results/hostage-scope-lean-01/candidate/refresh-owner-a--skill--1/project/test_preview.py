import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    def __init__(self):
        self.entered = asyncio.Event()
        self.result = asyncio.get_running_loop().create_future()
        self.keys = []

    async def __call__(self, key):
        self.keys.append(key)
        self.entered.set()
        return await self.result


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True), TIMEOUT
        )

    async def settle(self, task):
        return await asyncio.wait_for(asyncio.shield(task), TIMEOUT)

    async def start(self, preview, key):
        fetch = ControlledFetch()
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        await asyncio.wait_for(fetch.entered.wait(), TIMEOUT)
        self.assertEqual(fetch.keys, [key])
        self.assertTrue(preview.pending)
        self.assertFalse(task.done())
        return task, fetch

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        task, fetch = await self.start(preview, "seed")
        fetch.result.set_result(prior)
        self.assertIs(await self.settle(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def completion_order(self, latest_first):
        preview, prior = await self.seeded()
        # Reuse the key to ensure overlapping duplicates still invoke fetch.
        older, old_fetch = await self.start(preview, "same")
        latest, new_fetch = await self.start(preview, "same")
        self.assertIs(preview.value, prior)
        old_value, new_value = object(), object()
        if latest_first:
            new_fetch.result.set_result(new_value)
            self.assertIs(await self.settle(latest), new_value)
            self.assertFalse(preview.pending)
            self.assertFalse(older.done())
            self.assertIs(preview.value, new_value)
            displayed = preview.value
            old_fetch.result.set_result(old_value)
            self.assertIs(await self.settle(older), old_value)
            self.assertIs(preview.value, displayed)
        else:
            old_fetch.result.set_result(old_value)
            self.assertIs(await self.settle(older), old_value)
            self.assertTrue(preview.pending)
            self.assertFalse(latest.done())
            self.assertIs(preview.value, prior)
            new_fetch.result.set_result(new_value)
            self.assertIs(await self.settle(latest), new_value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, new_value)
        self.assertEqual(old_fetch.keys, ["same"])
        self.assertEqual(new_fetch.keys, ["same"])

    async def test_earlier_success_before_latest(self):
        await self.completion_order(latest_first=False)

    async def test_latest_success_before_earlier(self):
        await self.completion_order(latest_first=True)

    async def reject(self, task, fetch, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.settle(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("fetch failed")
            fetch.result.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.settle(task)
            self.assertIs(caught.exception, error)

    async def earlier_rejection(self, cancel):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "older")
        latest, new_fetch = await self.start(preview, "latest")
        self.assertIs(preview.value, prior)
        await self.reject(older, old_fetch, cancel)
        self.assertTrue(preview.pending)
        self.assertFalse(latest.done())
        self.assertIs(preview.value, prior)
        value = object()
        new_fetch.result.set_result(value)
        self.assertIs(await self.settle(latest), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_rejection(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_rejection(cancel=True)

    async def latest_rejection_and_retry(self, cancel):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "older")
        latest, new_fetch = await self.start(preview, "latest")
        self.assertIs(preview.value, prior)
        await self.reject(latest, new_fetch, cancel)
        self.assertFalse(preview.pending)
        self.assertFalse(older.done())
        self.assertIs(preview.value, prior)
        retry, retry_fetch = await self.start(preview, "retry")
        self.assertIs(preview.value, prior)
        old_value = object()
        old_fetch.result.set_result(old_value)
        self.assertIs(await self.settle(older), old_value)
        self.assertTrue(preview.pending)
        self.assertFalse(retry.done())
        self.assertIs(preview.value, prior)
        value = object()
        retry_fetch.result.set_result(value)
        self.assertIs(await self.settle(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.latest_rejection_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_rejection_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "older")
        error = ValueError("synchronous failure")
        keys = []

        def fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            raise error

        task = asyncio.create_task(preview.refresh("sync", fetch))
        self.tasks.append(task)
        with self.assertRaises(ValueError) as caught:
            await self.settle(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(preview.pending)
        self.assertFalse(older.done())
        self.assertIs(preview.value, prior)
        old_value = object()
        old_fetch.result.set_result(old_value)
        self.assertIs(await self.settle(older), old_value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        retry, retry_fetch = await self.start(preview, "retry")
        self.assertIs(preview.value, prior)
        value = object()
        retry_fetch.result.set_result(value)
        self.assertIs(await self.settle(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instance_isolation(self):
        first, first_prior = await self.seeded()
        second, second_prior = await self.seeded()
        older, old_fetch = await self.start(first, "older")
        latest, new_fetch = await self.start(first, "latest")
        other, other_fetch = await self.start(second, "other")
        self.assertIs(first.value, first_prior)
        self.assertIs(second.value, second_prior)
        value = object()
        new_fetch.result.set_result(value)
        self.assertIs(await self.settle(latest), value)
        self.assertFalse(first.pending)
        self.assertTrue(second.pending)
        self.assertFalse(other.done())
        self.assertFalse(older.done())
        self.assertIs(second.value, second_prior)
        await self.reject(other, other_fetch, cancel=False)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertIs(first.value, value)
        await self.reject(older, old_fetch, cancel=True)
        self.assertFalse(first.pending)
        self.assertIs(first.value, value)


if __name__ == "__main__":
    unittest.main()
