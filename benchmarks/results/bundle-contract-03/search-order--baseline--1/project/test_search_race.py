"""Local regression test: python3 -B -m unittest -v test_search_race.py."""

import asyncio
import unittest

from search import Search


class SearchOrderingTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 2.0

    async def check_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        values = {"ca": ["car", "cafe"], "cat": ["cat", "catalog"]}
        loop = asyncio.get_running_loop()
        responses = {query: loop.create_future() for query in queries}
        entered = {query: asyncio.Event() for query in queries}
        calls = []
        tasks = {}

        async def fetch(query):
            calls.append(query)
            entered[query].set()
            return await responses[query]

        try:
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(entered[query].wait(), self.TIMEOUT)

            self.assertEqual(calls, list(queries), "Requests start in typing order")
            self.assertTrue(all(not task.done() for task in tasks.values()))
            self.assertTrue(all(not response.done() for response in responses.values()))
            self.assertIsNone(search.result, "Neither response has been released")
            print("\nCONTROL: ca then cat entered actual Search.run; both pending", flush=True)

            first, second = order
            responses[first].set_result(values[first])
            await asyncio.wait_for(asyncio.shield(tasks[first]), self.TIMEOUT)
            self.assertEqual(search.result, values[first], "First completion is displayed")
            self.assertFalse(tasks[second].done(), "Other request remains in flight")
            self.assertFalse(responses[second].done(), "Other response is still withheld")
            print(f"CONTROL: {first} completed; result={search.result!r}; {second} pending", flush=True)

            responses[second].set_result(values[second])
            await asyncio.wait_for(asyncio.shield(tasks[second]), self.TIMEOUT)
            self.assertTrue(all(task.done() for task in tasks.values()))
            self.assertEqual(calls, list(queries), "Exactly two fetch calls")
            print(
                f"ASSERT: completion order={order!r}; "
                f"actual={search.result!r}; expected latest={values['cat']!r}",
                flush=True,
            )
            self.assertEqual(
                search.result,
                values["cat"],
                "Latest typed query 'cat' must remain visible after both requests finish",
            )
        finally:
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            if tasks:
                await asyncio.wait_for(
                    asyncio.gather(*tasks.values(), return_exceptions=True), self.TIMEOUT
                )
            for response in responses.values():
                if not response.done():
                    response.cancel()

    async def test_normal_completion_keeps_latest_result(self):
        await self.check_order(("ca", "cat"))

    async def test_reversed_completion_keeps_latest_result(self):
        await self.check_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
