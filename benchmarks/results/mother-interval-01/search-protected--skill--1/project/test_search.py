"""Deterministic component QA; standard library only, no network or sleeps."""
import asyncio
from dataclasses import dataclass
from typing import Any
import unittest

from search import Search


# Standalone copy of the skill's controlled transport; no installed helper needed.
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


class SearchSequenceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.owned_tasks = []
        self.addAsyncCleanup(self.drain_owned_tasks)

    async def drain_owned_tasks(self):
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.owned_tasks, return_exceptions=True), 1)

    async def start(self, query, expected=None):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        # Register ownership before an entry assertion can fail.
        self.owned_tasks.append(task)
        request = await self.fetch.started(query if expected is None else expected)
        return task, request

    async def complete(self, task, request, value):
        request.complete(value)
        await asyncio.wait_for(asyncio.shield(task), 1)

    async def seed(self):
        task, request = await self.start('seed')
        await self.complete(task, request, 'existing result')
        self.assertEqual(self.search.result, 'existing result')

    async def test_normal_loading_retains_existing_result(self):
        self.assertIsNone(self.search.result)
        await self.seed()
        task, request = await self.start('next')
        self.assertFalse(task.done())
        self.assertEqual(self.search.result, 'existing result')
        await self.complete(task, request, 'next result')
        self.assertEqual(self.search.result, 'next result')

    async def check_overlap(self, newer_first, repeated=False):
        await self.seed()
        older_task, older = await self.start('query A')
        self.assertEqual(self.search.result, 'existing result')
        newer_task, newer = await self.start('query A' if repeated else 'query B')
        self.assertIsNot(older, newer)
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        self.assertEqual(self.search.result, 'existing result')
        if newer_first:
            await self.complete(newer_task, newer, 'newer result')
            self.assertFalse(older_task.done())
            self.assertEqual(self.search.result, 'newer result')
            await self.complete(older_task, older, 'older result')
        else:
            await self.complete(older_task, older, 'older result')
            self.assertFalse(newer_task.done())
            self.assertFalse(newer.response.done())
            # Retention is required through the intervening older completion.
            self.assertEqual(self.search.result, 'existing result')
            await self.complete(newer_task, newer, 'newer result')
        self.assertEqual(self.search.result, 'newer result')

    async def test_older_completes_while_newer_pending(self):
        await self.check_overlap(newer_first=False)

    async def test_newer_completes_before_older(self):
        await self.check_overlap(newer_first=True)

    async def test_repeated_query_older_completes_first(self):
        await self.check_overlap(newer_first=False, repeated=True)

    async def test_repeated_query_newer_completes_first(self):
        await self.check_overlap(newer_first=True, repeated=True)

    async def test_entry_mismatch_reports_expected_and_observed(self):
        with self.assertRaisesRegex(
            AssertionError, "request key: expected 'expected', observed 'actual'"
        ):
            await self.start('actual', expected='expected')
        # Exercise cleanup for a task whose entry assertion failed.
        await self.drain_owned_tasks()
        self.assertTrue(all(task.done() for task in self.owned_tasks))


if __name__ == '__main__':
    unittest.main()
