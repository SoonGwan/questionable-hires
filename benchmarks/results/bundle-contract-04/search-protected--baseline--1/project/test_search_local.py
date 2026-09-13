"""Deterministic QA for the actual Search implementation.

Run from this project: python3 -m unittest -v test_search_local
Only the standard library is required; production code is not patched.
"""

import asyncio
import unittest

from search import Search


TIMEOUT = 2.0


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.tasks = []
        self.responses = {}
        self.started = {}

    async def asyncTearDown(self):
        # Own and reap every Search task, including on assertion/timeout failure.
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            done, pending = await asyncio.wait(self.tasks, timeout=TIMEOUT)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "Search tasks did not stop after cancellation")
        for response in self.responses.values():
            if not response.done():
                response.cancel()

    async def fetch(self, query):
        self.started[query].set()
        return await self.responses[query]

    async def start(self, query):
        self.responses[query] = asyncio.get_running_loop().create_future()
        self.started[query] = asyncio.Event()
        task = asyncio.create_task(self.search.run(query, self.fetch), name=query)
        self.tasks.append(task)
        # Wait for actual fetch entry, not a guessed scheduling delay.
        await asyncio.wait_for(self.started[query].wait(), timeout=TIMEOUT)
        self.assertFalse(task.done(), f"{query} should be waiting for its response")
        return task

    async def finish(self, query, task, result):
        self.responses[query].set_result(result)
        # Observe the assignment/guard after fetch returns, not just resolution.
        await asyncio.wait_for(asyncio.shield(task), timeout=TIMEOUT)

    async def display_existing(self):
        task = await self.start("existing")
        await self.finish("existing", task, "existing result")
        self.assertEqual(self.search.result, "existing result")

    async def test_older_finishes_while_newer_pending(self):
        await self.display_existing()
        older = await self.start("older")
        newer = await self.start("newer")
        self.assertEqual(self.search.result, "existing result")

        await self.finish("older", older, "older result")
        self.assertFalse(newer.done())
        self.assertFalse(self.responses["newer"].done())
        self.assertEqual(self.search.result, "existing result")

        await self.finish("newer", newer, "newer result")
        self.assertEqual(self.search.result, "newer result")

    async def test_newer_finishes_before_older(self):
        await self.display_existing()
        older = await self.start("older")
        newer = await self.start("newer")
        self.assertEqual(self.search.result, "existing result")

        await self.finish("newer", newer, "newer result")
        self.assertFalse(older.done())
        self.assertFalse(self.responses["older"].done())
        self.assertEqual(self.search.result, "newer result")

        await self.finish("older", older, "older result")
        self.assertEqual(self.search.result, "newer result")

    async def test_existing_result_retained_while_loading(self):
        await self.display_existing()
        replacement = await self.start("replacement")
        self.assertFalse(self.responses["replacement"].done())
        self.assertEqual(self.search.result, "existing result")
        await self.finish("replacement", replacement, "replacement result")
        self.assertEqual(self.search.result, "replacement result")


if __name__ == "__main__":
    unittest.main(verbosity=2)
