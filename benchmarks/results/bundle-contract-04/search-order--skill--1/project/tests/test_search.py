"""Deterministic component QA; no network, sleeps, or production edits.

Run from the project root with a process-wide deadline:
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], timeout=15).returncode)'
"""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            done, pending = await asyncio.wait(self.tasks, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()
            self.assertFalse(pending, "owned Search tasks did not stop within 1 second")

    async def start_query(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        return task, request

    async def test_normal_completion_order(self):
        await self.check_order(reverse=False)

    async def test_reversed_completion_order(self):
        await self.check_order(reverse=True)

    async def check_order(self, reverse):
        label = "reversed" if reverse else "normal"
        self.assertIsNone(self.search.result)
        seed_task, seed = await self.start_query("c")
        seed.complete("results for c")
        await asyncio.wait_for(asyncio.shield(seed_task), timeout=1)
        self.assertEqual(self.search.result, "results for c")

        older_task, older = await self.start_query("ca")
        newer_task, newer = await self.start_query("cat")
        self.assertIsNot(older, newer)
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        self.assertFalse(older.response.done())
        self.assertFalse(newer.response.done())
        print(f"{label}: both requests pending; expected retained='results for c', observed={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "results for c", "pending requests must retain the visible result")

        if reverse:
            first_task, first, first_result = newer_task, newer, "results for cat"
            last_task, last, last_result = older_task, older, "results for ca"
        else:
            first_task, first, first_result = older_task, older, "results for ca"
            last_task, last, last_result = newer_task, newer, "results for cat"

        first.complete(first_result)
        await asyncio.wait_for(asyncio.shield(first_task), timeout=1)
        self.assertFalse(last_task.done())
        self.assertFalse(last.response.done())
        print(f"{label}: completed {first.key!r}; expected={first_result!r}, observed={self.search.result!r}; {last.key!r} still pending", flush=True)
        self.assertEqual(self.search.result, first_result)

        last.complete(last_result)
        await asyncio.wait_for(asyncio.shield(last_task), timeout=1)
        print(f"{label}: completed {last.key!r}; expected latest='results for cat', observed={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "results for cat", "latest query must remain visible after both requests complete")

    async def test_transport_key_mismatch_is_an_assertion(self):
        # Exercise the copied support's failure path independently of Search state.
        task = asyncio.create_task(self.fetch("actual"))
        self.tasks.append(task)
        with self.assertRaisesRegex(AssertionError, "request key: expected 'wrong', observed 'actual'"):
            await self.fetch.started("wrong", timeout=1)
        print("control: deliberate request-key mismatch raised the intended AssertionError", flush=True)


if __name__ == "__main__":
    unittest.main()
