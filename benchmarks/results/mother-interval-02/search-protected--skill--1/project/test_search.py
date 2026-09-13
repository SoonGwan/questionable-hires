"""Deterministic Search QA; run: python3 -B -m unittest -v test_search.

Contract under test: the latest invocation owns the result, and an existing
displayed result is retained throughout loading until that invocation completes.
Tests exercise the actual component with controlled, local fetch futures.
"""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.owned_tasks = []
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            done, pending = await asyncio.wait(self.owned_tasks, timeout=1)
            # Retrieve outcomes, including after failed request-entry checks.
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned Search tasks did not stop in 1s")

    async def start_request(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned_tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        return task, request

    async def complete_request(self, task, request, payload):
        request.complete(payload)
        done, pending = await asyncio.wait([task], timeout=1)
        self.assertFalse(pending, "Search did not finish within 1s of response")
        self.assertIn(task, done)
        task.result()

    async def seed_display(self):
        task, request = await self.start_request("seed")
        self.assertIsNone(self.search.result)
        await self.complete_request(task, request, "existing result")
        self.assertEqual(self.search.result, "existing result")

    async def start_overlap(self):
        await self.seed_display()
        older = await self.start_request("older")
        self.assertEqual(self.search.result, "existing result")
        newer = await self.start_request("newer")
        self.assertEqual(self.search.result, "existing result")
        self.assertFalse(older[0].done())
        self.assertFalse(newer[0].done())
        return older, newer

    async def test_single_request_retains_display_until_completion(self):
        await self.seed_display()
        task, request = await self.start_request("replacement")
        self.assertFalse(task.done())
        self.assertEqual(self.search.result, "existing result")
        await self.complete_request(task, request, "replacement result")
        self.assertEqual(self.search.result, "replacement result")

    async def test_older_completes_while_newer_pending_retains_display(self):
        older, newer = await self.start_overlap()
        await self.complete_request(*older, "older result")
        self.assertFalse(newer[0].done())
        self.assertFalse(newer[1].response.done())
        self.assertEqual(
            self.search.result, "existing result",
            "older completion must retain the display while latest is pending",
        )
        await self.complete_request(*newer, "newer result")
        self.assertEqual(self.search.result, "newer result")

    async def test_newer_completes_first_late_older_cannot_overwrite(self):
        older, newer = await self.start_overlap()
        await self.complete_request(*newer, "newer result")
        self.assertFalse(older[0].done())
        self.assertEqual(self.search.result, "newer result")
        await self.complete_request(*older, "older result")
        self.assertEqual(self.search.result, "newer result")


if __name__ == "__main__":
    unittest.main()
