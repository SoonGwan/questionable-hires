"""Local interaction QA: real Search with explicitly released fetch responses.

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search
No network, sleeps, or production changes. Each async wait is bounded.
"""

import asyncio
import unittest
from dataclasses import dataclass

from search import Search


@dataclass(frozen=True)
class Request:
    query: str
    response: asyncio.Future

    def complete(self, payload):
        self.response.set_result(payload)


class ControlledFetch:
    def __init__(self):
        self.calls = asyncio.Queue()

    async def __call__(self, query):
        request = Request(query, asyncio.get_running_loop().create_future())
        self.calls.put_nowait(request)
        return await request.response


class SearchInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.search = Search()
        self.fetch = ControlledFetch()
        self.tasks = []
        self.addAsyncCleanup(self.cleanup_tasks)

    async def cleanup_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True), timeout=1
        )

    async def start(self, query):
        task = asyncio.create_task(self.search.run(query, self.fetch))
        self.tasks.append(task)
        request = await asyncio.wait_for(self.fetch.calls.get(), timeout=1)
        self.assertEqual(request.query, query)
        return task, request

    async def complete(self, call, payload):
        task, request = call
        request.complete(payload)
        await asyncio.wait_for(task, timeout=1)

    async def test_sequential_searches(self):
        first = await self.start("cat")
        await self.complete(first, "cat results")
        self.assertEqual(self.search.result, "cat results")
        latest = await self.start("cats")
        await self.complete(latest, "cats results")
        self.assertEqual(self.search.result, "cats results")

    async def test_overlapping_searches_complete_in_input_order(self):
        first = await self.start("cat")
        latest = await self.start("cats")
        await self.complete(first, "cat results")
        # Display while the latest is pending is unspecified by the contract.
        await self.complete(latest, "cats results")
        self.assertEqual(self.search.result, "cats results")

    async def test_late_old_response_preserves_latest_result(self):
        first = await self.start("cat")
        latest = await self.start("cats")
        await self.complete(latest, "cats results")
        self.assertEqual(self.search.result, "cats results")
        await self.complete(first, "cat results")
        self.assertEqual(
            self.search.result, "cats results",
            "An older response must not replace the latest query's result",
        )

    async def test_retyping_same_query_preserves_latest_request_result(self):
        first = await self.start("cat")
        middle = await self.start("cats")
        latest = await self.start("cat")
        await self.complete(latest, "cat results from newest request")
        self.assertEqual(self.search.result, "cat results from newest request")
        # Distinct handles let identical query strings finish independently.
        for call, payload in (
            (middle, "cats results"),
            (first, "cat results from oldest request"),
        ):
            with self.subTest(late_payload=payload):
                await self.complete(call, payload)
                self.assertEqual(
                    self.search.result, "cat results from newest request",
                    "Late responses must preserve the newest completed search",
                )


if __name__ == "__main__":
    unittest.main()
