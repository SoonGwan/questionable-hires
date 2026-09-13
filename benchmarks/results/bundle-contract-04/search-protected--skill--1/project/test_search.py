"""Deterministic component QA. Run: python3 -B -m unittest -v test_search

All waits are bounded by one second; fetches use local controlled futures.
Transport support adapted from the project's mother-in-law skill asset.
"""
import asyncio
from dataclasses import dataclass
import unittest

from search import Search


@dataclass(frozen=True)
class Request:
    key: object
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


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
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
                    task.exception()
            self.assertFalse(pending, 'owned Search tasks did not stop within 1s')

    async def start_query(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned_tasks.append(task)
        request = await self.fetch.started(query)
        return task, request

    async def finish_task(self, task):
        await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def seed_result(self):
        task, request = await self.start_query('seed')
        self.assertIsNone(self.search.result)
        self.assertFalse(task.done())
        request.complete('existing result')
        await self.finish_task(task)
        self.assertEqual(self.search.result, 'existing result')

    async def start_overlap(self):
        await self.seed_result()
        older_task, older = await self.start_query('older')
        self.assertEqual(self.search.result, 'existing result')
        newer_task, newer = await self.start_query('newer')
        self.assertEqual(self.search.result, 'existing result')
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        self.assertFalse(older.response.done())
        self.assertFalse(newer.response.done())
        return older_task, older, newer_task, newer

    async def test_single_request_displays_result(self):
        await self.seed_result()

    async def test_older_completes_while_newer_pending(self):
        older_task, older, newer_task, newer = await self.start_overlap()
        older.complete('older result')
        await self.finish_task(older_task)
        self.assertFalse(newer_task.done())
        self.assertFalse(newer.response.done())
        self.assertEqual(self.search.result, 'existing result')
        newer.complete('newer result')
        await self.finish_task(newer_task)
        self.assertEqual(self.search.result, 'newer result')

    async def test_newer_completes_before_older(self):
        older_task, older, newer_task, newer = await self.start_overlap()
        newer.complete('newer result')
        await self.finish_task(newer_task)
        self.assertFalse(older_task.done())
        self.assertFalse(older.response.done())
        self.assertEqual(self.search.result, 'newer result')
        older.complete('older result')
        await self.finish_task(older_task)
        self.assertEqual(self.search.result, 'newer result')

    async def test_transport_key_mismatch_raises_assertion(self):
        # Exercise the support assertion's failure path in an isolated case.
        task = asyncio.create_task(self.search.run('actual', self.fetch))
        self.owned_tasks.append(task)
        with self.assertRaisesRegex(
            AssertionError, "request key: expected 'expected', observed 'actual'"
        ):
            await self.fetch.started('expected')
        # Pending work is cancelled and awaited by bounded owned-task cleanup.


if __name__ == '__main__':
    unittest.main(verbosity=2)
