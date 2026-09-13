"""Local interaction regression: python3 -m unittest -v test_search.

Latest invocation owns the final result; loading retains the displayed result.
The display after an older completion while the latest is pending is observed,
not prescribed. Uses actual Search, no network, dependencies, or timed sleeps.
"""
import asyncio
import unittest
from dataclasses import dataclass
from typing import Any

from search import Search


# Adapted from the skill's copiable controlled_fetch.py; standalone test support.
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
        self.owned = []
        self.addAsyncCleanup(self.cleanup_owned)

    async def cleanup_owned(self):
        for task in self.owned:
            if not task.done():
                task.cancel()
        if self.owned:
            done, pending = await asyncio.wait(self.owned, timeout=1)
            for task in done:
                if not task.cancelled():
                    task.exception()  # Retrieve exceptions even after failed checks.
            self.assertFalse(pending, 'owned Search tasks did not stop within 1s')

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.owned.append(task)  # Own it before entry checks can fail.
        request = await self.fetch.started(query)
        return task, request

    async def finish(self, task, request, payload):
        request.complete(payload)
        await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def seed(self):
        task, request = await self.start('seed')
        self.assertIsNone(self.search.result)
        await self.finish(task, request, 'existing result')
        self.assertEqual(self.search.result, 'existing result')

    async def test_normal_search(self):
        await self.seed()
        print('normal: pending=None; completed=existing result', flush=True)

    async def overlap(self, older_first, repeated=False):
        await self.seed()
        older_task, older = await self.start('same' if repeated else 'older')
        self.assertEqual(self.search.result, 'existing result')
        newer_task, newer = await self.start('same' if repeated else 'newer')
        self.assertIsNot(older, newer)
        self.assertFalse(older_task.done())
        self.assertFalse(newer_task.done())
        self.assertEqual(self.search.result, 'existing result')
        label = f'{"same key" if repeated else "distinct keys"}, '
        if older_first:
            label += 'older then newer'
            await self.finish(older_task, older, 'older result')
            self.assertFalse(newer.response.done())
            self.assertFalse(newer_task.done())
            intermediate = self.search.result
            # No assertion on unspecified older-first intermediate display.
            await self.finish(newer_task, newer, 'newer result')
        else:
            label += 'newer then older'
            await self.finish(newer_task, newer, 'newer result')
            self.assertFalse(older.response.done())
            self.assertFalse(older_task.done())
            self.assertEqual(self.search.result, 'newer result')
            intermediate = self.search.result
            await self.finish(older_task, older, 'older result')
        print(f'{label}: loading=existing result; '
              f'first completion={intermediate!r}; final={self.search.result!r}',
              flush=True)
        self.assertEqual(self.search.result, 'newer result')

    async def test_older_then_newer(self):
        await self.overlap(older_first=True)

    async def test_newer_then_older(self):
        await self.overlap(older_first=False)

    async def test_same_query_older_then_newer(self):
        await self.overlap(older_first=True, repeated=True)

    async def test_same_query_newer_then_older(self):
        await self.overlap(older_first=False, repeated=True)

    async def test_controlled_entry_mismatch_reports_expected_and_observed(self):
        task = asyncio.create_task(self.search.run('actual', self.fetch))
        self.owned.append(task)
        with self.assertRaisesRegex(
            AssertionError, "request key: expected 'expected', observed 'actual'"
        ):
            await self.fetch.started('expected')
        # Cleanup must cancel/drain even though the entry assertion lost the handle.


if __name__ == '__main__':
    unittest.main()
