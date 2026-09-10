import asyncio
import unittest

from search import Search


class ControlledFetch:
    def __init__(self):
        self.started = asyncio.Queue()
        self.responses = {}

    async def __call__(self, query):
        response = asyncio.get_running_loop().create_future()
        self.responses[query] = response
        self.started.put_nowait(query)
        return await response


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def check_response_order(self, completion_order):
        search = Search()
        fetch = ControlledFetch()
        tasks = {}
        results = {"ca": ["cat", "car"], "cat": ["cat"]}
        try:
            # The user types a prefix, then continues while it is pending.
            for query in ("ca", "cat"):
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                self.assertEqual(await fetch.started.get(), query)

            self.assertIsNone(search.result)
            for query in completion_order:
                fetch.responses[query].set_result(results[query])
                await tasks[query]
                if query == "cat":
                    self.assertEqual(search.result, results["cat"])

            self.assertEqual(
                search.result,
                results["cat"],
                "The displayed result must belong to the latest typed query 'cat'",
            )
        finally:
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks.values(), return_exceptions=True)

    async def test_in_order_responses_keep_latest_result(self):
        await self.check_response_order(("ca", "cat"))

    async def test_late_older_response_keeps_latest_result(self):
        await self.check_response_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main()
