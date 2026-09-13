"""Run from the project root: python3 -m unittest discover -s qa -v."""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 1.0

    async def check_completion_order(self, order):
        search = Search()
        queries = ("ca", "cat")  # Two successive edits in the same search box.
        values = {"ca": "results for ca", "cat": "results for cat"}
        loop = asyncio.get_running_loop()
        gates = {query: loop.create_future() for query in queries}
        entered = {query: asyncio.Event() for query in queries}
        calls = []
        tasks = {}

        async def fetch(query):
            calls.append(query)
            entered[query].set()
            return await gates[query]

        def record(stage):
            print(
                f"order={order!r} stage={stage} calls={calls!r} "
                f"done={ {q: t.done() for q, t in tasks.items()}!r} "
                f"displayed={search.result!r}",
                flush=True,
            )

        try:
            for query in queries:
                tasks[query] = asyncio.create_task(
                    search.run(query, fetch), name=f"search-{query}"
                )
                await asyncio.wait_for(entered[query].wait(), self.TIMEOUT)

            # Both actual Search.run calls have reached fetch; neither may finish
            # until this test releases its response. No sleep controls scheduling.
            self.assertEqual(calls, list(queries))
            self.assertTrue(all(not task.done() for task in tasks.values()))
            self.assertTrue(all(not gate.done() for gate in gates.values()))
            self.assertIsNone(search.result)
            record("overlap controls passed")

            first, last = order
            gates[first].set_result(values[first])
            await asyncio.wait_for(asyncio.shield(tasks[first]), self.TIMEOUT)
            self.assertTrue(tasks[first].done())
            self.assertFalse(tasks[last].done())
            self.assertFalse(gates[last].done())
            self.assertEqual(search.result, values[first])
            record("first response assertions passed")

            gates[last].set_result(values[last])
            await asyncio.wait_for(asyncio.shield(tasks[last]), self.TIMEOUT)
            self.assertTrue(all(task.done() for task in tasks.values()))
            self.assertEqual(calls, list(queries))
            record("before latest-query assertion")
            self.assertEqual(
                search.result,
                values[queries[-1]],
                "Latest query 'cat' must remain displayed after both requests "
                f"finish; completion order was {order!r}",
            )
        finally:
            # Own and drain every created task even on assertion failure/timeout.
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

    async def test_normal_completion_keeps_latest_query(self):
        await self.check_completion_order(("ca", "cat"))

    async def test_reversed_completion_keeps_latest_query(self):
        await self.check_completion_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
