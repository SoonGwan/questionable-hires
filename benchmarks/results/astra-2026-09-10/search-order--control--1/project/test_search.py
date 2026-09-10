import asyncio
import unittest

from search import Search


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def test_latest_query_stays_visible_when_earlier_request_finishes_last(self):
        """Typing 'ca' then 'cat' must not let the slower 'ca' response win."""
        search = Search()
        loop = asyncio.get_running_loop()
        responses = {query: loop.create_future() for query in ("ca", "cat")}
        started = asyncio.Queue()

        async def fetch(query):
            started.put_nowait(query)
            return await responses[query]

        tasks = []
        try:
            earlier = asyncio.create_task(search.run("ca", fetch))
            tasks.append(earlier)
            self.assertEqual(await asyncio.wait_for(started.get(), 1), "ca")

            latest = asyncio.create_task(search.run("cat", fetch))
            tasks.append(latest)
            self.assertEqual(await asyncio.wait_for(started.get(), 1), "cat")

            responses["cat"].set_result(["cat"])
            await asyncio.wait_for(latest, 1)
            self.assertEqual(search.result, ["cat"])

            responses["ca"].set_result(["car", "cat"])
            await asyncio.wait_for(earlier, 1)
            self.assertEqual(
                search.result,
                ["cat"],
                "An earlier query's late response replaced the latest query's result",
            )
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    unittest.main()
