"""Deterministic local QA: python3 -B -m unittest -v test_search_local.py."""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 2.0

    async def asyncSetUp(self):
        self.search = Search()
        self.tasks = []
        self.replies = {}
        self.entered = {}

    async def asyncTearDown(self):
        # Own and drain only this test's tasks, including on assertion failure.
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True),
                timeout=self.TIMEOUT,
            )
        for reply in self.replies.values():
            if not reply.done():
                reply.cancel()

    async def fetch(self, query):
        self.entered[query].set()
        return await self.replies[query]

    async def start(self, query):
        self.replies[query] = asyncio.get_running_loop().create_future()
        self.entered[query] = asyncio.Event()
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        # Wait for actual fetch entry, not an arbitrary sleep or scheduler count.
        await asyncio.wait_for(self.entered[query].wait(), self.TIMEOUT)
        self.assertFalse(task.done())
        return task

    async def complete(self, query, value, task):
        self.replies[query].set_result(value)
        # Completion means Search has consumed the reply and applied its guard.
        await asyncio.wait_for(asyncio.shield(task), self.TIMEOUT)
        self.assertTrue(task.done())

    async def check_order(self, first, with_existing):
        existing = None
        if with_existing:
            existing = "previously displayed result"
            seed = await self.start("seed")
            await self.complete("seed", existing, seed)
            self.assertEqual(self.search.result, existing)

        older = await self.start("older")
        self.assertEqual(self.search.result, existing)
        newer = await self.start("newer")
        self.assertEqual(self.search.result, existing)
        self.assertFalse(older.done())
        self.assertFalse(newer.done())

        if first == "older":
            await self.complete("older", "older result", older)
            self.assertFalse(newer.done())
            self.assertFalse(self.replies["newer"].done())
            # A stale completion must not appear even temporarily while loading.
            self.assertEqual(self.search.result, existing)
            await self.complete("newer", "newer result", newer)
        else:
            await self.complete("newer", "newer result", newer)
            self.assertFalse(older.done())
            self.assertFalse(self.replies["older"].done())
            self.assertEqual(self.search.result, "newer result")
            await self.complete("older", "older result", older)

        self.assertEqual(self.search.result, "newer result")

    async def test_older_finishes_first_empty(self):
        await self.check_order("older", with_existing=False)

    async def test_newer_finishes_first_empty(self):
        await self.check_order("newer", with_existing=False)

    async def test_older_finishes_first_retains_displayed_result(self):
        await self.check_order("older", with_existing=True)

    async def test_newer_finishes_first_retains_displayed_result(self):
        await self.check_order("newer", with_existing=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
