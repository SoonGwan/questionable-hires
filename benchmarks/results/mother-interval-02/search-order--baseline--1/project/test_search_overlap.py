"""Local QA: python3 -B -m unittest -v test_search_overlap.py"""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 1.0

    async def check_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        values = {"ca": "results for ca", "cat": "results for cat"}
        started = {query: asyncio.Event() for query in queries}
        replies = {
            query: asyncio.get_running_loop().create_future() for query in queries
        }
        calls = []
        tasks = {}

        def record(message):
            print(f"[{order}] {message}", flush=True)

        def equal(actual, expected, message):
            record(f"ASSERT {message}: actual={actual!r}, expected={expected!r}")
            self.assertEqual(actual, expected, message)

        async def fetch(query):
            calls.append(query)
            started[query].set()
            return await replies[query]

        async def complete(query):
            record(f"CONTROL release {query!r} with {values[query]!r}")
            replies[query].set_result(values[query])
            await asyncio.wait_for(asyncio.shield(tasks[query]), self.TIMEOUT)
            equal(tasks[query].done(), True, f"{query!r} request finished")

        try:
            # Start the older request first, but hold both responses pending.
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(started[query].wait(), self.TIMEOUT)
                record(f"CONTROL {query!r} entered fetch; response gated")
            equal(calls, list(queries), "actual Search invoked both queries in order")
            equal([task.done() for task in tasks.values()], [False, False],
                  "both requests overlap before any response is released")

            first, second = queries if order == "normal" else tuple(reversed(queries))
            await complete(first)
            equal(tasks[second].done(), False, "other request is still pending")
            if order == "reversed":
                equal(search.result, values["cat"],
                      "completed latest result is visible before older response")
            # Normal order deliberately imposes no intermediate display requirement.
            await complete(second)
            equal([task.done() for task in tasks.values()], [True, True],
                  "both requests finished before final display assertion")
            equal(search.result, values["cat"],
                  "latest query result must remain visible after both finish")
        finally:
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            if tasks:
                done, pending = await asyncio.wait(
                    tasks.values(), timeout=self.TIMEOUT
                )
                # Retrieve exceptions, including cancellation, from owned tasks.
                for task in done:
                    if not task.cancelled():
                        task.exception()
                record(f"CLEANUP owned={len(tasks)}, done={len(done)}, pending={len(pending)}")
                self.assertFalse(pending, "owned tasks did not stop within timeout")
            for reply in replies.values():
                if not reply.done():
                    reply.cancel()

    async def test_normal_completion_keeps_latest_result(self):
        await self.check_order("normal")

    async def test_reversed_completion_keeps_latest_result(self):
        await self.check_order("reversed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
