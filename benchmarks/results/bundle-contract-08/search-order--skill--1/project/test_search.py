"""Deterministic component regression; run: python3 -B -m unittest -v test_search."""
import asyncio
from dataclasses import dataclass
from typing import Any
import unittest

from search import Search


# Copied from the skill's controlled_fetch.py so this test is standalone.
@dataclass(frozen=True)
class Request:
    key: Any
    response: asyncio.Future

    def complete(self, value):
        self.response.set_result(value)

    def fail_request(self, error):
        self.response.set_exception(error)


class ControlledFetch:
    def __init__(self):
        self.calls = asyncio.Queue()

    async def __call__(self, key):
        request = Request(key, asyncio.get_running_loop().create_future())
        self.calls.put_nowait(request)
        return await request.response

    async def started(self, expected, timeout=1):
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        request = await asyncio.wait_for(self.calls.get(), timeout)
        if request.key != expected:
            raise AssertionError(
                f'request key: expected {expected!r}, observed {request.key!r}')
        return request


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
                    task.exception()  # Retrieve exceptions even on failed entry checks.
            self.assertFalse(pending, 'owned Search tasks did not stop within 1s')

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch), name=query)
        self.tasks.append(task)
        request = await self.fetch.started(query, timeout=1)
        self.assertFalse(task.done(), f'{query}: must await controlled response')
        print(f'CONTROL entered {query!r}; response withheld', flush=True)
        return task, request

    async def finish(self, task, request, payload):
        request.complete(payload)
        _, pending = await asyncio.wait([task], timeout=1)
        self.assertFalse(pending, f'{request.key}: did not finish within 1s')
        task.result()
        print(f'CONTROL completed {request.key!r} with {payload!r}', flush=True)

    async def test_normal_overlapping_completion(self):
        older, older_request = await self.start('ca')
        latest, latest_request = await self.start('cat')
        self.assertFalse(older.done(), 'both requests must overlap')
        await self.finish(older, older_request, 'older result')
        self.assertFalse(latest.done(), 'latest response must remain controlled')
        # The contract leaves display while the latest is pending unspecified.
        await self.finish(latest, latest_request, 'latest result')
        self.assertEqual(self.search.result, 'latest result',
                         'after both finish, latest query owns the displayed result')
        print(f'ASSERT normal final result = {self.search.result!r}: PASS', flush=True)

    async def test_reversed_overlapping_completion(self):
        older, older_request = await self.start('ca')
        latest, latest_request = await self.start('cat')
        self.assertFalse(older.done(), 'both requests must overlap')
        await self.finish(latest, latest_request, 'latest result')
        self.assertFalse(older.done(), 'older response must still be withheld')
        self.assertEqual(self.search.result, 'latest result',
                         'completed latest query must be displayed')
        print(f'ASSERT latest completed result = {self.search.result!r}: PASS', flush=True)
        await self.finish(older, older_request, 'older result')
        self.assertEqual(self.search.result, 'latest result',
                         'older response must not overwrite completed latest result')


if __name__ == '__main__':
    unittest.main(verbosity=2)
