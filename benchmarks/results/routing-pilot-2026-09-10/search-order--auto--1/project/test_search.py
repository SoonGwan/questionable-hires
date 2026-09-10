import asyncio
import unittest

from search import Search


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def test_latest_query_remains_visible_when_older_request_finishes_last(self):
        search = Search()
        queries = ("ca", "cat")
        loop = asyncio.get_running_loop()
        responses = {query: loop.create_future() for query in queries}
        started = {query: asyncio.Event() for query in queries}

        async def fetch(query):
            started[query].set()
            return await responses[query]

        tasks = []
        try:
            # The user types again while the first request is still pending.
            for query in queries:
                tasks.append(asyncio.create_task(search.run(query, fetch)))
                await started[query].wait()

            responses["cat"].set_result(["cat result"])
            await tasks[1]
            self.assertEqual(search.result, ["cat result"])

            # A slower response for the earlier input must not replace it.
            responses["ca"].set_result(["ca result"])
            await tasks[0]
            self.assertEqual(
                search.result,
                ["cat result"],
                "An older response replaced the latest query's visible result",
            )
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    unittest.main()
