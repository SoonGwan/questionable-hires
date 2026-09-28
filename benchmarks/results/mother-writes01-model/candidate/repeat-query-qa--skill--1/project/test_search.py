import asyncio
import unittest
from search import Search


class SearchTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial(self):
        self.assertIsNone(Search(None).result)

    async def test_identical_queries_complete_in_reverse_order(self):
        await self._check_reverse_completion("repeat", "repeat")

    async def test_different_queries_complete_in_reverse_order(self):
        await self._check_reverse_completion("older", "newer")

    async def _check_reverse_completion(self, older_query, newer_query):
        # Each fetch call has its own response future, including repeated keys.
        entries = asyncio.Queue()
        actual_keys = []
        tasks = []
        timeout = 1

        async def fetch(key):
            response = asyncio.get_running_loop().create_future()
            actual_keys.append(key)
            entries.put_nowait((key, response))
            return await response

        search = Search(fetch)
        displayed = {
            "items": [{"id": "seed", "labels": ["previous", "visible"]}],
            "meta": {"request": "seed", "count": 1},
        }
        older_payload = {
            "items": [{"id": "old", "labels": ["stale"]}],
            "meta": {"request": "older", "count": 1},
        }
        newest_payload = {
            "items": [{"id": "new", "labels": ["current", "complete"]}],
            "meta": {"request": "newest", "count": 1},
        }

        try:
            # Establish a previously displayed payload through the real component.
            seed = asyncio.create_task(search.submit("seed"))
            tasks.append(seed)
            key, response = await asyncio.wait_for(entries.get(), timeout)
            self.assertEqual(key, "seed")
            response.set_result(displayed)
            await asyncio.wait_for(asyncio.shield(seed), timeout)
            self.assertEqual(search.result, displayed, "seed completion")

            older = asyncio.create_task(search.submit(older_query))
            tasks.append(older)
            key, older_response = await asyncio.wait_for(entries.get(), timeout)
            self.assertEqual(key, older_query)
            self.assertFalse(older.done())
            self.assertEqual(search.result, displayed, "after older submission")

            newest = asyncio.create_task(search.submit(newer_query))
            tasks.append(newest)
            key, newest_response = await asyncio.wait_for(entries.get(), timeout)
            self.assertEqual(key, newer_query)
            self.assertIsNot(older_response, newest_response)
            self.assertFalse(older.done())
            self.assertFalse(newest.done())
            self.assertEqual(search.result, displayed, "after newest submission")
            self.assertEqual(actual_keys, ["seed", older_query, newer_query])

            newest_response.set_result(newest_payload)
            await asyncio.wait_for(asyncio.shield(newest), timeout)
            self.assertFalse(older.done())
            self.assertEqual(search.result, newest_payload, "after newest completion")

            older_response.set_result(older_payload)
            await asyncio.wait_for(asyncio.shield(older), timeout)
            self.assertEqual(search.result, newest_payload, "after older completion")
        finally:
            # Own and drain every submission even if an entry/state assertion fails.
            for task in tasks:
                task.cancel()
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout
            )
