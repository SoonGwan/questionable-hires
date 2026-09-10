"""Local, cache-free experiment: python3 -m unittest -v experiment_search_order.

These tests document current behavior, including the stale-result race. They
are diagnostic checks, not assertions of the behavior a future fix should keep.
"""

import asyncio
import unittest

from search import Search
from transport import fetch


class SearchCompletionOrderExperiment(unittest.IsolatedAsyncioTestCase):
    async def exercise(self, completion_order):
        search = Search()
        started = asyncio.Queue()
        responses = {}
        calls = []

        async def request(path, *, params, headers):
            query = params["q"]
            calls.append((path, params.copy(), headers.copy()))
            # Each request gets its own fresh response; no cache exists here.
            response = asyncio.get_running_loop().create_future()
            responses[query] = response
            started.put_nowait(query)
            return await response

        async def local_fetch(query):
            return await fetch(query, request)

        tasks = {}
        snapshots = []
        try:
            for query in ("old", "new"):
                tasks[query] = asyncio.create_task(search.run(query, local_fetch))
                self.assertEqual(await asyncio.wait_for(started.get(), 1), query)

            self.assertIsNone(search.result)
            self.assertTrue(all(not task.done() for task in tasks.values()))
            self.assertEqual(calls, [
                ("/search", {"q": query}, {"Cache-Control": "no-cache"})
                for query in ("old", "new")
            ])

            for query in completion_order:
                responses[query].set_result(f"fresh response for {query}")
                await asyncio.wait_for(tasks[query], 1)
                snapshots.append(search.result)
            return snapshots
        finally:
            for task in tasks.values():
                task.cancel()
            await asyncio.gather(*tasks.values(), return_exceptions=True)

    async def test_in_order_completion_leaves_new_result(self):
        self.assertEqual(await self.exercise(("old", "new")), [
            "fresh response for old", "fresh response for new",
        ])

    async def test_reverse_completion_overwrites_new_result_with_old(self):
        self.assertEqual(await self.exercise(("new", "old")), [
            "fresh response for new", "fresh response for old",
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
