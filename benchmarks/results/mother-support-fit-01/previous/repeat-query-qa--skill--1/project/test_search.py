import asyncio
import unittest
from search import Search


class SearchTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial(self):
        self.assertIsNone(Search(None).result)

    async def test_identical_queries_complete_in_reverse_order(self):
        await self._assert_reverse_completion("repeat", "repeat")

    async def test_different_queries_complete_in_reverse_order(self):
        await self._assert_reverse_completion("older", "newer")

    async def _assert_reverse_completion(self, older_query, newer_query):
        # Each actual fetch call receives its own response, including equal keys.
        requests = asyncio.Queue()
        fetch_keys = []
        owned_tasks = []

        async def fetch(key):
            response = asyncio.get_running_loop().create_future()
            fetch_keys.append(key)
            requests.put_nowait((key, response))
            return await response

        search = Search(fetch)
        displayed = {
            "items": [{"id": "seed", "details": {"label": "Previously shown"}}],
            "total": 1,
            "metadata": {"request": "seed", "cursor": None},
        }
        older_payload = {
            "items": [{"id": "old", "details": {"label": "Older response"}}],
            "total": 7,
            "metadata": {"request": "older", "cursor": "old-page"},
        }
        newest_payload = {
            "items": [{"id": "new", "details": {"label": "Newest response"}}],
            "total": 12,
            "metadata": {"request": "newest", "cursor": "new-page"},
        }

        async def start(query):
            task = asyncio.create_task(search.submit(query))
            owned_tasks.append(task)
            actual_key, response = await asyncio.wait_for(requests.get(), timeout=1)
            self.assertEqual(actual_key, query)
            self.assertFalse(task.done(), "Submission must await its own response")
            return task, response

        async def complete(task, response, payload):
            response.set_result(payload)
            await asyncio.wait_for(asyncio.shield(task), timeout=1)

        try:
            seed_task, seed_response = await start("seed")
            await complete(seed_task, seed_response, displayed)
            self.assertEqual(search.result, displayed, "Seed complete payload")

            older_task, older_response = await start(older_query)
            self.assertEqual(search.result, displayed, "Retain payload after older submission")

            newest_task, newest_response = await start(newer_query)
            self.assertIsNot(older_response, newest_response)
            self.assertEqual(fetch_keys, ["seed", older_query, newer_query])
            self.assertEqual(search.result, displayed, "Retain payload after newest submission")
            self.assertFalse(older_response.done())

            await complete(newest_task, newest_response, newest_payload)
            self.assertFalse(older_task.done(), "Older request must still be pending")
            self.assertEqual(search.result, newest_payload, "Newest completion owns complete payload")

            await complete(older_task, older_response, older_payload)
            self.assertEqual(search.result, newest_payload, "Older completion must not replace newest payload")
        finally:
            # Register ownership before any assertion; failures also drain tasks.
            for task in owned_tasks:
                task.cancel()
            await asyncio.wait_for(
                asyncio.gather(*owned_tasks, return_exceptions=True), timeout=1
            )
