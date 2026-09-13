"""Deterministic QA of actual Search; run: python3 -B -m unittest -v test_search_overlap."""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 2.0

    async def check_completion_order(self, completion_order):
        search = Search()
        queries = ("ca", "cat")
        results = {"ca": "results for ca", "cat": "results for cat"}
        entered = {query: asyncio.Event() for query in queries}
        gates = {
            query: asyncio.get_running_loop().create_future()
            for query in queries
        }
        started = []
        completed = []
        tasks = {}

        async def fetch(query):
            started.append(query)
            entered[query].set()
            value = await gates[query]
            completed.append(query)
            return value

        async def finish(query):
            gates[query].set_result(results[query])
            await asyncio.wait_for(asyncio.shield(tasks[query]), self.TIMEOUT)
            self.assertTrue(tasks[query].done(), "released Search.run must finish")
            self.assertFalse(tasks[query].cancelled())
            self.assertIsNone(tasks[query].exception())

        try:
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(entered[query].wait(), self.TIMEOUT)

            # Establish real overlap, with the newer query submitted second.
            self.assertEqual(started, list(queries))
            self.assertEqual(completed, [])
            for query in queries:
                self.assertFalse(tasks[query].done(), "both requests must overlap")
                self.assertFalse(gates[query].done(), "responses remain gated")

            first, second = completion_order
            await finish(first)
            self.assertEqual(completed, [first])
            self.assertFalse(tasks[second].done(), "other request must still be pending")
            self.assertFalse(gates[second].done())
            if first == "cat":
                self.assertEqual(
                    search.result, results["cat"],
                    "completed latest query must be displayed before older completion",
                )
            # Normal order deliberately has no intermediate display assertion.
            await finish(second)
            self.assertEqual(completed, list(completion_order))
            self.assertTrue(all(task.done() for task in tasks.values()))
            self.assertEqual(
                search.result, results["cat"],
                "latest query must remain displayed after both requests finish; "
                "completion order: " + " -> ".join(completion_order),
            )
        finally:
            # Own and drain every task, including assertion/timeout failure paths.
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            if tasks:
                await asyncio.wait_for(
                    asyncio.gather(*tasks.values(), return_exceptions=True),
                    self.TIMEOUT,
                )
            for gate in gates.values():
                if not gate.done():
                    gate.cancel()

    async def test_normal_overlapping_completion_keeps_latest(self):
        await self.check_completion_order(("ca", "cat"))

    async def test_reversed_completion_does_not_overwrite_latest(self):
        await self.check_completion_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
