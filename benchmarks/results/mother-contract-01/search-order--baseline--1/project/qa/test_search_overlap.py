"""Deterministic integration repro; imports the unchanged production Search."""

import asyncio
import unittest

from search import Search


TIMEOUT = 2.0


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def check_completion_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        responses = {"ca": "results for ca", "cat": "results for cat"}
        entered = {query: asyncio.Event() for query in queries}
        releases = {
            query: asyncio.get_running_loop().create_future() for query in queries
        }
        calls = []
        completed = []
        tasks = {}

        async def fetch(query):
            calls.append(query)
            entered[query].set()
            result = await releases[query]
            completed.append(query)
            return result

        try:
            # Start the newer query only after the older one has reached fetch.
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(entered[query].wait(), TIMEOUT)

            self.assertEqual(calls, list(queries))
            self.assertEqual(completed, [])
            self.assertTrue(all(not task.done() for task in tasks.values()))
            self.assertTrue(all(not gate.done() for gate in releases.values()))
            self.assertIsNone(search.result)
            print("CONTROL: ca then cat entered actual Search.run; both pending; "
                  "no response completed; result is None", flush=True)

            first, second = order
            releases[first].set_result(responses[first])
            await asyncio.wait_for(asyncio.shield(tasks[first]), TIMEOUT)
            self.assertEqual(completed, [first])
            self.assertEqual(search.result, responses[first])
            self.assertFalse(tasks[second].done())
            self.assertFalse(releases[second].done())
            print("CONTROL: only {!r} completed; result={!r}; {!r} still pending"
                  .format(first, search.result, second), flush=True)

            releases[second].set_result(responses[second])
            await asyncio.wait_for(asyncio.shield(tasks[second]), TIMEOUT)
            self.assertEqual(completed, list(order))
            self.assertTrue(all(task.done() for task in tasks.values()))
            print("ASSERT: completion order={!r}; expected latest result={!r}; "
                  "actual={!r}".format(order, responses["cat"], search.result),
                  flush=True)
            self.assertEqual(
                search.result, responses["cat"],
                "The latest query's result must remain visible after both "
                "overlapping requests finish",
            )
        finally:
            # Own and reap every request, including on timeout or assertion failure.
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            await asyncio.wait_for(
                asyncio.gather(*tasks.values(), return_exceptions=True), TIMEOUT
            )
            for gate in releases.values():
                if not gate.done():
                    gate.cancel()
            self.assertTrue(all(task.done() for task in tasks.values()))
            print("CLEANUP: all owned request tasks finished", flush=True)

    async def test_normal_completion_order(self):
        await self.check_completion_order(("ca", "cat"))

    async def test_reversed_completion_order(self):
        await self.check_completion_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
