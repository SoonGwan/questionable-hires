"""Deterministic local QA: python3 -m unittest -v test_search_overlap.

Uses actual Search with a controlled fetch; no network, dependencies or sleeps.
The reverse-order regression is expected to fail until Search rejects stale results.
"""

import asyncio
import unittest

from search import Search


TIMEOUT = 2.0


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.tasks = []
        self.started = {query: asyncio.Event() for query in ("c", "cat")}
        self.responses = {
            query: asyncio.get_running_loop().create_future()
            for query in self.started
        }
        self.calls = []

    async def asyncTearDown(self):
        # Own every task and response gate, including on assertion/timeout failure.
        for task in self.tasks:
            if not task.done():
                task.cancel()
        for response in self.responses.values():
            if not response.done():
                response.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), TIMEOUT
            )
        self.assertTrue(all(task.done() for task in self.tasks))
        print("CONTROL: all owned tasks finished; response gates closed", flush=True)

    async def fetch(self, query):
        self.calls.append(query)
        self.started[query].set()
        return await self.responses[query]

    async def start_overlap(self):
        for query in ("c", "cat"):
            task = asyncio.create_task(self.search.run(query, self.fetch))
            self.tasks.append(task)
            await asyncio.wait_for(self.started[query].wait(), TIMEOUT)
        self.assertEqual(self.calls, ["c", "cat"])
        self.assertTrue(all(not task.done() for task in self.tasks))
        self.assertTrue(all(not gate.done() for gate in self.responses.values()))
        print("CONTROL: c started before cat; both requests blocked in fetch", flush=True)
        return self.tasks

    async def complete(self, query, value, task):
        self.assertFalse(task.done(), f"{query} must still be pending before release")
        self.assertFalse(self.responses[query].done())
        self.responses[query].set_result(value)
        await asyncio.wait_for(asyncio.shield(task), TIMEOUT)
        self.assertTrue(task.done())
        self.assertFalse(task.cancelled())
        self.assertIsNone(task.exception())
        print(
            f"CONTROL: {query} completed with {value!r}; "
            f"display={self.search.result!r}",
            flush=True,
        )

    def assert_latest_visible(self, phase):
        print(
            f"ASSERT ({phase}): expected='latest: cat', "
            f"actual={self.search.result!r}",
            flush=True,
        )
        self.assertEqual(
            self.search.result, "latest: cat",
            f"{phase}: latest query's result must remain visible",
        )

    async def test_normal_completion_latest_after_both_finish(self):
        older, newer = await self.start_overlap()
        await self.complete("c", "older: c", older)
        self.assertFalse(newer.done())
        self.assertFalse(self.responses["cat"].done())
        # Deliberately no assertion about display while the latest is pending.
        await self.complete("cat", "latest: cat", newer)
        self.assertTrue(all(task.done() for task in self.tasks))
        self.assert_latest_visible("normal order, both finished")

    async def test_reversed_completion_older_cannot_overwrite_latest(self):
        older, newer = await self.start_overlap()
        await self.complete("cat", "latest: cat", newer)
        self.assertFalse(older.done())
        self.assertFalse(self.responses["c"].done())
        self.assert_latest_visible("reversed order, latest finished first")
        await self.complete("c", "older: c", older)
        self.assertTrue(all(task.done() for task in self.tasks))
        self.assert_latest_visible("reversed order, both finished")


if __name__ == "__main__":
    unittest.main(verbosity=2)
