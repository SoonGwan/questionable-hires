"""Deterministic component QA; no network, sleeps, or production edits."""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.tasks = []
        self.addAsyncCleanup(self.cleanup_requests)

    async def cleanup_requests(self):
        # Register ownership before checking entry so failed checks also drain.
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            done, pending = await asyncio.wait(self.tasks, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned Search tasks did not stop")

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        self.assertFalse(task.done())
        return task, request

    async def finish(self, task, request, payload):
        request.complete(payload)
        done, _ = await asyncio.wait([task], timeout=1)
        self.assertIn(task, done, "Search did not process controlled completion")
        task.result()

    async def seed(self):
        task, request = await self.start("existing")
        await self.finish(task, request, "existing result")
        self.assertEqual(self.search.result, "existing result")

    async def test_single_request_retains_display_until_completion(self):
        task, request = await self.start("initial")
        self.assertIsNone(self.search.result)
        await self.finish(task, request, "existing result")
        self.assertEqual(self.search.result, "existing result")
        task, request = await self.start("replacement")
        self.assertEqual(self.search.result, "existing result")
        await self.finish(task, request, "replacement result")
        self.assertEqual(self.search.result, "replacement result")

    async def test_older_completes_while_newer_pending_retains_display(self):
        await self.seed()
        older, old_request = await self.start("older")
        self.assertEqual(self.search.result, "existing result")
        newer, new_request = await self.start("newer")
        self.assertEqual(self.search.result, "existing result")

        await self.finish(older, old_request, "older result")
        self.assertFalse(newer.done())
        self.assertFalse(new_request.response.done())
        self.assertEqual(self.search.result, "existing result")

        await self.finish(newer, new_request, "newer result")
        self.assertEqual(self.search.result, "newer result")

    async def test_newer_completes_first_late_older_cannot_overwrite(self):
        await self.seed()
        older, old_request = await self.start("older")
        self.assertEqual(self.search.result, "existing result")
        newer, new_request = await self.start("newer")
        self.assertEqual(self.search.result, "existing result")

        await self.finish(newer, new_request, "newer result")
        self.assertFalse(older.done())
        self.assertEqual(self.search.result, "newer result")
        await self.finish(older, old_request, "older result")
        self.assertEqual(self.search.result, "newer result")


if __name__ == "__main__":
    unittest.main()
