"""Contract checks using the real Catalog and the project's controlled API."""

import asyncio
import unittest
from itertools import product

from catalog.controller import Catalog
from tests.support import CatalogCase


class QACatalogChecks(CatalogCase):
    def fail(self, *args):
        # CatalogCase uses fail(query, message, task) as an async API helper;
        # preserve unittest's single-message assertion failure path as well.
        if len(args) == 1:
            return unittest.TestCase.fail(self, args[0])
        return super().fail(*args)

    async def settle(self, future, task, outcome, label):
        if outcome == 'success':
            future.set_result([{'title': label}])
        else:
            future.set_exception(RuntimeError(label))
        await asyncio.wait_for(task, 0.5)

    def snapshot(self):
        return list(self.view.titles), self.view.problem

    async def seed_titles(self):
        task = await self.begin('seed')
        await self.succeed('seed', ['Seed'], task)

    async def test_normal_order_case_whitespace_and_empty_results(self):
        self.assertIsInstance(self.view, Catalog)
        task = await self.begin('\t MiXeD QUERY \n')
        await self.succeed('mixed query', ['B', 'A', 'B', 'a', '', 'A', 'C'], task)
        self.assertEqual(self.snapshot(), (['B', 'A', 'a', '', 'C'], None))
        empty = await self.begin('empty')
        await self.succeed('empty', [], empty)
        self.assertEqual(self.snapshot(), ([], None))

    async def test_repeated_failure_and_empty_successful_retry(self):
        await self.seed_titles()
        for message in ('offline', 'still offline'):
            task = await self.begin('retry')
            await self.fail('retry', message, task)
            self.assertEqual(self.view.problem, message)
        task = await self.begin('retry')
        await self.succeed('retry', [], task)
        self.assertEqual(self.snapshot(), ([], None))

    async def check_overlap(self, same_query):
        for newer_first, old_outcome, new_outcome in product(
            (False, True), ('success', 'failure'), ('success', 'failure')
        ):
            with self.subTest(newer_first=newer_first, old=old_outcome, new=new_outcome):
                await self.seed_titles()
                old = await self.begin(' Query ')
                old_future = self.api.pending['query']
                new_text = 'QUERY' if same_query else 'new query'
                new = await self.begin(new_text)
                new_future = self.api.pending[new_text.lower()]
                # Capture each future: support.pending keys alone cannot distinguish
                # two in-flight calls with the same normalized query.
                self.assertIsNot(old_future, new_future)
                before = self.snapshot()
                if newer_first:
                    await self.settle(new_future, new, new_outcome, 'new result')
                    newest = self.snapshot()
                    await self.settle(old_future, old, old_outcome, 'old result')
                    self.assertEqual(self.snapshot(), newest)
                else:
                    await self.settle(old_future, old, old_outcome, 'old result')
                    self.assertEqual(self.snapshot(), before)
                    await self.settle(new_future, new, new_outcome, 'new result')
                if new_outcome == 'success':
                    self.assertEqual(self.snapshot(), (['new result'], None))
                else:
                    self.assertEqual(self.view.problem, 'new result')

    async def test_overlapping_distinct_queries(self):
        await self.check_overlap(same_query=False)

    async def test_overlapping_identical_normalized_queries(self):
        await self.check_overlap(same_query=True)

    async def test_clear_invalidates_all_pending_successes_and_failures(self):
        for blank, first_outcome, second_outcome in product(
            ('', ' \t\n'), ('success', 'failure'), ('success', 'failure')
        ):
            with self.subTest(blank=repr(blank), first=first_outcome, second=second_outcome):
                await self.seed_titles()
                failed = await self.begin('failed')
                await self.fail('failed', 'previous error', failed)
                first = await self.begin('first')
                second = await self.begin('second')
                await asyncio.wait_for(self.view.search(blank), 0.5)
                self.assertEqual(self.snapshot(), ([], None))
                self.assertTrue(self.api.entered.empty(), 'blank search called API')
                self.assertFalse(first.done())
                self.assertFalse(second.done())
                await self.settle(self.api.pending['second'], second, second_outcome, 'second')
                self.assertEqual(self.snapshot(), ([], None))
                await self.settle(self.api.pending['first'], first, first_outcome, 'first')
                self.assertEqual(self.snapshot(), ([], None))

    async def test_new_search_after_clear_survives_older_completion(self):
        for old_outcome in ('success', 'failure'):
            with self.subTest(old=old_outcome):
                old = await self.begin('same')
                old_future = self.api.pending['same']
                await self.view.search('')
                new = await self.begin('same')
                await self.succeed('same', ['Fresh'], new)
                await self.settle(old_future, old, old_outcome, 'obsolete')
                self.assertEqual(self.snapshot(), (['Fresh'], None))

    async def test_current_oserror_displays_message_and_retry_recovers(self):
        task = await self.begin('books')
        self.api.pending['books'].set_exception(OSError('offline'))
        escaped = None
        try:
            await asyncio.wait_for(task, 0.5)
        except OSError as error:
            escaped = str(error)
        failure_state = escaped, self.view.problem
        retry = await self.begin('books')
        await self.succeed('books', ['Recovered'], retry)
        self.assertEqual(self.snapshot(), (['Recovered'], None))
        self.assertEqual(
            failure_state, (None, 'offline'),
            'Current API failure should display its message instead of escaping search()',
        )
