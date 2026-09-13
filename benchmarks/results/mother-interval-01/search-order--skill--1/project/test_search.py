"""Deterministic component QA; no network, dependencies, or production changes."""
import asyncio
import unittest

from search import Search
from search_test_support import ControlledFetch


TIMEOUT = 1


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
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
            self.assertFalse(pending, "owned Search tasks did not stop within 1s")

    async def start(self, search, fetch, query):
        task = asyncio.create_task(search.run(query, fetch))
        self.tasks.append(task)  # Own it before entry assertions can fail.
        request = await fetch.started(query, timeout=TIMEOUT)
        return task, request

    async def finish(self, task, request, payload):
        request.complete(payload)
        done, pending = await asyncio.wait([task], timeout=TIMEOUT)
        self.assertFalse(pending, "Search.run did not finish within 1s")
        task.result()

    def assert_display(self, search, expected, stage):
        self.assertEqual(
            search.result, expected,
            f"{stage}: expected {expected!r}, observed {search.result!r}",
        )

    def test_assertion_failure_control(self):
        # Deliberate mismatch in isolation proves the same display assertion
        # fails with actual/expected evidence, rather than a support exception.
        search = Search()
        with self.assertRaises(AssertionError) as caught:
            self.assert_display(search, "sentinel", "deliberate mismatch")
        self.assertIn("expected 'sentinel', observed None", str(caught.exception))
        print(f"CONTROL: caught intended display assertion: {caught.exception}", flush=True)

    async def overlap(self, reversed_order):
        search = Search()
        fetch = ControlledFetch()
        older, older_request = await self.start(search, fetch, "c")
        newer, newer_request = await self.start(search, fetch, "cat")
        self.assertIsNot(older_request, newer_request)
        self.assertFalse(older.done(), "older request must overlap newer")
        self.assertFalse(newer.done(), "newer request must be pending")
        self.assertFalse(older_request.response.done())
        self.assertFalse(newer_request.response.done())
        print("CONTROL: actual Search entered 'c' then 'cat'; both responses pending", flush=True)

        if reversed_order:
            await self.finish(newer, newer_request, "CAT_RESULT")
            self.assert_display(search, "CAT_RESULT", "latest completes first")
            self.assertFalse(older.done())
            print("PASS: latest completes first; displayed 'CAT_RESULT'", flush=True)
            await self.finish(older, older_request, "C_RESULT")
        else:
            await self.finish(older, older_request, "C_RESULT")
            self.assertFalse(newer.done())
            # The contract permits any display while the latest is pending.
            print(f"OBSERVATION only: latest pending; displayed {search.result!r}", flush=True)
            await self.finish(newer, newer_request, "CAT_RESULT")

        self.assertTrue(older.done())
        self.assertTrue(newer.done())
        order = "reversed" if reversed_order else "normal"
        print(f"CHECK {order}, both finished: expected 'CAT_RESULT', observed {search.result!r}", flush=True)
        self.assert_display(search, "CAT_RESULT", f"{order}, both requests finished")

    async def test_normal_overlapping_completion(self):
        await self.overlap(reversed_order=False)

    async def test_reversed_overlapping_completion(self):
        await self.overlap(reversed_order=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
