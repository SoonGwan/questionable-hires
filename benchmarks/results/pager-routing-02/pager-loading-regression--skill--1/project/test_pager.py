import asyncio
import unittest
from pager import Pager
from test_support import requests


class PagerTests(unittest.IsolatedAsyncioTestCase):
    async def test_single_success(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            task = start(pager.select(1))
            page, response = await next_request()
            self.assertEqual(page, 1)
            self.assertTrue(pager.loading)
            self.assertEqual(pager.rows, ['cached'])
            response.set_result(['page one'])
            await asyncio.wait_for(task, 1)
            self.assertEqual(pager.rows, ['page one'])
            self.assertFalse(pager.loading)
            self.assertIsNone(pager.error)

    def assert_state(self, pager, rows, loading, error):
        self.assertEqual(
            (pager.rows, pager.loading, pager.error),
            (rows, loading, error),
        )

    async def check_older_completion(self, *, fails):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            older = start(pager.select(2))
            page, older_response = await next_request()
            self.assertEqual(page, 2)
            self.assert_state(pager, ['cached'], True, None)

            newer = start(pager.select(3))
            page, newer_response = await next_request()
            self.assertEqual(page, 3)
            self.assert_state(pager, ['cached'], True, None)

            if fails:
                older_response.set_exception(OSError('older request failed'))
            else:
                older_response.set_result(['page two'])
            await asyncio.wait_for(older, 1)
            self.assertFalse(newer.done())
            self.assertFalse(newer_response.done())
            with self.subTest(transition='older completed, newer pending'):
                self.assert_state(pager, ['cached'], True, None)

            newer_response.set_result(['page three'])
            await asyncio.wait_for(newer, 1)
            with self.subTest(transition='latest succeeded'):
                self.assert_state(pager, ['page three'], False, None)

    async def test_older_success_while_newer_pending(self):
        await self.check_older_completion(fails=False)

    async def test_older_oserror_while_newer_pending(self):
        await self.check_older_completion(fails=True)

    async def test_latest_error_followed_by_successful_retry(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            latest = start(pager.select(4))
            page, response = await next_request()
            self.assertEqual(page, 4)
            self.assert_state(pager, ['cached'], True, None)

            response.set_exception(OSError('page four unavailable'))
            await asyncio.wait_for(latest, 1)
            self.assert_state(pager, ['cached'], False, 'page four unavailable')

            retry = start(pager.select(4))
            page, response = await next_request()
            self.assertEqual(page, 4)
            self.assert_state(pager, ['cached'], True, None)

            response.set_result(['page four'])
            await asyncio.wait_for(retry, 1)
            self.assert_state(pager, ['page four'], False, None)
