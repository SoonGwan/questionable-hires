"""Deterministic component QA; imports actual Search and uses only the stdlib."""
import asyncio
import unittest

from controlled_fetch import ControlledFetch
from search import Search


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.owned = []
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        for task in self.owned:
            if not task.done():
                task.cancel()
        if self.owned:
            await asyncio.wait_for(
                asyncio.gather(*self.owned, return_exceptions=True), timeout=1
            )

    def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned.append(task)
        return task

    async def finish(self, task):
        await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def overlapping(self):
        older_task = self.start('c')
        older = await self.fetch.started('c')
        newer_task = self.start('cat')
        newer = await self.fetch.started('cat')
        self.assertIsNot(older, newer)
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        self.assertFalse(older.response.done())
        self.assertFalse(newer.response.done())
        print('CONTROL: c and cat both entered fetch and are pending', flush=True)
        return older_task, older, newer_task, newer

    async def test_normal_completion_latest_after_both_finish(self):
        older_task, older, newer_task, newer = await self.overlapping()
        older.complete('older result')
        await self.finish(older_task)
        self.assertFalse(newer_task.done())
        self.assertFalse(newer.response.done())
        # Pending display is deliberately unconstrained by the contract.
        print(f'OBSERVATION: older finished, newer pending; display={self.search.result!r}',
              flush=True)
        newer.complete('latest result')
        await self.finish(newer_task)
        self.assertEqual(self.search.result, 'latest result',
                         'latest result must be displayed after both finish normally')
        print('ASSERTION PASS: normal completion final display is latest result', flush=True)

    async def test_reversed_completion_latest_survives_older(self):
        older_task, older, newer_task, newer = await self.overlapping()
        newer.complete('latest result')
        await self.finish(newer_task)
        self.assertFalse(older_task.done())
        self.assertFalse(older.response.done())
        self.assertEqual(self.search.result, 'latest result')
        print('ASSERTION PASS: newer finished first; latest result displayed, older pending',
              flush=True)
        older.complete('older result')
        await self.finish(older_task)
        print(f'OBSERVATION: both finished in reverse order; display={self.search.result!r}',
              flush=True)
        self.assertEqual(self.search.result, 'latest result',
                         'older response must not overwrite the completed latest result')

    async def test_transport_key_mismatch_raises_actual_assertion(self):
        # Isolated negative control exercises custom assertion plumbing.
        self.start('actual')
        with self.assertRaisesRegex(
            AssertionError, "request key: expected 'different', observed 'actual'"
        ):
            await self.fetch.started('different')
        print('CONTROL PASS: deliberate key mismatch raised the expected AssertionError',
              flush=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
