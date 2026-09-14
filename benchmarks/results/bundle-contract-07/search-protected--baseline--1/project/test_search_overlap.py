"""Local QA: run with python3 -B -m unittest -v test_search_overlap.

Uses the real Search and explicitly completed futures; no network or sleeps.
"""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 2.0

    async def asyncSetUp(self):
        self.search = Search()
        self.entered = asyncio.Queue()
        self.futures = {}
        self.tasks = []

    async def asyncTearDown(self):
        # Own and settle only tasks/futures created by this test, even on failure.
        for task in self.tasks:
            if not task.done():
                task.cancel()
        for future in self.futures.values():
            if not future.done():
                future.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), self.TIMEOUT
            )

    async def fetch(self, query):
        self.entered.put_nowait(query)
        return await self.futures[query]

    async def start(self, query):
        self.futures[query] = asyncio.get_running_loop().create_future()
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        # The fetch-entry signal establishes request order, not elapsed time.
        entered = await asyncio.wait_for(self.entered.get(), self.TIMEOUT)
        self.assertEqual(entered, query)
        self.assertFalse(task.done())
        self.assertFalse(self.futures[query].done())
        return task

    async def complete(self, query, task, result):
        self.futures[query].set_result(result)
        # Await actual processing of the completion, with a failure deadline.
        await asyncio.wait_for(asyncio.shield(task), self.TIMEOUT)

    async def seed_and_overlap(self):
        seed = await self.start("seed")
        self.assertIsNone(self.search.result)
        await self.complete("seed", seed, "existing result")
        self.assertEqual(self.search.result, "existing result")
        older = await self.start("older")
        self.assertEqual(self.search.result, "existing result")
        newer = await self.start("newer")
        self.assertEqual(self.search.result, "existing result")
        self.assertFalse(older.done())
        self.assertFalse(newer.done())
        return older, newer

    async def test_older_completes_while_newer_pending(self):
        older, newer = await self.seed_and_overlap()
        await self.complete("older", older, "older result")
        self.assertFalse(newer.done())
        self.assertFalse(self.futures["newer"].done())
        self.assertEqual(self.search.result, "existing result")
        await self.complete("newer", newer, "newer result")
        self.assertEqual(self.search.result, "newer result")

    async def test_newer_completes_before_older(self):
        older, newer = await self.seed_and_overlap()
        await self.complete("newer", newer, "newer result")
        self.assertFalse(older.done())
        self.assertFalse(self.futures["older"].done())
        self.assertEqual(self.search.result, "newer result")
        await self.complete("older", older, "older result")
        self.assertEqual(self.search.result, "newer result")


if __name__ == "__main__":
    unittest.main(verbosity=2)
