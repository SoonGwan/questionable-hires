"""Deterministic component regression; no network, dependencies, or sleeps.

Run: python3 -B -m unittest -v test_search
Every request-entry, completion, and cleanup wait is bounded to one second.
"""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.owned = []
        self.addAsyncCleanup(self.cleanup_requests)

    async def cleanup_requests(self):
        for task in self.owned:
            if not task.done():
                task.cancel()
        if self.owned:
            done, pending = await asyncio.wait(self.owned, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()  # Retrieve even on an earlier assertion failure.
            self.assertFalse(pending, "owned Search tasks failed to stop in one second")

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned.append(task)  # Own before waiting, including entry failures.
        request = await self.fetch.started(query, timeout=1)
        self.assertFalse(task.done(), "Search must be awaiting the controlled response")
        print(f"CONTROL: entered {query!r}; response held", flush=True)
        return task, request

    async def finish(self, task, request, payload):
        request.complete(payload)
        done, pending = await asyncio.wait([task], timeout=1)
        self.assertFalse(pending, f"Search did not finish {request.key!r} in one second")
        task.result()  # Surface component exceptions rather than only exit status.
        print(f"CONTROL: completed {request.key!r} with {payload!r}", flush=True)

    async def test_normal_overlap_latest_after_both_finish(self):
        older_task, older = await self.start("ca")
        latest_task, latest = await self.start("cat")
        await self.finish(older_task, older, "older: ca")
        self.assertFalse(latest_task.done(), "latest request must still be pending")
        print(f"OBSERVATION only: while latest pending, result={self.search.result!r}", flush=True)
        await self.finish(latest_task, latest, "latest: cat")
        self.assertEqual(self.search.result, "latest: cat",
                         "After both finish normally, latest query owns the display")
        print("ASSERT PASS: normal final result == 'latest: cat'", flush=True)

    async def test_reversed_overlap_latest_survives_older_completion(self):
        older_task, older = await self.start("ca")
        latest_task, latest = await self.start("cat")
        await self.finish(latest_task, latest, "latest: cat")
        self.assertFalse(older_task.done(), "older request must still be pending")
        self.assertEqual(self.search.result, "latest: cat",
                         "Completed latest query must be displayed")
        print("ASSERT PASS: latest completed first, result == 'latest: cat'", flush=True)
        await self.finish(older_task, older, "older: ca")
        self.assertEqual(self.search.result, "latest: cat",
                         "Older completion must not overwrite the completed latest result")
        print("ASSERT PASS: reversed final result == 'latest: cat'", flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
