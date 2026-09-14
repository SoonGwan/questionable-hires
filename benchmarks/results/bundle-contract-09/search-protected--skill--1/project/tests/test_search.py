"""Deterministic component QA; run: python3 -B -m unittest discover -s tests -v."""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchFlowTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.owned_tasks = []
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        # Own tasks immediately, including when a fetch-entry assertion fails.
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            done, pending = await asyncio.wait(self.owned_tasks, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned Search tasks did not stop within 1s")

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned_tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        return task, request

    async def finish(self, task, request, payload):
        request.complete(payload)
        done, pending = await asyncio.wait([task], timeout=1)
        self.assertFalse(pending, "Search did not consume its response within 1s")
        task.result()

    async def seed_result(self):
        task, request = await self.start("seed")
        await self.finish(task, request, "existing result")
        self.assertEqual(self.search.result, "existing result")

    async def test_single_request_retains_display_until_completion(self):
        self.assertIsNone(self.search.result)
        await self.seed_result()
        task, request = await self.start("replacement")
        self.assertFalse(task.done())
        self.assertFalse(request.response.done())
        self.assertEqual(self.search.result, "existing result")
        await self.finish(task, request, "replacement result")
        self.assertEqual(self.search.result, "replacement result")

    async def test_older_completes_while_newer_pending_retains_existing(self):
        await self.seed_result()
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

    async def test_newer_completes_first_older_cannot_replace_it(self):
        await self.seed_result()
        older, old_request = await self.start("older")
        self.assertEqual(self.search.result, "existing result")
        newer, new_request = await self.start("newer")
        self.assertEqual(self.search.result, "existing result")

        await self.finish(newer, new_request, "newer result")
        self.assertFalse(older.done())
        self.assertFalse(old_request.response.done())
        self.assertEqual(self.search.result, "newer result")

        await self.finish(older, old_request, "older result")
        self.assertEqual(self.search.result, "newer result")


if __name__ == "__main__":
    unittest.main()
