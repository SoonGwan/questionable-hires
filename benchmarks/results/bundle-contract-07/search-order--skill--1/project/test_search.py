"""Local component regression: python3 -B -m unittest -v test_search."""
import asyncio
import unittest

from qa_controlled_fetch import ControlledFetch
from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.tasks = []
        self.addAsyncCleanup(self.clean_up_tasks)

    async def clean_up_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            done, pending = await asyncio.wait(self.tasks, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned Search tasks did not stop within 1s")

    async def start_request(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        self.assertEqual(request.key, query)
        self.assertFalse(task.done(), "request must wait for controlled completion")
        self.assertFalse(request.response.done())
        return task, request

    async def overlap(self):
        older_task, older = await self.start_request("ca")
        latest_task, latest = await self.start_request("cat")
        self.assertIsNot(older, latest)
        self.assertFalse(older_task.done())
        self.assertFalse(latest_task.done())
        print(f"\n{self.id()}: CONTROL 'ca' and 'cat' both entered and pending", flush=True)
        return older_task, older, latest_task, latest

    async def finish(self, task, request, payload):
        request.complete(payload)
        await asyncio.wait_for(asyncio.shield(task), timeout=1)
        self.assertTrue(task.done())
        self.assertEqual(request.response.result(), payload)
        print(f"CONTROL completed {request.key!r} with {payload!r}", flush=True)

    async def test_normal_completion_latest_after_both_finish(self):
        older_task, older, latest_task, latest = await self.overlap()
        await self.finish(older_task, older, "older result")
        self.assertFalse(latest_task.done())
        self.assertFalse(latest.response.done())
        # The display during this interval is deliberately unspecified.
        print(f"OBSERVATION while latest pending: {self.search.result!r} (no display assertion)", flush=True)
        await self.finish(latest_task, latest, "latest result")
        print(f"ASSERT after both finish: expected 'latest result', observed {self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "latest result", "latest must own final display")

    async def test_reversed_completion_older_cannot_overwrite_latest(self):
        older_task, older, latest_task, latest = await self.overlap()
        await self.finish(latest_task, latest, "latest result")
        self.assertFalse(older_task.done())
        self.assertFalse(older.response.done())
        print(f"ASSERT latest completed: expected 'latest result', observed {self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "latest result")
        await self.finish(older_task, older, "older result")
        print(f"ASSERT after both finish: expected 'latest result', observed {self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "latest result", "older response overwrote completed latest result")


if __name__ == "__main__":
    unittest.main(verbosity=2)
