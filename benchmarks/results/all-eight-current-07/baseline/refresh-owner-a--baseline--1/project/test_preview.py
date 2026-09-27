import asyncio
import unittest

from preview import Preview


TIMEOUT = 1


class ControlledFetch:
    """A real callback whose completion is controlled by each test."""

    def __init__(self):
        self.entered = asyncio.Event()
        self.result = asyncio.get_running_loop().create_future()
        self.keys = []

    def __call__(self, key):
        self.keys.append(key)
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
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), TIMEOUT
            )

    async def start(self, preview, key):
        fetch = ControlledFetch()
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        await asyncio.wait_for(fetch.entered.wait(), TIMEOUT)
        self.assertEqual(len(fetch.keys), 1)
        self.assertIs(fetch.keys[0], key)
        self.assertFalse(task.done())
        return task, fetch

    async def outcome(self, task):
        done, _ = await asyncio.wait({task}, timeout=TIMEOUT)
        self.assertIn(task, done, "refresh did not settle")
        return task.result()

    async def succeed(self, task, fetch, value):
        fetch.result.set_result(value)
        self.assertIs(await self.outcome(task), value)

    async def reject(self, task, fetch, cancellation):
        if cancellation:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError("controlled failure")
            fetch.result.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        task, fetch = await self.start(preview, object())
        self.assertTrue(preview.pending)
        self.assertIsNone(preview.value)
        await self.succeed(task, fetch, prior)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        return preview, prior

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview, prior = await self.seeded()
                # Identical keys must still invoke both supplied callbacks.
                key = object()
                older, older_fetch = await self.start(preview, key)
                latest, latest_fetch = await self.start(preview, key)
                self.assertFalse(older.done())
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                older_value, latest_value = object(), object()
                if latest_first:
                    await self.succeed(latest, latest_fetch, latest_value)
                    self.assertFalse(preview.pending)
                    self.assertIs(preview.value, latest_value)
                    self.assertFalse(older.done())
                    await self.succeed(older, older_fetch, older_value)
                else:
                    await self.succeed(older, older_fetch, older_value)
                    self.assertTrue(preview.pending)
                    self.assertIs(preview.value, prior)
                    self.assertFalse(latest.done())
                    await self.succeed(latest, latest_fetch, latest_value)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, latest_value)

    async def test_earlier_failure_or_cancellation_keeps_latest_pending(self):
        for cancellation in (False, True):
            with self.subTest(cancellation=cancellation):
                preview, prior = await self.seeded()
                older, older_fetch = await self.start(preview, object())
                latest, latest_fetch = await self.start(preview, object())
                await self.reject(older, older_fetch, cancellation)
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                self.assertFalse(latest.done())
                value = object()
                await self.succeed(latest, latest_fetch, value)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, value)

    async def test_latest_failure_or_cancellation_retains_display_and_allows_retry(self):
        for cancellation in (False, True):
            with self.subTest(cancellation=cancellation):
                preview, prior = await self.seeded()
                older, older_fetch = await self.start(preview, object())
                latest, latest_fetch = await self.start(preview, object())
                await self.reject(latest, latest_fetch, cancellation)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, prior)
                self.assertFalse(older.done())
                retry, retry_fetch = await self.start(preview, object())
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                await self.succeed(older, older_fetch, object())
                self.assertTrue(preview.pending)
                self.assertIs(preview.value, prior)
                self.assertFalse(retry.done())
                value = object()
                await self.succeed(retry, retry_fetch, value)
                self.assertFalse(preview.pending)
                self.assertIs(preview.value, value)

    async def test_synchronous_callback_failure_clears_pending_and_allows_retry(self):
        preview, prior = await self.seeded()
        older, older_fetch = await self.start(preview, object())
        error, key = ValueError("synchronous failure"), object()
        calls = []

        def fail(received):
            calls.append(received)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        task = asyncio.create_task(preview.refresh(key, fail))
        self.tasks.append(task)
        with self.assertRaises(ValueError) as caught:
            await self.outcome(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0], key)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        await self.succeed(older, older_fetch, object())
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        retry, fetch = await self.start(preview, key)
        self.assertTrue(preview.pending)
        self.assertIs(preview.value, prior)
        value = object()
        await self.succeed(retry, fetch, value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_instances_have_independent_ownership_and_display(self):
        first, first_prior = await self.seeded()
        second, second_prior = await self.seeded()
        first_task, first_fetch = await self.start(first, object())
        second_old, second_old_fetch = await self.start(second, object())
        second_new, second_new_fetch = await self.start(second, object())
        first_value = object()
        await self.succeed(first_task, first_fetch, first_value)
        self.assertFalse(first.pending)
        self.assertIs(first.value, first_value)
        self.assertTrue(second.pending)
        self.assertIs(second.value, second_prior)
        first_retry, first_retry_fetch = await self.start(first, object())
        await self.reject(second_new, second_new_fetch, cancellation=False)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertTrue(first.pending)
        self.assertIs(first.value, first_value)
        await self.succeed(second_old, second_old_fetch, object())
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertTrue(first.pending)
        await self.succeed(first_retry, first_retry_fetch, first_prior)
        self.assertFalse(first.pending)
        self.assertIs(first.value, first_prior)
        self.assertIs(second.value, second_prior)


if __name__ == "__main__":
    unittest.main()
