import asyncio
import unittest

from search import Search


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def test_latest_query_remains_visible_when_older_response_arrives_last(self):
        search = Search()
        loop = asyncio.get_running_loop()
        responses = {query: loop.create_future() for query in ("ca", "cat")}
        started = {query: asyncio.Event() for query in responses}

        async def fetch(query):
            started[query].set()
            return await responses[query]

        tasks = []
        try:
            # The user types another character while the first search is pending.
            older = asyncio.create_task(search.run("ca", fetch))
            tasks.append(older)
            await started["ca"].wait()
            newer = asyncio.create_task(search.run("cat", fetch))
            tasks.append(newer)
            await started["cat"].wait()

            # The latest request completes first and its result is displayed.
            responses["cat"].set_result(["cat result"])
            await newer
            self.assertEqual(search.result, ["cat result"])

            # A slower, outdated response must not replace the latest result.
            responses["ca"].set_result(["ca result"])
            await older
            self.assertEqual(
                search.result,
                ["cat result"],
                "An older response replaced the latest query's displayed result",
            )
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    unittest.main()
