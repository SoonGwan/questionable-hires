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

    async def test_older_success_while_newer_pending(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            older = start(pager.select(1))
            page, older_response = await next_request()
            self.assertEqual(page, 1)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], True, None))

            newer = start(pager.select(2))
            page, newer_response = await next_request()
            self.assertEqual(page, 2)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], True, None))

            older_response.set_result(['stale page one'])
            await asyncio.wait_for(older, 1)
            self.assertFalse(newer.done())
            self.assertFalse(newer_response.done())
            with self.subTest(transition='older success, newer pending'):
                self.assertEqual(
                    (pager.rows, pager.loading, pager.error),
                    (['cached'], True, None))

            newer_response.set_result(['page two'])
            await asyncio.wait_for(newer, 1)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['page two'], False, None))

    async def test_older_oserror_while_newer_pending(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            older = start(pager.select(1))
            page, older_response = await next_request()
            self.assertEqual(page, 1)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], True, None))

            newer = start(pager.select(2))
            page, newer_response = await next_request()
            self.assertEqual(page, 2)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], True, None))

            older_response.set_exception(OSError('older request failed'))
            await asyncio.wait_for(older, 1)
            self.assertFalse(newer.done())
            self.assertFalse(newer_response.done())
            with self.subTest(transition='older OSError, newer pending'):
                self.assertEqual(
                    (pager.rows, pager.loading, pager.error),
                    (['cached'], True, None))

            newer_response.set_result(['page two'])
            await asyncio.wait_for(newer, 1)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['page two'], False, None))

    async def test_latest_error_then_successful_retry(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            latest = start(pager.select(2))
            page, response = await next_request()
            self.assertEqual(page, 2)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], True, None))

            response.set_exception(OSError('page two unavailable'))
            await asyncio.wait_for(latest, 1)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], False, 'page two unavailable'))

            retry = start(pager.select(2))
            page, retry_response = await next_request()
            self.assertEqual(page, 2)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['cached'], True, None))

            retry_response.set_result(['page two after retry'])
            await asyncio.wait_for(retry, 1)
            self.assertEqual(
                (pager.rows, pager.loading, pager.error),
                (['page two after retry'], False, None))
