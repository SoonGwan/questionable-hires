"""Local diagnosis: exercise real Search and transport with cache-free requests.

Run from the project root:
    python3 -B -m unittest discover -s experiments -p 'test_search_order.py' -v
The assertions document current behavior; they are not desired-behavior tests.
"""

import asyncio
import unittest

from search import Search
from transport import fetch


class SearchOrderProbe(unittest.IsolatedAsyncioTestCase):
    async def scenario(self, completion_order, sequential=False):
        search = Search()
        queries = ('old', 'new')
        started = {q: asyncio.Event() for q in queries}
        responses = {q: asyncio.get_running_loop().create_future() for q in queries}
        calls = []
        trace = []
        tasks = {}

        async def request(url, *, params, headers):
            query = params['q']
            calls.append((url, dict(params), dict(headers)))
            started[query].set()
            # No cache or network: each query has its own explicitly released response.
            return await responses[query]

        async def actual_fetch(query):
            return await fetch(query, request)

        async def submit(query):
            tasks[query] = asyncio.create_task(search.run(query, actual_fetch))
            await asyncio.wait_for(started[query].wait(), timeout=1)

        async def complete(query):
            responses[query].set_result('fresh:' + query)
            await asyncio.wait_for(tasks[query], timeout=1)
            trace.append((query, search.result))

        try:
            await submit('old')
            if sequential:
                await complete('old')
                await submit('new')
                await complete('new')
            else:
                await submit('new')
                for query in completion_order:
                    await complete(query)

            self.assertEqual(calls, [
                ('/search', {'q': q}, {'Cache-Control': 'no-cache'})
                for q in queries
            ])
            self.assertEqual(trace, [(q, 'fresh:' + q) for q in completion_order])
            self.assertEqual(search.result, 'fresh:' + completion_order[-1])
            print('mode={} submit=old,new complete={} states={} final={} '
                  'cache=absent headers=no-cache'.format(
                      'sequential' if sequential else 'overlap',
                      ','.join(completion_order), trace, search.result), flush=True)
        finally:
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks.values(), return_exceptions=True)

    async def test_sequential_control(self):
        await self.scenario(('old', 'new'), sequential=True)

    async def test_overlapping_in_order_control(self):
        await self.scenario(('old', 'new'))

    async def test_overlapping_reverse_order_reproduces_stale_result(self):
        await self.scenario(('new', 'old'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
