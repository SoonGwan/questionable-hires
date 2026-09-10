import asyncio
import unittest

from search import Search


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def test_latest_query_remains_visible_when_older_response_arrives_last(self):
        search = Search()
        queries = ("cat", "cats")
        started = {query: asyncio.Event() for query in queries}
        responses = {
            query: asyncio.get_running_loop().create_future() for query in queries
        }

        async def fetch(query):
            started[query].set()
            return await responses[query]

        tasks = []
        try:
            # The user types another character while the first request is pending.
            for query in queries:
                tasks.append(asyncio.create_task(search.run(query, fetch)))
                await started[query].wait()

            # The newer request finishes first and its result is displayed.
            responses["cats"].set_result("results for cats")
            await tasks[1]
            self.assertEqual(search.result, "results for cats")

            # A delayed response for the previous query must not replace it.
            responses["cat"].set_result("results for cat")
            await tasks[0]
            self.assertEqual(
                search.result,
                "results for cats",
                "An older response overwrote the latest query's visible result",
            )
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    unittest.main()
