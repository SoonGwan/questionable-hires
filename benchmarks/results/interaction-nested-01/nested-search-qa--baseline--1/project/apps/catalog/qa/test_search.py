import asyncio
import unittest

from search import Search


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def test_normal_sequence_including_empty_query(self):
        search = Search()
        responses = {"b": ["book", "bag"], "": [], "book": ["book"]}
        calls = []

        async def fetch(query):
            calls.append(query)
            return responses[query]

        for query in ("b", "", "book"):
            await search.run(query, fetch)
            self.assertEqual(search.result, responses[query])
        self.assertEqual(calls, ["b", "", "book"])

    async def check_overlapping_queries(self, latest_query, latest_result):
        search = Search()
        loop = asyncio.get_running_loop()
        queries = ("b", latest_query)
        started = {query: asyncio.Event() for query in queries}
        responses = {query: loop.create_future() for query in queries}
        tasks = []

        async def fetch(query):
            started[query].set()
            return await responses[query]

        try:
            for query in queries:
                tasks.append(asyncio.create_task(search.run(query, fetch)))
                await asyncio.wait_for(started[query].wait(), timeout=0.5)

            # The latest query finishes first; no timing sleeps are involved.
            responses[latest_query].set_result(latest_result)
            await asyncio.wait_for(tasks[1], timeout=0.5)
            self.assertEqual(search.result, latest_result)

            responses["b"].set_result(["book", "bag"])
            await asyncio.wait_for(tasks[0], timeout=0.5)
            self.assertEqual(
                search.result,
                latest_result,
                f"Older 'b' response replaced latest {latest_query!r} result",
            )
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    async def test_latest_nonempty_query_survives_older_response(self):
        await self.check_overlapping_queries("book", ["book"])

    async def test_cleared_query_survives_older_response(self):
        await self.check_overlapping_queries("", [])
