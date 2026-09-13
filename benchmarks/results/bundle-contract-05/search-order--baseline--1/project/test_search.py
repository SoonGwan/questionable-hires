"""Deterministic overlap regression tests; run: python3 -B -m unittest -v test_search."""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 1.0

    async def check_completion_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        responses = {"ca": "results for ca", "cat": "results for cat"}
        loop = asyncio.get_running_loop()
        gates = {query: loop.create_future() for query in queries}
        started = {query: asyncio.Event() for query in queries}
        calls = []
        tasks = {}

        async def fetch(query):
            calls.append(query)
            started[query].set()
            return await gates[query]

        async def bounded(awaitable):
            return await asyncio.wait_for(awaitable, timeout=self.TIMEOUT)

        async def complete(query):
            self.assertFalse(tasks[query].done(), f"{query}: pending before release")
            self.assertFalse(gates[query].done(), f"{query}: gate still closed")
            gates[query].set_result(responses[query])
            await bounded(asyncio.shield(tasks[query]))
            self.assertTrue(tasks[query].done(), f"{query}: request completed")
            self.assertFalse(tasks[query].cancelled(), f"{query}: completed normally")
            self.assertIsNone(tasks[query].exception(), f"{query}: no request error")

        try:
            # Enter the actual Search.run fetch for each query in typing order.
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await bounded(started[query].wait())

            self.assertEqual(calls, list(queries), "both actual requests entered in typing order")
            for query in queries:
                self.assertFalse(tasks[query].done(), "requests overlap before any response")
                self.assertFalse(gates[query].done(), "responses remain under test control")

            first, second = order
            await complete(first)
            self.assertFalse(tasks[second].done(), "second response remains pending")
            self.assertFalse(gates[second].done(), "second gate remains closed")

            if first == "cat":
                self.assertEqual(
                    search.result, responses["cat"],
                    "latest completed result is visible before releasing the older response",
                )
            # Normal order deliberately makes no intermediate display assertion.
            await complete(second)
            self.assertTrue(all(task.done() for task in tasks.values()))
            self.assertEqual(
                search.result, responses["cat"],
                f"latest query must remain visible after both finish; completion order={order}",
            )
        finally:
            # Own, cancel, and join every task even on assertion failure or timeout.
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            if tasks:
                await bounded(asyncio.gather(*tasks.values(), return_exceptions=True))
            for gate in gates.values():
                if not gate.done():
                    gate.cancel()

    async def test_normal_completion_latest_result_after_both_finish(self):
        await self.check_completion_order(("ca", "cat"))

    async def test_reversed_completion_older_response_cannot_overwrite_latest(self):
        await self.check_completion_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
