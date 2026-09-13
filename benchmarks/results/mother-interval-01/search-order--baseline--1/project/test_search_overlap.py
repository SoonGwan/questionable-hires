"""Local QA: python3 -B -m unittest -v test_search_overlap.py"""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 2.0

    async def check_completion_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        responses = {"ca": "results for ca", "cat": "results for cat"}
        started = {query: asyncio.Event() for query in queries}
        gates = {
            query: asyncio.get_running_loop().create_future() for query in queries
        }
        calls = []
        tasks = {}

        async def fetch(query):
            calls.append(query)
            started[query].set()
            return await gates[query]

        async def finish(query):
            self.assertFalse(tasks[query].done(), f"{query} completed before release")
            self.assertFalse(gates[query].done(), f"{query} gate already released")
            gates[query].set_result(responses[query])
            await asyncio.wait_for(asyncio.shield(tasks[query]), self.TIMEOUT)
            self.assertTrue(tasks[query].done(), f"{query} did not complete")
            self.assertIsNone(tasks[query].result())

        try:
            # Start the older query first, then overlap the newer query with it.
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(started[query].wait(), self.TIMEOUT)
            self.assertEqual(calls, list(queries))
            self.assertTrue(all(not task.done() for task in tasks.values()))
            self.assertTrue(all(not gate.done() for gate in gates.values()))

            first, second = order
            await finish(first)
            self.assertFalse(tasks[second].done(), "requests did not overlap")
            self.assertFalse(gates[second].done())
            if first == "cat":
                self.assertEqual(
                    search.result, responses["cat"],
                    "completed latest query must be displayed before older release",
                )
            # Normal order deliberately imposes no intermediate display requirement.
            await finish(second)
            self.assertTrue(all(task.done() for task in tasks.values()))
            self.assertEqual(
                search.result, responses["cat"],
                f"latest query must remain visible after both finish ({order})",
            )
        finally:
            # Own and reap every task, including when an assertion or wait fails.
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            for gate in gates.values():
                if not gate.done():
                    gate.cancel()
            await asyncio.wait_for(
                asyncio.gather(*tasks.values(), return_exceptions=True), self.TIMEOUT
            )

    async def test_normal_completion_keeps_latest_final_result(self):
        await self.check_completion_order(("ca", "cat"))

    async def test_reversed_completion_does_not_overwrite_latest(self):
        await self.check_completion_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
