"""Local component QA: python3 -B -m unittest discover -s tests -v."""

import asyncio
from dataclasses import dataclass
from typing import Any
import unittest

from search import Search


# Self-contained copy of the skill's controlled transport; no skill dependency.
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


class SearchTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.tasks = []
        # Register before any entry wait so failed waits also clean up.
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), timeout=1)

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        return task, await self.fetch.started(query)

    async def finish(self, task, request, payload):
        request.complete(payload)
        await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def seed(self):
        task, request = await self.start('seed')
        await self.finish(task, request, 'displayed seed')
        self.assertEqual(self.search.result, 'displayed seed')

    async def test_normal_request(self):
        self.assertIsNone(self.search.result)
        task, request = await self.start('normal')
        self.assertFalse(task.done())
        self.assertIsNone(self.search.result)
        await self.finish(task, request, 'normal result')
        self.assertEqual(self.search.result, 'normal result')

    async def overlap(self, newer_first):
        await self.seed()
        older_task, older = await self.start('older')
        self.assertEqual(self.search.result, 'displayed seed')
        newer_task, newer = await self.start('newer')
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        self.assertEqual(self.search.result, 'displayed seed')

        if newer_first:
            await self.finish(newer_task, newer, 'newer result')
            self.assertFalse(older_task.done())
            self.assertEqual(self.search.result, 'newer result')
            await self.finish(older_task, older, 'older result')
        else:
            await self.finish(older_task, older, 'older result')
            self.assertFalse(newer_task.done())
            self.assertFalse(newer.response.done())
            # Retention must hold after an intervening completion too.
            self.assertEqual(self.search.result, 'displayed seed')
            await self.finish(newer_task, newer, 'newer result')

        self.assertEqual(self.search.result, 'newer result')

    async def test_older_finishes_while_newer_pending_retains_display(self):
        await self.overlap(newer_first=False)

    async def test_newer_finishes_first_late_older_cannot_replace_display(self):
        await self.overlap(newer_first=True)


if __name__ == '__main__':
    unittest.main()
