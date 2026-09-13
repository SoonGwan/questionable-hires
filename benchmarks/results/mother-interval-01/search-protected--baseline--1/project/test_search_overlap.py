"""Local concurrency QA. Run: python3 -B -m unittest -v test_search_overlap

Requests advance only when their controlled future is resolved. Timeouts are
failure bounds, not sleeps used to guess whether an operation has completed.
"""

import asyncio
import unittest

from search import Search


TIMEOUT = 2.0


class ControlledFetch:
    def __init__(self, query):
        self.query = query
        self.started = asyncio.Event()
        self.response = asyncio.get_running_loop().create_future()

    async def __call__(self, query):
        if query != self.query:
            raise AssertionError(f"Expected {self.query!r}, got {query!r}")
        self.started.set()
        return await self.response


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.owned_tasks = []

    async def asyncTearDown(self):
        # Clean up only tasks this test created, including after assertion errors.
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.owned_tasks, return_exceptions=True),
                timeout=TIMEOUT,
            )

    async def start_request(self, query):
        fetch = ControlledFetch(query)
        task = asyncio.create_task(self.search.run(query, fetch), name=query)
        self.owned_tasks.append(task)
        await asyncio.wait_for(fetch.started.wait(), timeout=TIMEOUT)
        self.assertFalse(task.done())
        self.assertFalse(fetch.response.done())
        return fetch, task

    async def complete_request(self, request, result):
        fetch, task = request
        fetch.response.set_result(result)
        # Wait for Search.run to consume the result and perform its assignment.
        await asyncio.wait_for(asyncio.shield(task), timeout=TIMEOUT)
        self.assertTrue(task.done())

    def assert_pending(self, request):
        fetch, task = request
        self.assertFalse(fetch.response.done())
        self.assertFalse(task.done())

    async def test_newer_then_older_keeps_newer_result(self):
        older = await self.start_request("older")
        newer = await self.start_request("newer")
        self.assertIsNone(self.search.result)

        await self.complete_request(newer, "newer result")
        self.assertEqual(self.search.result, "newer result")
        self.assert_pending(older)

        await self.complete_request(older, "older result")
        self.assertEqual(self.search.result, "newer result")

    async def test_older_then_newer_ignores_older_while_newer_pending(self):
        older = await self.start_request("older")
        newer = await self.start_request("newer")

        await self.complete_request(older, "older result")
        self.assert_pending(newer)
        self.assertIsNone(self.search.result)

        await self.complete_request(newer, "newer result")
        self.assertEqual(self.search.result, "newer result")

    async def test_existing_result_retained_through_overlapping_loading(self):
        existing = await self.start_request("existing")
        await self.complete_request(existing, "existing result")
        self.assertEqual(self.search.result, "existing result")

        older = await self.start_request("older")
        self.assertEqual(self.search.result, "existing result")
        newer = await self.start_request("newer")
        self.assert_pending(older)
        self.assert_pending(newer)
        self.assertEqual(self.search.result, "existing result")

        await self.complete_request(older, "older result")
        self.assert_pending(newer)
        self.assertEqual(self.search.result, "existing result")

        await self.complete_request(newer, "newer result")
        self.assertEqual(self.search.result, "newer result")


if __name__ == "__main__":
    unittest.main(verbosity=2)
