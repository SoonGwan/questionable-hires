import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    def __init__(self):
        self.started = asyncio.Event()
        self.result = asyncio.get_running_loop().create_future()
        self.keys = []

    async def __call__(self, key):
        self.keys.append(key)
        self.started.set()
        return await self.result


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), TIMEOUT
            )

    async def seed(self, preview):
        value = object()

        async def fetch(key):
            return value

        task = asyncio.create_task(preview.refresh("seed", fetch))
        self.tasks.append(task)
        self.assertIs(await self.result(task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)
        return value

    async def start(self, preview, key="same-key"):
        fetch = ControlledFetch()
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        await asyncio.wait_for(fetch.started.wait(), TIMEOUT)
        self.assertEqual(fetch.keys, [key])
        self.assertTrue(preview.pending)
        return task, fetch

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), TIMEOUT)

    async def fail(self, task, fetch, cancellation):
        if cancellation:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("controlled failure")
            fetch.result.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(task)
            self.assertIs(caught.exception, error)

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview = Preview()
                self.assertIsNone(preview.value)
                prior = await self.seed(preview)
                older, older_fetch = await self.start(preview)
                latest, latest_fetch = await self.start(preview)
                generation = preview.generation
                self.assertFalse(older.done())
                self.assertIs(preview.value, prior)
                older_value, latest_value = object(), object()
                if latest_first:
                    latest_fetch.result.set_result(latest_value)
                    self.assertIs(await self.result(latest), latest_value)
                    self.assertFalse(preview.pending)
                    self.assertFalse(older.done())
                    self.assertIs(preview.value, latest_value)
                    older_fetch.result.set_result(older_value)
                    self.assertIs(await self.result(older), older_value)
                else:
                    older_fetch.result.set_result(older_value)
                    self.assertIs(await self.result(older), older_value)
                    self.assertTrue(preview.pending)
                    self.assertFalse(latest.done())
                    self.assertIs(preview.value, prior)
                    latest_fetch.result.set_result(latest_value)
                    self.assertIs(await self.result(latest), latest_value)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, latest_value)
                self.assertEqual(preview.generation, generation)

    async def test_earlier_failure_or_cancellation_keeps_latest_pending(self):
        for cancellation in (False, True):
            with self.subTest(cancellation=cancellation):
                preview = Preview()
                prior = await self.seed(preview)
                older, older_fetch = await self.start(preview)
                latest, latest_fetch = await self.start(preview)
                generation = preview.generation
                await self.fail(older, older_fetch, cancellation)
                self.assertTrue(preview.pending)
                self.assertFalse(latest.done())
                self.assertIs(preview.value, prior)
                self.assertEqual(preview.generation, generation)
                value = object()
                latest_fetch.result.set_result(value)
                self.assertIs(await self.result(latest), value)
                self.assertIs(preview.value, value)
                self.assertFalse(preview.pending)

    async def test_latest_failure_or_cancellation_retains_display_and_allows_retry(self):
        for cancellation in (False, True):
            with self.subTest(cancellation=cancellation):
                preview = Preview()
                prior = await self.seed(preview)
                older, older_fetch = await self.start(preview)
                latest, latest_fetch = await self.start(preview)
                await self.fail(latest, latest_fetch, cancellation)
                self.assertFalse(preview.pending)
                self.assertFalse(older.done())
                self.assertIs(preview.value, prior)
                retry, retry_fetch = await self.start(preview)
                self.assertIs(preview.value, prior)
                generation = preview.generation
                older_value = object()
                older_fetch.result.set_result(older_value)
                self.assertIs(await self.result(older), older_value)
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                self.assertEqual(preview.generation, generation)
                value = object()
                retry_fetch.result.set_result(value)
                self.assertIs(await self.result(retry), value)
                self.assertIs(preview.value, value)
                self.assertFalse(preview.pending)

    async def test_synchronous_callback_failure_and_retry(self):
        preview = Preview()
        prior = await self.seed(preview)
        older, older_fetch = await self.start(preview)
        error = ValueError("synchronous failure")
        keys = []

        def fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            raise error

        task = asyncio.create_task(preview.refresh("sync", fetch))
        self.tasks.append(task)
        with self.assertRaises(ValueError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        older_value = object()
        older_fetch.result.set_result(older_value)
        self.assertIs(await self.result(older), older_value)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        retry, retry_fetch = await self.start(preview)
        self.assertIs(preview.value, prior)
        value = object()
        retry_fetch.result.set_result(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def test_instances_are_independent(self):
        first, second = Preview(), Preview()
        first_prior, second_prior = await self.seed(first), await self.seed(second)
        first_task, first_fetch = await self.start(first)
        first_generation = first.generation
        second_task, second_fetch = await self.start(second)
        second_older, second_older_fetch = second_task, second_fetch
        second_task, second_fetch = await self.start(second)
        second_generation = second.generation
        first_value = object()
        first_fetch.result.set_result(first_value)
        self.assertIs(first.value, first_prior)
        self.assertIs(await self.result(first_task), first_value)
        self.assertIs(first.value, first_value)
        self.assertFalse(first.pending)
        self.assertEqual(first.generation, first_generation)
        self.assertTrue(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertEqual(second.generation, second_generation)
        await self.fail(second_older, second_older_fetch, False)
        self.assertTrue(second.pending)
        second_value = object()
        second_fetch.result.set_result(second_value)
        self.assertIs(await self.result(second_task), second_value)
        self.assertIs(second.value, second_value)
        self.assertFalse(second.pending)
        self.assertIs(first.value, first_value)
        self.assertFalse(first.pending)
        self.assertEqual(first.generation, first_generation)


if __name__ == "__main__":
    unittest.main()
