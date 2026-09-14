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

    async def check_older_completion(self, older_error=None):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            self.assert_state(pager, ['cached'], False, None)

            older = start(pager.select(1))
            page, older_response = await next_request()
            self.assertEqual(page, 1)
            self.assert_state(pager, ['cached'], True, None)

            newer = start(pager.select(2))
            page, newer_response = await next_request()
            self.assertEqual(page, 2)
            self.assert_state(pager, ['cached'], True, None)

            if older_error is None:
                older_response.set_result(['older page'])
            else:
                older_response.set_exception(older_error)
            await asyncio.wait_for(older, 1)

            # Inspect the completed older request before releasing the newer one.
            # A subtest lets the latest completion be checked even on regression.
            with self.subTest(transition='older complete, newer pending'):
                self.assertFalse(newer_response.done())
                self.assertFalse(newer.done())
                self.assert_state(pager, ['cached'], True, None)

            newer_response.set_result(['newer page'])
            await asyncio.wait_for(newer, 1)
            self.assert_state(pager, ['newer page'], False, None)

    async def test_older_success_while_newer_pending(self):
        await self.check_older_completion()

    async def test_older_oserror_while_newer_pending(self):
        await self.check_older_completion(OSError('older request failed'))

    async def test_latest_error_followed_by_successful_retry(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            self.assert_state(pager, ['cached'], False, None)

            latest = start(pager.select(3))
            page, response = await next_request()
            self.assertEqual(page, 3)
            self.assert_state(pager, ['cached'], True, None)

            response.set_exception(OSError('latest request failed'))
            await asyncio.wait_for(latest, 1)
            self.assert_state(pager, ['cached'], False, 'latest request failed')

            retry = start(pager.select(3))
            page, response = await next_request()
            self.assertEqual(page, 3)
            self.assert_state(pager, ['cached'], True, None)

            response.set_result(['retried page'])
            await asyncio.wait_for(retry, 1)
            self.assert_state(pager, ['retried page'], False, None)
