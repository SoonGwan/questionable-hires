"""Deterministic overlap checks against the real Search; standard library only."""

import asyncio
import unittest

from search import Search


class SearchOverlapTests(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 2.0

    async def check_order(self, order):
        search = Search()
        queries = ("ca", "cat")
        values = {"ca": "results for ca", "cat": "results for cat"}
        loop = asyncio.get_running_loop()
        replies = {query: loop.create_future() for query in queries}
        entered = {query: asyncio.Event() for query in queries}
        calls = []
        completed = []
        tasks = {}

        def record(message):
            print("[{}] {}".format(" -> ".join(order), message), flush=True)

        async def fetch(query):
            calls.append(query)
            entered[query].set()
            return await replies[query]

        async def finish(query):
            replies[query].set_result(values[query])
            await asyncio.wait_for(asyncio.shield(tasks[query]), self.TIMEOUT)
            self.assertTrue(tasks[query].done())
            self.assertFalse(tasks[query].cancelled())
            self.assertIsNone(tasks[query].exception())
            completed.append(query)
            record("PASS request {!r} finished successfully".format(query))

        def assert_latest(stage):
            record("ASSERT {}: expected={!r}, actual={!r}".format(
                stage, values["cat"], search.result))
            self.assertEqual(search.result, values["cat"], stage)
            record("PASS " + stage)

        try:
            # Observe each fetch starting, without letting either complete.
            for query in queries:
                tasks[query] = asyncio.create_task(search.run(query, fetch))
                await asyncio.wait_for(entered[query].wait(), self.TIMEOUT)

            self.assertEqual(calls, list(queries))
            self.assertTrue(all(not task.done() for task in tasks.values()))
            self.assertTrue(all(not reply.done() for reply in replies.values()))
            record("PASS actual Search started ca then cat; both requests pending")

            await finish(order[0])
            self.assertFalse(tasks[order[1]].done())
            self.assertFalse(replies[order[1]].done())
            record("PASS {!r} remains pending".format(order[1]))
            if order[0] == "cat":
                assert_latest("newer result visible while older request is pending")
            # Normal order intentionally makes no intermediate display assertion.
            await finish(order[1])
            self.assertEqual(completed, list(order))
            record("PASS controlled completion order = {!r}".format(completed))
            assert_latest("latest result remains visible after both requests finish")
        finally:
            for task in tasks.values():
                if not task.done():
                    task.cancel()
            for reply in replies.values():
                if not reply.done():
                    reply.cancel()
            if tasks:
                await asyncio.wait_for(
                    asyncio.gather(*tasks.values(), return_exceptions=True),
                    self.TIMEOUT,
                )
            self.assertTrue(all(task.done() for task in tasks.values()))
            self.assertTrue(all(reply.done() for reply in replies.values()))
            record("PASS cleanup: all owned requests and reply futures settled")

    async def test_normal_completion_latest_result_after_both_finish(self):
        await self.check_order(("ca", "cat"))

    async def test_reversed_completion_older_must_not_overwrite_latest(self):
        await self.check_order(("cat", "ca"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
