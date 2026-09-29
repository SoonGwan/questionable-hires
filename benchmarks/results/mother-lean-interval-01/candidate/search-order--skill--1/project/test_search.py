"""Deterministic interaction QA. Run: python3 -m unittest -v test_search"""
import asyncio
import unittest

from search import Search


TIMEOUT = 1


class ControlledFetch:
    def __init__(self):
        self.calls = asyncio.Queue()

    async def __call__(self, query):
        response = asyncio.get_running_loop().create_future()
        self.calls.put_nowait((query, response))
        return await response


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.tasks = []
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            done, pending = await asyncio.wait(self.tasks, timeout=TIMEOUT)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned Search tasks did not stop during cleanup")

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        actual_query, response = await asyncio.wait_for(
            self.fetch.calls.get(), timeout=TIMEOUT
        )
        self.assertEqual(actual_query, query, "actual Search fetch query")
        self.assertFalse(task.done(), "request must be pending before release")
        self.assertFalse(response.done(), "response must await controlled release")
        print(f"CONTROL: entered query={actual_query!r}; response held", flush=True)
        return task, response

    async def complete(self, request, payload):
        task, response = request
        self.assertFalse(response.done(), "response released exactly once")
        response.set_result(payload)
        done, pending = await asyncio.wait([task], timeout=TIMEOUT)
        self.assertFalse(pending, "Search did not finish after response release")
        task.result()
        print(f"CONTROL: completed payload={payload!r}", flush=True)

    async def overlap(self):
        older = await self.start("ca")
        newer = await self.start("cat")
        self.assertFalse(older[0].done(), "older request overlaps newer request")
        self.assertFalse(newer[0].done(), "newer request overlaps older request")
        return older, newer

    async def test_normal_completion_latest_after_both_finish(self):
        older, newer = await self.overlap()
        await self.complete(older, "results for ca")
        self.assertFalse(newer[0].done(), "newer request remains controlled/pending")
        # No intermediate display contract while the newer request is pending.
        await self.complete(newer, "results for cat")
        actual = self.search.result  # Immutable snapshot, not an aliased container.
        print(f"ASSERT normal final: actual={actual!r}, expected='results for cat'", flush=True)
        self.assertEqual(actual, "results for cat", "normal: both requests finished")

    async def test_reversed_completion_preserves_latest(self):
        older, newer = await self.overlap()
        await self.complete(newer, "results for cat")
        self.assertFalse(older[0].done(), "older request remains controlled/pending")
        actual = self.search.result
        print(f"ASSERT reversed latest completed: actual={actual!r}, expected='results for cat'", flush=True)
        self.assertEqual(actual, "results for cat", "reversed: latest finished, older pending")
        await self.complete(older, "results for ca")
        actual = self.search.result
        print(f"ASSERT reversed final: actual={actual!r}, expected='results for cat'", flush=True)
        self.assertEqual(actual, "results for cat", "reversed: both requests finished")


if __name__ == "__main__":
    unittest.main(verbosity=2)
