import asyncio
import gc
import unittest
import weakref

from shared import Loader


class ConcurrentLoads(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.owned = set()
        self.entries = asyncio.Queue()
        self.addAsyncCleanup(self.drain_owned)

        async def fetch(key):
            self.owned.add(asyncio.current_task())
            response = asyncio.get_running_loop().create_future()
            self.entries.put_nowait((key, response, asyncio.current_task()))
            return await response

        self.loader = Loader(fetch)

    async def drain_owned(self):
        for task in self.owned:
            if not task.done():
                task.cancel()
        if self.owned:
            done, pending = await asyncio.wait(self.owned, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned tasks did not stop")

    async def start_load(self, key="one"):
        task = asyncio.create_task(self.loader.load(key))
        self.owned.add(task)
        # Give the caller a turn to enter load and attach to its fetch.
        await asyncio.sleep(0)
        return task

    async def entry(self, key="one"):
        actual_key, response, task = await asyncio.wait_for(
            self.entries.get(), timeout=1
        )
        self.assertEqual(actual_key, key)
        return response, task

    async def outcome(self, task):
        return await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def cancel_caller(self, task):
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.outcome(task)
        self.assertTrue(task.cancelled())

    async def test_shared_completion_and_no_completed_cache(self):
        first = await self.start_load()
        response, fetch = await self.entry()
        second = await self.start_load()
        self.assertFalse(first.done())
        self.assertFalse(second.done())
        self.assertIs(self.loader._inflight["one"], fetch)
        self.assertTrue(self.entries.empty())
        value = object()
        response.set_result(value)
        self.assertIs(await self.outcome(first), value)
        self.assertIs(await self.outcome(second), value)
        self.assertEqual(self.loader._inflight, {})

        later = await self.start_load()
        next_response, next_fetch = await self.entry()
        self.assertIsNot(next_fetch, fetch)
        next_value = object()
        next_response.set_result(next_value)
        self.assertIs(await self.outcome(later), next_value)

    async def test_cancel_one_preserves_fetch_and_late_joiner(self):
        first = await self.start_load()
        response, fetch = await self.entry()
        second = await self.start_load()
        await self.cancel_caller(first)
        third = await self.start_load()
        self.assertFalse(fetch.done())
        self.assertFalse(response.cancelled())
        self.assertFalse(second.done())
        self.assertFalse(third.done())
        self.assertIs(self.loader._inflight["one"], fetch)
        self.assertTrue(self.entries.empty())
        value = object()
        response.set_result(value)
        self.assertIs(await self.outcome(second), value)
        self.assertIs(await self.outcome(third), value)

    async def test_all_cancel_then_new_caller_joins_active_fetch(self):
        first = await self.start_load()
        response, fetch = await self.entry()
        second = await self.start_load()
        await self.cancel_caller(first)
        await self.cancel_caller(second)
        self.assertFalse(fetch.done())
        self.assertIs(self.loader._inflight["one"], fetch)
        later = await self.start_load()
        self.assertTrue(self.entries.empty())
        self.assertFalse(later.done())
        value = object()
        response.set_result(value)
        self.assertIs(await self.outcome(later), value)

    async def test_shared_failure_identity_and_retry(self):
        first = await self.start_load()
        response, _ = await self.entry()
        second = await self.start_load()
        error = RuntimeError("fetch failed")
        response.set_exception(error)
        for caller in (first, second):
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(caller)
            self.assertIs(caught.exception, error)
        self.assertEqual(self.loader._inflight, {})
        retry = await self.start_load()
        retry_response, _ = await self.entry()
        value = object()
        retry_response.set_result(value)
        self.assertIs(await self.outcome(retry), value)

    async def check_abandoned_completion(self, error=None):
        loop = asyncio.get_running_loop()
        reports = []
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda loop, context: reports.append(context))
        self.addCleanup(loop.set_exception_handler, previous_handler)
        first = await self.start_load()
        response, fetch = await self.entry()
        second = await self.start_load()
        await self.cancel_caller(first)
        await self.cancel_caller(second)
        self.assertFalse(fetch.done())
        self.assertIs(self.loader._inflight["one"], fetch)
        if error is None:
            response.set_result(object())
        else:
            response.set_exception(error)
        # Wait for completion without retrieving the task's exception ourselves.
        done, pending = await asyncio.wait({fetch}, timeout=1)
        self.assertFalse(pending)
        self.assertFalse(fetch.cancelled())
        self.assertEqual(self.loader._inflight, {})
        reference = weakref.ref(fetch)
        self.owned.remove(fetch)
        # Cancelled callers can retain load's frame through their traceback.
        self.owned.difference_update((first, second))
        done.clear()
        del fetch, first, second
        gc.collect()
        self.assertIsNone(reference(), "completed fetch is still retained")
        self.assertEqual(reports, [], "abandoned failure was not observed")

        retry = await self.start_load()
        retry_response, _ = await self.entry()
        value = object()
        retry_response.set_result(value)
        self.assertIs(await self.outcome(retry), value)

    async def test_abandoned_success_clears_for_next_load(self):
        await self.check_abandoned_completion()

    async def test_abandoned_failure_is_observed_and_allows_retry(self):
        await self.check_abandoned_completion(RuntimeError("abandoned failure"))

    async def test_different_keys_complete_independently(self):
        first = await self.start_load("one")
        first_response, first_fetch = await self.entry("one")
        second = await self.start_load("two")
        second_response, second_fetch = await self.entry("two")
        self.assertIsNot(first_fetch, second_fetch)
        await self.cancel_caller(first)
        value = object()
        second_response.set_result(value)
        self.assertIs(await self.outcome(second), value)
        self.assertFalse(first_fetch.done())
        self.assertIs(self.loader._inflight["one"], first_fetch)
        self.assertNotIn("two", self.loader._inflight)
        later = await self.start_load("one")
        self.assertTrue(self.entries.empty())
        first_value = object()
        first_response.set_result(first_value)
        self.assertIs(await self.outcome(later), first_value)
