"""Local component regression: python3 -B -m unittest -v test_search."""
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
                    task.exception()
            self.assertFalse(pending, 'owned Search tasks failed to stop within 1s')

    async def start_request(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        self.assertFalse(task.done(), 'request must wait for controlled response')
        print(f'CONTROL: {query!r} entered fetch and is pending', flush=True)
        return task, request

    async def finish_request(self, task, request, payload):
        request.complete(payload)
        await asyncio.wait_for(asyncio.shield(task), timeout=1)
        print(
            f'CONTROL: completed {request.key!r} with {payload!r}; '
            f'displayed={self.search.result!r}',
            flush=True,
        )

    async def test_normal_completion_latest_after_both_finish(self):
        older_task, older = await self.start_request('ca')
        latest_task, latest = await self.start_request('cat')
        await self.finish_request(older_task, older, 'results for ca')
        self.assertFalse(latest_task.done(), 'latest request must still be pending')
        # The display during this interval is intentionally unspecified.
        await self.finish_request(latest_task, latest, 'results for cat')
        self.assertEqual(
            self.search.result, 'results for cat',
            'latest result must be displayed after both requests finish normally',
        )

    async def test_reversed_completion_older_cannot_overwrite_latest(self):
        older_task, older = await self.start_request('ca')
        latest_task, latest = await self.start_request('cat')
        await self.finish_request(latest_task, latest, 'results for cat')
        self.assertFalse(older_task.done(), 'older request must still be pending')
        self.assertEqual(
            self.search.result, 'results for cat',
            'completed latest result must be displayed while older is pending',
        )
        await self.finish_request(older_task, older, 'results for ca')
        self.assertEqual(
            self.search.result, 'results for cat',
            'older completion must not overwrite the completed latest result',
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
