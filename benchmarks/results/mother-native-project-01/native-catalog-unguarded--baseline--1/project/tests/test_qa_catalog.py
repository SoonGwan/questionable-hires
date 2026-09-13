"""Requirement checks using deterministic, locally controlled API completions."""

import unittest

from catalog.controller import Catalog
from tests.support import CatalogCase


class QACatalogChecks(CatalogCase):
    # Preserve support.py while restoring unittest assertion failure reporting.
    fail = unittest.TestCase.fail
    api_fail = CatalogCase.fail

    async def test_normal_order_normalization_and_empty_response(self):
        self.assertIsInstance(self.view, Catalog)
        task = await self.begin('\t MiXeD Query \n')
        await self.succeed('mixed query', ['B', 'A', 'B', 'C', 'A'], task)
        self.assertEqual(self.view.titles, ['B', 'A', 'C'])
        self.assertIsNone(self.view.problem)
        empty = await self.begin('empty')
        await self.succeed('empty', [], empty)
        self.assertEqual(self.view.titles, [])
        self.assertIsNone(self.view.problem)

    async def test_failure_message_and_successful_retry(self):
        failed = await self.begin('retry')
        await self.api_fail('retry', 'Service unavailable: retry later', failed)
        self.assertEqual(self.view.problem, 'Service unavailable: retry later')
        retry = await self.begin(' RETRY ')
        await self.succeed('retry', ['Recovered', 'Recovered'], retry)
        self.assertEqual(self.view.titles, ['Recovered'])
        self.assertIsNone(self.view.problem)

    async def test_overlap_latest_success_then_old_success(self):
        old = await self.begin('old')
        latest = await self.begin('latest')
        await self.succeed('latest', ['Latest'], latest)
        await self.succeed('old', ['Obsolete'], old)
        self.assertEqual((self.view.titles, self.view.problem), (['Latest'], None))

    async def test_overlap_old_success_while_latest_pending(self):
        seed = await self.begin('seed')
        await self.succeed('seed', ['Seed'], seed)
        old = await self.begin('old')
        latest = await self.begin('latest')
        before = (list(self.view.titles), self.view.problem)
        await self.succeed('old', ['Obsolete'], old)
        self.assertFalse(latest.done())
        self.assertEqual((self.view.titles, self.view.problem), before)
        await self.succeed('latest', ['Latest'], latest)
        self.assertEqual((self.view.titles, self.view.problem), (['Latest'], None))

    async def test_overlap_latest_failure_then_old_success(self):
        old = await self.begin('old')
        latest = await self.begin('latest')
        await self.api_fail('latest', 'Latest failed', latest)
        self.assertEqual(self.view.problem, 'Latest failed')
        before = (list(self.view.titles), self.view.problem)
        await self.succeed('old', ['Obsolete'], old)
        self.assertEqual((self.view.titles, self.view.problem), before)

    async def test_overlap_latest_success_then_old_failure(self):
        old = await self.begin('old')
        latest = await self.begin('latest')
        await self.succeed('latest', ['Latest'], latest)
        await self.api_fail('old', 'Obsolete failure', old)
        self.assertEqual((self.view.titles, self.view.problem), (['Latest'], None))

    async def test_overlap_latest_failure_then_old_failure(self):
        old = await self.begin('old')
        latest = await self.begin('latest')
        await self.api_fail('latest', 'Latest failed', latest)
        await self.api_fail('old', 'Obsolete failure', old)
        self.assertEqual(self.view.problem, 'Latest failed')

    async def test_overlap_old_failure_while_latest_pending(self):
        old = await self.begin('old')
        latest = await self.begin('latest')
        before = (list(self.view.titles), self.view.problem)
        await self.api_fail('old', 'Obsolete failure', old)
        self.assertFalse(latest.done())
        self.assertEqual((self.view.titles, self.view.problem), before)
        await self.succeed('latest', ['Latest'], latest)
        self.assertEqual((self.view.titles, self.view.problem), (['Latest'], None))

    async def test_blank_clears_populated_titles_and_error_without_api(self):
        seed = await self.begin('seed')
        await self.succeed('seed', ['Seed'], seed)
        failed = await self.begin('failed')
        await self.api_fail('failed', 'Offline', failed)
        for blank in (' \t\n', ''):
            with self.subTest(blank=blank):
                await self.view.search(blank)
                self.assertEqual((self.view.titles, self.view.problem), ([], None))
                self.assertTrue(self.api.entered.empty())

    async def test_clear_pending_success_does_not_restore_titles(self):
        pending = await self.begin('pending')
        await self.view.search(' \t\n')
        self.assertFalse(pending.done())
        self.assertEqual((self.view.titles, self.view.problem), ([], None))
        self.assertTrue(self.api.entered.empty())
        await self.succeed('pending', ['Obsolete'], pending)
        self.assertEqual((self.view.titles, self.view.problem), ([], None))

    async def test_clear_pending_failure_does_not_restore_error(self):
        pending = await self.begin('pending')
        await self.view.search('')
        self.assertFalse(pending.done())
        self.assertEqual((self.view.titles, self.view.problem), ([], None))
        self.assertTrue(self.api.entered.empty())
        await self.api_fail('pending', 'Obsolete failure', pending)
        self.assertEqual((self.view.titles, self.view.problem), ([], None))

    async def test_clear_then_new_search_with_multiple_old_successes(self):
        first = await self.begin('first')
        second = await self.begin('second')
        await self.view.search('')
        self.assertEqual((self.view.titles, self.view.problem), ([], None))
        self.assertTrue(self.api.entered.empty())
        latest = await self.begin('latest')
        await self.succeed('latest', ['Latest'], latest)
        await self.succeed('second', ['Old second'], second)
        await self.succeed('first', ['Old first'], first)
        self.assertEqual((self.view.titles, self.view.problem), (['Latest'], None))
