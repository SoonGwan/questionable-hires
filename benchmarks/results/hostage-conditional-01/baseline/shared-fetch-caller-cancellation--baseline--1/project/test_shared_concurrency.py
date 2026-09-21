import asyncio
import gc
import unittest
import weakref

from shared import Loader


class ConcurrentLoads(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = set()
        self.calls = []
        self.started = {}
        self.release = {}
        self.results = {}
        self.failures = {}

        async def fetch(key):
            self.tasks.add(asyncio.current_task())
            self.calls.append(key)
            self.started[key].set()
            await self.release[key].wait()
            if key in self.failures:
                raise self.failures[key]
            return self.results[key]

        self.loader = Loader(fetch)

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), 2
            )

    def prepare(self, key, failure=None):
        self.started[key] = asyncio.Event()
        self.release[key] = asyncio.Event()
        self.results[key] = object()
        self.failures.pop(key, None)
        if failure is not None:
            self.failures[key] = failure
        return self.results[key]

    async def caller(self, key):
        entered = asyncio.Event()

        async def load():
            entered.set()
            return await self.loader.load(key)

        task = asyncio.create_task(load())
        self.tasks.add(task)
        await asyncio.wait_for(entered.wait(), 2)
        await asyncio.wait_for(self.started[key].wait(), 2)
        return task

    async def cancel(self, task):
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, 2)

    async def finish_fetch(self, task, key):
        # Wait for completion callbacks without retrieving the fetch exception.
        completed = asyncio.Event()
        task.add_done_callback(lambda unused: completed.set())
        self.release[key].set()
        await asyncio.wait_for(completed.wait(), 2)

    async def test_cancel_one_caller_and_join_active_fetch(self):
        value = self.prepare("one")
        first = await self.caller("one")
        second = await self.caller("one")
        fetch = self.loader._inflight["one"]
        await self.cancel(first)
        third = await self.caller("one")
        self.assertIs(self.loader._inflight["one"], fetch)
        self.assertEqual(self.calls, ["one"])
        self.assertFalse(fetch.done())
        self.assertFalse(second.done())
        self.release["one"].set()
        results = await asyncio.wait_for(asyncio.gather(second, third), 2)
        self.assertTrue(all(result is value for result in results))
        self.assertEqual(self.loader._inflight, {})

    async def test_all_cancel_then_late_caller_joins_and_results_are_not_cached(self):
        value = self.prepare("one")
        first = await self.caller("one")
        second = await self.caller("one")
        fetch = self.loader._inflight["one"]
        await self.cancel(first)
        await self.cancel(second)
        self.assertFalse(fetch.done())
        late = await self.caller("one")
        self.assertEqual(self.calls, ["one"])
        self.release["one"].set()
        self.assertIs(await asyncio.wait_for(late, 2), value)
        next_value = self.prepare("one")
        retry = await self.caller("one")
        self.release["one"].set()
        self.assertIs(await asyncio.wait_for(retry, 2), next_value)
        self.assertEqual(self.calls, ["one", "one"])

    async def test_abandoned_success_finishes_and_clears(self):
        self.prepare("one")
        caller = await self.caller("one")
        fetch = self.loader._inflight["one"]
        await self.cancel(caller)
        self.assertFalse(fetch.done())
        await self.finish_fetch(fetch, "one")
        self.assertFalse(fetch.cancelled())
        self.assertEqual(self.loader._inflight, {})

    async def test_abandoned_failure_is_observed_and_can_retry(self):
        loop = asyncio.get_running_loop()
        previous_handler = loop.get_exception_handler()
        unhandled = []
        loop.set_exception_handler(lambda loop, context: unhandled.append(context))
        try:
            self.prepare("one", RuntimeError("fetch failed"))
            first = await self.caller("one")
            second = await self.caller("one")
            fetch = self.loader._inflight["one"]
            await self.cancel(first)
            await self.cancel(second)
            self.assertFalse(fetch.done())
            await self.finish_fetch(fetch, "one")
            self.assertFalse(fetch.cancelled())
            self.assertEqual(self.loader._inflight, {})
            fetch_ref = weakref.ref(fetch)
            self.tasks.remove(fetch)
            # Cancelled callers can retain load's frame (and its fetch task).
            self.tasks.remove(first)
            self.tasks.remove(second)
            del fetch, first, second
            gc.collect()
            self.assertIsNone(fetch_ref())
            self.assertEqual(unhandled, [])
            value = self.prepare("one")
            retry = await self.caller("one")
            self.release["one"].set()
            self.assertIs(await asyncio.wait_for(retry, 2), value)
            self.assertEqual(self.calls, ["one", "one"])
        finally:
            loop.set_exception_handler(previous_handler)

    async def test_fetch_error_identity_and_retry(self):
        error = RuntimeError("fetch failed")
        self.prepare("one", error)
        first = await self.caller("one")
        second = await self.caller("one")
        self.release["one"].set()
        errors = await asyncio.wait_for(
            asyncio.gather(first, second, return_exceptions=True), 2
        )
        self.assertTrue(all(result is error for result in errors))
        self.assertEqual(self.loader._inflight, {})
        value = self.prepare("one")
        retry = await self.caller("one")
        self.release["one"].set()
        self.assertIs(await asyncio.wait_for(retry, 2), value)
        self.assertEqual(self.calls, ["one", "one"])

    async def test_different_keys_complete_independently(self):
        first_value = self.prepare("one")
        second_value = self.prepare("two")
        first = await self.caller("one")
        cancelled = await self.caller("one")
        second = await self.caller("two")
        await self.cancel(cancelled)
        self.release["two"].set()
        self.assertIs(await asyncio.wait_for(second, 2), second_value)
        self.assertFalse(first.done())
        self.assertEqual(set(self.loader._inflight), {"one"})
        self.release["one"].set()
        self.assertIs(await asyncio.wait_for(first, 2), first_value)
        self.assertEqual(self.calls, ["one", "two"])
        self.assertEqual(self.loader._inflight, {})
