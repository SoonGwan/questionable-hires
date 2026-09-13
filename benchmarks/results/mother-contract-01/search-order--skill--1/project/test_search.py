"""Local component regression: python3 -m unittest -v test_search.

Uses actual Search with controlled transport; no network or timing sleeps.
Every behavior-dependent wait is bounded to one second.
"""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.owned_tasks = []

    async def asyncTearDown(self):
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            done, pending = await asyncio.wait(self.owned_tasks, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()  # Retrieve exceptions even after a failed assertion.
            self.assertFalse(pending, "owned Search tasks did not stop within 1s")

    def launch(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned_tasks.append(task)
        return task

    async def test_single_query(self):
        task = self.launch("cat")
        request = await self.fetch.started("cat")
        self.assertFalse(task.done())
        request.complete("cat result")
        await asyncio.wait_for(asyncio.shield(task), timeout=1)
        print(f"single: expected='cat result', observed={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "cat result")

    async def overlap(self, reverse):
        older_task = self.launch("ca")
        older = await self.fetch.started("ca")
        newer_task = self.launch("cat")
        newer = await self.fetch.started("cat")
        self.assertIsNot(older, newer)
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        print("controls: both actual Search requests entered fetch and remain pending", flush=True)

        if reverse:
            newer.complete("cat result")
            await asyncio.wait_for(asyncio.shield(newer_task), timeout=1)
            self.assertFalse(older_task.done())
            print(f"newer first: expected='cat result', observed={self.search.result!r}", flush=True)
            self.assertEqual(self.search.result, "cat result")
            older.complete("ca result")
            await asyncio.wait_for(asyncio.shield(older_task), timeout=1)
        else:
            older.complete("ca result")
            await asyncio.wait_for(asyncio.shield(older_task), timeout=1)
            self.assertFalse(newer_task.done())
            # The contract does not specify display policy while newer is pending.
            print(f"older first: intermediate observation={self.search.result!r}", flush=True)
            newer.complete("cat result")
            await asyncio.wait_for(asyncio.shield(newer_task), timeout=1)

        order = "reversed" if reverse else "normal"
        print(f"{order} final: expected='cat result', observed={self.search.result!r}", flush=True)
        self.assertEqual(self.search.result, "cat result", "latest query must retain final ownership")

    async def test_overlap_normal_completion(self):
        await self.overlap(reverse=False)

    async def test_overlap_reversed_completion(self):
        await self.overlap(reverse=True)

    async def test_transport_key_mismatch_is_an_assertion(self):
        self.launch("actual")
        with self.assertRaisesRegex(
            AssertionError, "request key: expected 'wrong', observed 'actual'"
        ):
            await self.fetch.started("wrong")
        print("control: deliberate key mismatch raised the expected AssertionError", flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
