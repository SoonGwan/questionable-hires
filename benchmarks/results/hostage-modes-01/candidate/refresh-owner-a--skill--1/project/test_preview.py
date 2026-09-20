import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    def __init__(self):
        self.entered = asyncio.Event()
        self.result = asyncio.get_running_loop().create_future()
        self.keys = []
        self.error = None

    async def __call__(self, key):
        self.keys.append(key)
        self.entered.set()
        try:
            return await self.result
        except BaseException as error:
            self.error = error
            raise


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
        self.assertEqual(fetch.keys, [key])
        self.assertFalse(task.done())
        self.assertTrue(preview.pending)
        return task, fetch

    async def outcome(self, task):
        # asyncio.wait bounds observation without replacing a task's exception.
        done, _ = await asyncio.wait([task], timeout=TIMEOUT)
        self.assertIn(task, done, "refresh did not settle")
        return await task

    async def succeed(self, task, fetch, value):
        fetch.result.set_result(value)
        self.assertIs(await self.outcome(task), value)

    async def fail_call(self, task, fetch, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
            self.assertIsInstance(fetch.error, asyncio.CancelledError)
        else:
            error = RuntimeError("controlled failure")
            fetch.result.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)
            self.assertIs(fetch.error, error)

    async def seeded(self):
        preview = Preview()
        self.assertFalse(preview.pending)
        self.assertIsNone(preview.value)
        prior = object()
        task, fetch = await self.start(preview, "seed")
        await self.succeed(task, fetch, prior)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        return preview, prior

    async def test_earlier_success_while_latest_pending(self):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "same-key")
        latest, new_fetch = await self.start(preview, "same-key")
        self.assertIs(preview.value, prior)
        before_pending, before_value = preview.pending, preview.value
        await self.succeed(older, old_fetch, object())
        self.assertIs(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        self.assertFalse(latest.done())
        value = object()
        await self.succeed(latest, new_fetch, value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_latest_success_before_earlier_success(self):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "old")
        latest, new_fetch = await self.start(preview, "new")
        self.assertIs(preview.value, prior)
        value = object()
        await self.succeed(latest, new_fetch, value)
        self.assertFalse(preview.pending)
        self.assertFalse(older.done())
        self.assertIs(preview.value, value)
        before_pending, before_value = preview.pending, preview.value
        await self.succeed(older, old_fetch, object())
        self.assertIs(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)

    async def check_earlier_failure(self, cancel):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "old")
        latest, new_fetch = await self.start(preview, "new")
        self.assertIs(preview.value, prior)
        before_pending, before_value = preview.pending, preview.value
        await self.fail_call(older, old_fetch, cancel)
        self.assertIs(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        self.assertFalse(latest.done())
        value = object()
        await self.succeed(latest, new_fetch, value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_earlier_failure_while_latest_pending(self):
        await self.check_earlier_failure(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.check_earlier_failure(cancel=True)

    async def check_latest_failure_and_retry(self, cancel):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "old")
        latest, new_fetch = await self.start(preview, "new")
        self.assertIs(preview.value, prior)
        await self.fail_call(latest, new_fetch, cancel)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        retry, retry_fetch = await self.start(preview, "new")
        self.assertIs(preview.value, prior)
        before_pending, before_value = preview.pending, preview.value
        await self.succeed(older, old_fetch, object())
        self.assertIs(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        value = object()
        await self.succeed(retry, retry_fetch, value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_latest_failure_and_retry(self):
        await self.check_latest_failure_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.check_latest_failure_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded()
        older, old_fetch = await self.start(preview, "old")
        error = ValueError("synchronous failure")
        keys = []

        def fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        task = asyncio.create_task(preview.refresh("sync", fetch))
        self.tasks.append(task)
        with self.assertRaises(ValueError) as caught:
            await self.outcome(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ["sync"])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        before_pending, before_value = preview.pending, preview.value
        await self.succeed(older, old_fetch, object())
        self.assertIs(preview.pending, before_pending)
        self.assertIs(preview.value, before_value)
        retry, retry_fetch = await self.start(preview, "sync")
        self.assertIs(preview.value, prior)
        value = object()
        await self.succeed(retry, retry_fetch, value)
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, value)

    async def test_instance_isolation(self):
        first, first_prior = await self.seeded()
        second, second_prior = await self.seeded()
        first_task, first_fetch = await self.start(first, "same")
        second_task, second_fetch = await self.start(second, "same")
        self.assertIs(first.value, first_prior)
        self.assertIs(second.value, second_prior)
        second_pending, second_value = second.pending, second.value
        value = object()
        await self.succeed(first_task, first_fetch, value)
        self.assertFalse(first.pending)
        self.assertIs(first.value, value)
        self.assertIs(second.pending, second_pending)
        self.assertIs(second.value, second_value)
        self.assertFalse(second_task.done())
        first_pending, first_value = first.pending, first.value
        await self.fail_call(second_task, second_fetch, cancel=False)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertIs(first.pending, first_pending)
        self.assertIs(first.value, first_value)


if __name__ == "__main__":
    unittest.main()
