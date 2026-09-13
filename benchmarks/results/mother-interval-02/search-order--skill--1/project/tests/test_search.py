"""Deterministic component QA; no network, sleeps, or production modifications.

Run from the project root:
    python3 -B -m unittest discover -s tests -v
Every request-entry, completion, and cleanup wait has a one-second bound.
"""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
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
            done, pending = await asyncio.wait(self.tasks, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()  # Retrieve failures even after an entry assertion fails.
            self.assertFalse(pending, "Owned Search tasks did not stop within one second")

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)  # Own the task before any fallible entry check.
        request = await self.fetch.started(query, timeout=1)
        return task, request

    async def finish(self, task):
        done, pending = await asyncio.wait([task], timeout=1)
        self.assertFalse(pending, "Search did not finish within one second of release")
        task.result()

    async def test_normal_completion_latest_visible_after_both_finish(self):
        old_task, old = await self.start("c")
        latest_task, latest = await self.start("cat")
        self.assertFalse(old_task.done())
        self.assertFalse(latest_task.done())
        print("\nCONTROL normal: c and cat both entered fetch and are pending", flush=True)

        old.complete("older result")
        await self.finish(old_task)
        self.assertFalse(latest_task.done())
        # Intermediate display is unspecified by the product contract.
        latest.complete("latest result")
        await self.finish(latest_task)
        print(f"ASSERT normal after both finish: expected='latest result', actual={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "latest result")

    async def test_reversed_completion_older_cannot_overwrite_latest(self):
        old_task, old = await self.start("c")
        latest_task, latest = await self.start("cat")
        self.assertFalse(old_task.done())
        self.assertFalse(latest_task.done())
        print("\nCONTROL reversed: c and cat both entered fetch and are pending", flush=True)

        latest.complete("latest result")
        await self.finish(latest_task)
        self.assertFalse(old_task.done())
        print(f"ASSERT latest completed, older pending: expected='latest result', actual={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "latest result")

        old.complete("older result")
        await self.finish(old_task)
        print(f"ASSERT reversed after both finish: expected='latest result', actual={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "latest result")


if __name__ == "__main__":
    unittest.main(verbosity=2)
