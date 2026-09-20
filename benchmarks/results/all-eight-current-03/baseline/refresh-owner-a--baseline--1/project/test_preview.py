import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    """Signal invocation and let the test choose the callback's outcome."""

    def __init__(self):
        loop = asyncio.get_running_loop()
        self.started = loop.create_future()
        self.result = loop.create_future()
        self.keys = []

    async def __call__(self, key):
        self.keys.append(key)
        if not self.started.done():
            self.started.set_result(None)
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

    async def bounded(self, awaitable):
        if asyncio.iscoroutine(awaitable):
            awaitable = asyncio.create_task(awaitable)
            self.tasks.append(awaitable)
        return await asyncio.wait_for(asyncio.shield(awaitable), TIMEOUT)

    async def start(self, preview, key, fetch):
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        await self.bounded(fetch.started)
        self.assertEqual(len(fetch.keys), 1)
        self.assertIs(fetch.keys[0], key)
        return task

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()

        async def fetch(key):
            return prior

        self.assertIs(await self.bounded(preview.refresh(object(), fetch)), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def assert_failure(self, task, error):
        with self.assertRaises(type(error)) as caught:
            await self.bounded(task)
        self.assertIs(caught.exception, error)

    async def assert_cancelled(self, task):
        with self.assertRaises(asyncio.CancelledError):
            await self.bounded(task)
        self.assertTrue(task.cancelled())

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview, prior = await self.seeded()
                # The same key must still invoke both supplied callbacks.
                key = object()
                older, latest = ControlledFetch(), ControlledFetch()
                old_task = await self.start(preview, key, older)
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                new_task = await self.start(preview, key, latest)
                self.assertFalse(old_task.done())
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                old_value, new_value = object(), object()

                if latest_first:
                    latest.result.set_result(new_value)
                    self.assertIs(await self.bounded(new_task), new_value)
                    self.assertFalse(old_task.done())
                    self.assertFalse(preview.pending)
                    self.assertIs(preview.value, new_value)
                    older.result.set_result(old_value)
                    self.assertIs(await self.bounded(old_task), old_value)
                else:
                    older.result.set_result(old_value)
                    self.assertIs(await self.bounded(old_task), old_value)
                    self.assertFalse(new_task.done())
                    self.assertTrue(preview.pending)
                    self.assertIs(preview.value, prior)
                    latest.result.set_result(new_value)
                    self.assertIs(await self.bounded(new_task), new_value)

                self.assertFalse(preview.pending)
                self.assertIs(preview.value, new_value)

    async def test_earlier_failure_or_cancellation_leaves_latest_pending(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                preview, prior = await self.seeded()
                older, latest = ControlledFetch(), ControlledFetch()
                old_task = await self.start(preview, object(), older)
                new_task = await self.start(preview, object(), latest)
                if cancel:
                    old_task.cancel()
                    await self.assert_cancelled(old_task)
                else:
                    error = RuntimeError("earlier failure")
                    older.result.set_exception(error)
                    await self.assert_failure(old_task, error)
                self.assertFalse(new_task.done())
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                value = object()
                latest.result.set_result(value)
                self.assertIs(await self.bounded(new_task), value)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, value)

    async def test_latest_failure_or_cancellation_and_retry(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                preview, prior = await self.seeded()
                older, latest = ControlledFetch(), ControlledFetch()
                old_task = await self.start(preview, object(), older)
                new_task = await self.start(preview, object(), latest)
                if cancel:
                    new_task.cancel()
                    await self.assert_cancelled(new_task)
                else:
                    error = ValueError("latest failure")
                    latest.result.set_exception(error)
                    await self.assert_failure(new_task, error)
                self.assertFalse(old_task.done())
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, prior)

                # An old success cannot become publishable after latest fails.
                stale = object()
                older.result.set_result(stale)
                self.assertIs(await self.bounded(old_task), stale)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, prior)
                retry = ControlledFetch()
                retry_task = await self.start(preview, object(), retry)
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                value = object()
                retry.result.set_result(value)
                self.assertIs(await self.bounded(retry_task), value)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, value)

    async def test_synchronous_callback_failure_and_overlapping_retry(self):
        preview, prior = await self.seeded()
        older = ControlledFetch()
        old_task = await self.start(preview, object(), older)
        key, error = object(), LookupError("synchronous failure")
        keys = []

        def fail(received_key):
            keys.append(received_key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        await self.assert_failure(preview.refresh(key, fail), error)
        self.assertEqual(len(keys), 1)
        self.assertIs(keys[0], key)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(old_task.done())

        retry = ControlledFetch()
        retry_task = await self.start(preview, object(), retry)
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        old_value = object()
        older.result.set_result(old_value)
        self.assertIs(await self.bounded(old_task), old_value)
        self.assertFalse(retry_task.done())
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        value = object()
        retry.result.set_result(value)
        self.assertIs(await self.bounded(retry_task), value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_instances_are_independent(self):
        first, _ = await self.seeded()
        second, second_prior = await self.seeded()
        one, two = ControlledFetch(), ControlledFetch()
        one_task = await self.start(first, object(), one)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        two_task = await self.start(second, object(), two)
        first_value = object()
        one.result.set_result(first_value)
        self.assertIs(await self.bounded(one_task), first_value)
        self.assertFalse(first.pending)
        self.assertIs(first.value, first_value)
        self.assertFalse(two_task.done())
        self.assertTrue(second.pending)
        self.assertIs(second.value, second_prior)
        error = RuntimeError("second instance failure")
        two.result.set_exception(error)
        await self.assert_failure(two_task, error)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertFalse(first.pending)
        self.assertIs(first.value, first_value)


if __name__ == "__main__":
    unittest.main()
