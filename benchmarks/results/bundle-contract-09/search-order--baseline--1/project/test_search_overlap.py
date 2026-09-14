"""Run locally with: python3 -B -m unittest -v test_search_overlap.py"""

import asyncio
import unittest

from search import Search


TIMEOUT = 2.0


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    async def check_completion_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        responses = {"ca": "results for ca", "cat": "results for cat"}
        entered = {query: asyncio.Event() for query in queries}
        release = {query: asyncio.Event() for query in queries}
        calls = []
        completed = []
        tasks = {}

        def report(message):
            print("[{}] {}".format(" -> ".join(order), message), flush=True)

        async def fetch(query):
            calls.append(query)
            entered[query].set()
            await asyncio.wait_for(release[query].wait(), TIMEOUT)
            completed.append(query)
            return responses[query]

        async def finish(query):
            release[query].set()
            await asyncio.wait_for(asyncio.shield(tasks[query]), TIMEOUT)
            report("released {!r}; Search.run finished; displayed={!r}".format(
                query, search.result))

        try:
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(entered[query].wait(), TIMEOUT)

            self.assertEqual(calls, list(queries), "actual Search must fetch both queries in typing order")
            self.assertEqual(completed, [], "neither gated request may have completed")
            for query in queries:
                self.assertFalse(release[query].is_set())
                self.assertFalse(tasks[query].done(), "both requests must overlap")
            report("PASS controls: actual Search fetched ca then cat; both requests pending behind closed gates")

            first, last = order
            await finish(first)
            self.assertEqual(completed, [first])
            self.assertFalse(tasks[last].done(), "second completion must remain controlled")
            self.assertFalse(release[last].is_set())
            report("PASS controls: only {!r} completed; {!r} still gated".format(first, last))

            if first == queries[-1]:
                self.assertEqual(search.result, responses[queries[-1]],
                                 "completed latest query must be displayed")
                report("PASS assertion: completed latest query is displayed before the older response")
            # Normal order intentionally imposes no intermediate display assertion.

            await finish(last)
            self.assertEqual(completed, list(order), "completion order must match the controlled schedule")
            self.assertTrue(all(task.done() and not task.cancelled() for task in tasks.values()))
            report("PASS controls: both Search.run calls finished in the requested order")
            report("assert latest remains visible: expected={!r}, actual={!r}".format(
                responses[queries[-1]], search.result))
            self.assertEqual(search.result, responses[queries[-1]],
                             "after both requests finish, the latest query must remain visible")
        finally:
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            if tasks:
                await asyncio.wait_for(
                    asyncio.gather(*tasks.values(), return_exceptions=True), TIMEOUT)
            report("cleanup: all owned request tasks settled")

    async def test_normal_completion_keeps_latest_after_both_finish(self):
        await self.check_completion_order(("ca", "cat"))

    async def test_reversed_completion_cannot_overwrite_latest(self):
        await self.check_completion_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
