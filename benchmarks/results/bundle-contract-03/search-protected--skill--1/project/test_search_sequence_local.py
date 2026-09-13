"""Deterministic component QA: python3 -B test_search_sequence_local.py"""

import asyncio
import unittest

from search import Search


TIMEOUT = 5


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
    async def check_order(self, first, seeded):
        search = Search()
        tasks = []
        loop = asyncio.get_running_loop()
        queries = ["seed", "old", "new"]
        replies = {query: loop.create_future() for query in queries}
        started = {query: asyncio.Event() for query in queries}

        async def fetch(query):
            started[query].set()
            return await replies[query]

        async def start(query):
            task = asyncio.create_task(search.run(query, fetch))
            tasks.append(task)
            await asyncio.wait_for(started[query].wait(), TIMEOUT)
            return task

        async def complete(query, task):
            replies[query].set_result(query + " result")
            await asyncio.wait_for(asyncio.shield(task), TIMEOUT)

        try:
            if seeded:
                seed = await start("seed")
                await complete("seed", seed)
            previous = "seed result" if seeded else None
            self.assertEqual(search.result, previous, "initial displayed state")

            old = await start("old")
            self.assertEqual(search.result, previous, "retain state while old loads")
            new = await start("new")
            self.assertFalse(old.done())
            self.assertFalse(new.done())
            self.assertEqual(search.result, previous, "retain state while both load")

            if first == "old":
                await complete("old", old)
                self.assertFalse(new.done(), "new request must remain pending")
                self.assertFalse(replies["new"].done())
                self.assertEqual(search.result, previous, "ignore old while new pending")
                await complete("new", new)
            else:
                await complete("new", new)
                self.assertFalse(old.done(), "old request must remain pending")
                self.assertEqual(search.result, "new result", "publish newest result")
                await complete("old", old)
            self.assertEqual(search.result, "new result", "latest result wins")
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            for reply in replies.values():
                if not reply.done():
                    reply.cancel()
            if tasks:
                await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True), TIMEOUT
                )

    async def test_old_then_new_from_empty(self):
        await self.check_order("old", seeded=False)

    async def test_new_then_old_from_empty(self):
        await self.check_order("new", seeded=False)

    async def test_old_then_new_retains_displayed_result(self):
        await self.check_order("old", seeded=True)

    async def test_new_then_old_retains_displayed_result(self):
        await self.check_order("new", seeded=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
