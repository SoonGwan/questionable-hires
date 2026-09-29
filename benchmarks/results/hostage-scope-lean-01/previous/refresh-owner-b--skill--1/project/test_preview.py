import asyncio
import unittest

from preview import Preview


TIMEOUT = 2


class ControlledFetch:
    def __init__(self):
        self.calls = asyncio.Queue()

    async def __call__(self, key):
        result = asyncio.get_running_loop().create_future()
        self.calls.put_nowait((key, result))
        return await result


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

    async def seeded_preview(self):
        preview = Preview()
        prior = object()

        async def fetch(key):
            self.assertEqual(key, "seed")
            return prior

        self.assertIs(await asyncio.wait_for(preview.refresh("seed", fetch), TIMEOUT), prior)
        self.assert_state(preview, False, prior)
        return preview, prior

    async def start_refresh(self, preview, fetch, key):
        task = asyncio.create_task(preview.refresh(key, fetch))
        self.tasks.append(task)
        actual_key, result = await asyncio.wait_for(fetch.calls.get(), TIMEOUT)
        self.assertEqual(actual_key, key)
        return task, result

    async def complete(self, task, result, value):
        result.set_result(value)
        self.assertIs(await asyncio.wait_for(task, TIMEOUT), value)

    async def reject(self, task, result, error):
        result.set_exception(error)
        with self.assertRaises(type(error)) as raised:
            await asyncio.wait_for(task, TIMEOUT)
        self.assertIs(raised.exception, error)

    async def cancel_refresh(self, task):
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, TIMEOUT)

    def assert_state(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def test_initial_state(self):
        self.assert_state(Preview(), False, None)

    async def test_success_earlier_completes_first(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledFetch()
        # Equal keys must still invoke both callbacks concurrently.
        earlier, earlier_result = await self.start_refresh(preview, fetch, "same")
        latest, latest_result = await self.start_refresh(preview, fetch, "same")
        self.assert_state(preview, True, prior)
        pending_before, value_before = preview.pending, preview.value
        await self.complete(earlier, earlier_result, object())
        self.assert_state(preview, pending_before, value_before)
        self.assertFalse(latest.done())
        published = object()
        await self.complete(latest, latest_result, published)
        self.assert_state(preview, False, published)

    async def test_success_latest_completes_first(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledFetch()
        earlier, earlier_result = await self.start_refresh(preview, fetch, "earlier")
        latest, latest_result = await self.start_refresh(preview, fetch, "latest")
        self.assert_state(preview, True, prior)
        published = object()
        await self.complete(latest, latest_result, published)
        self.assert_state(preview, False, published)
        self.assertFalse(earlier.done())
        pending_before, value_before = preview.pending, preview.value
        await self.complete(earlier, earlier_result, object())
        self.assert_state(preview, pending_before, value_before)

    async def earlier_unsuccessful(self, cancel):
        preview, prior = await self.seeded_preview()
        fetch = ControlledFetch()
        earlier, earlier_result = await self.start_refresh(preview, fetch, "earlier")
        latest, latest_result = await self.start_refresh(preview, fetch, "latest")
        self.assert_state(preview, True, prior)
        pending_before, value_before = preview.pending, preview.value
        if cancel:
            await self.cancel_refresh(earlier)
        else:
            await self.reject(earlier, earlier_result, RuntimeError("earlier failed"))
        self.assert_state(preview, pending_before, value_before)
        self.assertFalse(latest.done())
        published = object()
        await self.complete(latest, latest_result, published)
        self.assert_state(preview, False, published)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        preview, prior = await self.seeded_preview()
        fetch = ControlledFetch()
        earlier, earlier_result = await self.start_refresh(preview, fetch, "earlier")
        latest, latest_result = await self.start_refresh(preview, fetch, "latest")
        self.assert_state(preview, True, prior)
        if cancel:
            await self.cancel_refresh(latest)
        else:
            await self.reject(latest, latest_result, RuntimeError("latest failed"))
        self.assert_state(preview, False, prior)
        self.assertFalse(earlier.done())
        # A stale success after latest failure must not replace the prior display.
        pending_before, value_before = preview.pending, preview.value
        await self.complete(earlier, earlier_result, object())
        self.assert_state(preview, pending_before, value_before)
        retry, retry_result = await self.start_refresh(preview, fetch, "latest")
        self.assert_state(preview, True, prior)
        published = object()
        await self.complete(retry, retry_result, published)
        self.assert_state(preview, False, published)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        preview, prior = await self.seeded_preview()
        fetch = ControlledFetch()
        earlier, earlier_result = await self.start_refresh(preview, fetch, "earlier")
        error = ValueError("synchronous failure")
        calls = []

        def broken_fetch(key):
            calls.append(key)
            self.assert_state(preview, True, prior)
            raise error

        with self.assertRaises(ValueError) as raised:
            await asyncio.wait_for(preview.refresh("broken", broken_fetch), TIMEOUT)
        self.assertIs(raised.exception, error)
        self.assertEqual(calls, ["broken"])
        self.assert_state(preview, False, prior)
        self.assertFalse(earlier.done())
        retry, retry_result = await self.start_refresh(preview, fetch, "broken")
        self.assert_state(preview, True, prior)
        pending_before, value_before = preview.pending, preview.value
        await self.complete(earlier, earlier_result, object())
        self.assert_state(preview, pending_before, value_before)
        self.assertFalse(retry.done())
        published = object()
        await self.complete(retry, retry_result, published)
        self.assert_state(preview, False, published)

    async def test_instance_isolation(self):
        first, first_prior = await self.seeded_preview()
        second, second_prior = await self.seeded_preview()
        fetch = ControlledFetch()
        first_task, first_result = await self.start_refresh(first, fetch, "first")
        self.assert_state(second, False, second_prior)
        second_task, second_result = await self.start_refresh(second, fetch, "second")
        first_pending, first_value = first.pending, first.value
        second_value = object()
        await self.complete(second_task, second_result, second_value)
        self.assert_state(second, False, second_value)
        self.assert_state(first, first_pending, first_value)
        self.assert_state(first, True, first_prior)
        first_value = object()
        await self.complete(first_task, first_result, first_value)
        self.assert_state(first, False, first_value)
        self.assert_state(second, False, second_value)


if __name__ == "__main__":
    unittest.main()
