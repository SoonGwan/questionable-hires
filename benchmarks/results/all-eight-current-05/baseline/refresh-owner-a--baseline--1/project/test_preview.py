import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    """Signal invocation and let the test decide when and how fetching settles."""

    def __init__(self, preview):
        self.preview = preview
        self.entered = asyncio.Event()
        self.result = asyncio.get_running_loop().create_future()
        self.calls = []

    def __call__(self, key):
        self.calls.append((key, self.preview.pending, self.preview.value))
        self.entered.set()
        return self.result


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            done, pending = await asyncio.wait(self.tasks, timeout=TIMEOUT)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "Owned refresh tasks did not stop")

    async def bounded(self, awaitable):
        return await asyncio.wait_for(asyncio.shield(awaitable), TIMEOUT)

    async def start(self, preview, key):
        fetch = ControlledFetch(preview)
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        # wait_for owns and cleans up this short-lived Event.wait task.
        await asyncio.wait_for(fetch.entered.wait(), TIMEOUT)
        self.assertEqual(len(fetch.calls), 1)
        self.assertIs(fetch.calls[0][0], key)
        self.assertTrue(fetch.calls[0][1])
        self.assertTrue(preview.pending)
        self.assertFalse(task.done())
        return task, fetch

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        task, fetch = await self.start(preview, object())
        fetch.result.set_result(prior)
        self.assertIs(await self.bounded(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return preview, prior

    async def pair(self):
        preview, prior = await self.seeded()
        # The same key must still invoke both callbacks independently.
        key = object()
        older, first = await self.start(preview, key)
        latest, second = await self.start(preview, key)
        self.assertFalse(older.done())
        self.assertFalse(first.result.cancelled())
        self.assertIs(first.calls[0][2], prior)
        self.assertIs(second.calls[0][2], prior)
        self.assertIs(preview.value, prior)
        return preview, prior, older, first, latest, second

    async def fail(self, task, fetch, cancelled):
        if cancelled:
            task.cancel("controlled cancellation")
            with self.assertRaises(asyncio.CancelledError):
                await self.bounded(task)
            self.assertTrue(task.cancelled())
            self.assertTrue(fetch.result.cancelled())
        else:
            error = RuntimeError("controlled failure")
            fetch.result.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.bounded(task)
            self.assertIs(caught.exception, error)

    async def test_older_success_then_latest_success(self):
        preview, prior, older, first, latest, second = await self.pair()
        old_value, new_value = object(), object()
        first.result.set_result(old_value)
        self.assertIs(await self.bounded(older), old_value)
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(latest.done())
        second.result.set_result(new_value)
        self.assertIs(await self.bounded(latest), new_value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, new_value)

    async def test_latest_success_then_older_success(self):
        preview, prior, older, first, latest, second = await self.pair()
        old_value, new_value = object(), object()
        second.result.set_result(new_value)
        self.assertIs(await self.bounded(latest), new_value)
        self.assertFalse(preview.pending)
        self.assertFalse(older.done())
        self.assertIs(preview.value, new_value)
        first.result.set_result(old_value)
        self.assertIs(await self.bounded(older), old_value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, new_value)

    async def earlier_failure_or_cancellation(self, cancelled):
        preview, prior, older, first, latest, second = await self.pair()
        await self.fail(older, first, cancelled)
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(latest.done())
        value = object()
        second.result.set_result(value)
        self.assertIs(await self.bounded(latest), value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_failure_or_cancellation(False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_failure_or_cancellation(True)

    async def latest_failure_or_cancellation_and_retry(self, cancelled):
        preview, prior, older, first, latest, second = await self.pair()
        await self.fail(latest, second, cancelled)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        retry, third = await self.start(preview, object())
        self.assertIs(preview.value, prior)
        old_value = object()
        first.result.set_result(old_value)
        self.assertIs(await self.bounded(older), old_value)
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        value = object()
        third.result.set_result(value)
        self.assertIs(await self.bounded(retry), value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_latest_failure_and_retry(self):
        await self.latest_failure_or_cancellation_and_retry(False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_failure_or_cancellation_and_retry(True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        older, first = await self.start(preview, object())
        key, error = object(), LookupError("synchronous failure")
        calls = []

        def fetch(received_key):
            calls.append(received_key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        with self.assertRaises(LookupError) as caught:
            await self.bounded(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0], key)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        first.result.set_result(object())
        await self.bounded(older)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        retry, second = await self.start(preview, key)
        value = object()
        second.result.set_result(value)
        self.assertIs(await self.bounded(retry), value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_instances_are_independent(self):
        left, left_prior = await self.seeded()
        right, right_prior = await self.seeded()
        left_task, left_fetch = await self.start(left, object())
        right_task, right_fetch = await self.start(right, object())
        left_latest, left_second = await self.start(left, object())
        right_value = object()
        right_fetch.result.set_result(right_value)
        self.assertIs(await self.bounded(right_task), right_value)
        self.assertIs(right.value, right_value)
        self.assertFalse(right.pending)
        self.assertTrue(left.pending)
        self.assertIs(left.value, left_prior)
        await self.fail(left_latest, left_second, False)
        self.assertFalse(left.pending)
        self.assertIs(left.value, left_prior)
        left_fetch.result.set_result(object())
        await self.bounded(left_task)
        self.assertFalse(left.pending)
        self.assertIs(left.value, left_prior)
        self.assertIs(right.value, right_value)
        self.assertFalse(right.pending)


if __name__ == "__main__":
    unittest.main()
