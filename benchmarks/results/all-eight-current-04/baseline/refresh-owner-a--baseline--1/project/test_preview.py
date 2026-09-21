import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    def __init__(self):
        self.called = asyncio.Event()
        self.result = asyncio.get_running_loop().create_future()
        self.keys = []

    async def __call__(self, key):
        self.keys.append(key)
        self.called.set()
        return await self.result


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.preview = Preview()
        self.prior = object()
        self.assertFalse(self.preview.pending)
        self.assertIsNone(self.preview.value)
        await self.publish(self.preview, self.prior)

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), TIMEOUT
            )

    async def finish(self, task):
        # Shield keeps a timeout from masquerading as application cancellation.
        return await asyncio.wait_for(asyncio.shield(task), TIMEOUT)

    async def start(self, fetch, key, preview=None):
        if preview is None:
            preview = self.preview
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        await asyncio.wait_for(fetch.called.wait(), TIMEOUT)
        self.assertEqual(fetch.keys, [key])
        self.assertFalse(task.done())
        self.assertTrue(preview.pending)
        return task

    async def publish(self, preview, value):
        async def fetch(key):
            self.assertTrue(preview.pending)
            return value

        task = asyncio.create_task(preview.refresh(object(), fetch))
        self.tasks.append(task)
        self.assertIs(await self.finish(task), value)
        self.assertIs(preview.value, value)
        self.assertFalse(preview.pending)

    async def pair(self):
        older_fetch, latest_fetch = ControlledFetch(), ControlledFetch()
        # Identical keys must still invoke both supplied callbacks concurrently.
        key = object()
        older = await self.start(older_fetch, key)
        latest = await self.start(latest_fetch, key)
        self.assertFalse(older.done())
        self.assertIs(self.preview.value, self.prior)
        return older_fetch, older, latest_fetch, latest

    async def test_earlier_success_then_latest_success(self):
        old_fetch, old, new_fetch, new = await self.pair()
        old_value, new_value = object(), object()
        old_fetch.result.set_result(old_value)
        self.assertIs(await self.finish(old), old_value)
        self.assertFalse(new.done())
        self.assertTrue(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        new_fetch.result.set_result(new_value)
        self.assertIs(await self.finish(new), new_value)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, new_value)

    async def test_latest_success_then_earlier_success(self):
        old_fetch, old, new_fetch, new = await self.pair()
        old_value, new_value = object(), object()
        new_fetch.result.set_result(new_value)
        self.assertIs(await self.finish(new), new_value)
        self.assertFalse(old.done())
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, new_value)
        old_fetch.result.set_result(old_value)
        self.assertIs(await self.finish(old), old_value)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, new_value)

    async def settle_unsuccessfully(self, fetch, task, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.finish(task)
        else:
            error = RuntimeError("controlled failure")
            fetch.result.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.finish(task)
            self.assertIs(caught.exception, error)

    async def earlier_unsuccessful(self, cancel):
        old_fetch, old, new_fetch, new = await self.pair()
        await self.settle_unsuccessfully(old_fetch, old, cancel)
        self.assertFalse(new.done())
        self.assertFalse(new_fetch.result.done())
        self.assertTrue(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        value = object()
        new_fetch.result.set_result(value)
        self.assertIs(await self.finish(new), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        old_fetch, old, new_fetch, new = await self.pair()
        await self.settle_unsuccessfully(new_fetch, new, cancel)
        self.assertFalse(old.done())
        self.assertFalse(old_fetch.result.done())
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        retry_fetch = ControlledFetch()
        retry = await self.start(retry_fetch, object())
        self.assertIs(self.preview.value, self.prior)
        old_value = object()
        old_fetch.result.set_result(old_value)
        self.assertIs(await self.finish(old), old_value)
        self.assertTrue(self.preview.pending)
        self.assertFalse(retry.done())
        self.assertIs(self.preview.value, self.prior)
        retry_value = object()
        retry_fetch.result.set_result(retry_value)
        self.assertIs(await self.finish(retry), retry_value)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, retry_value)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        old_fetch = ControlledFetch()
        old = await self.start(old_fetch, object())
        key, error = object(), LookupError("synchronous failure")
        calls = []

        def fail(actual_key):
            calls.append(actual_key)
            self.assertTrue(self.preview.pending)
            self.assertIs(self.preview.value, self.prior)
            raise error

        task = asyncio.create_task(self.preview.refresh(key, fail))
        self.tasks.append(task)
        with self.assertRaises(LookupError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(calls, [key])
        self.assertFalse(self.preview.pending)
        self.assertFalse(old.done())
        self.assertIs(self.preview.value, self.prior)
        value = object()
        await self.publish(self.preview, value)
        old_value = object()
        old_fetch.result.set_result(old_value)
        self.assertIs(await self.finish(old), old_value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_instances_are_independent(self):
        other = Preview()
        other_prior = object()
        await self.publish(other, other_prior)
        first_fetch, second_fetch = ControlledFetch(), ControlledFetch()
        first = await self.start(first_fetch, object())
        second = await self.start(second_fetch, object(), other)
        self.assertTrue(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        self.assertIs(other.value, other_prior)
        first_value = object()
        first_fetch.result.set_result(first_value)
        self.assertIs(await self.finish(first), first_value)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, first_value)
        self.assertTrue(other.pending)
        self.assertFalse(second.done())
        self.assertIs(other.value, other_prior)
        second_value = object()
        second_fetch.result.set_result(second_value)
        self.assertIs(await self.finish(second), second_value)
        self.assertFalse(other.pending)
        self.assertIs(other.value, second_value)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, first_value)


if __name__ == "__main__":
    unittest.main()
