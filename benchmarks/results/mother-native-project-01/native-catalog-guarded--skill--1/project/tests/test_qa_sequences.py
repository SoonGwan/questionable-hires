import asyncio

from tests.support import CatalogCase


class QASequences(CatalogCase):
    async def test_overlapping_searches_only_latest_may_update_state(self):
        for old_fails in (False, True):
            for new_fails in (False, True):
                for old_first in (False, True):
                    with self.subTest(old_fails=old_fails,
                                      new_fails=new_fails,
                                      old_first=old_first):
                        await asyncio.wait_for(self.view.search(''), 0.5)
                        old = await self.begin('old')
                        new = await self.begin('new')

                        async def finish_old():
                            if old_fails:
                                await self.fail('old', 'stale failure', old)
                            else:
                                await self.succeed('old', ['Stale'], old)

                        if old_first:
                            await finish_old()
                            self.assertEqual(self.view.titles, [])
                            self.assertIsNone(self.view.problem)
                        if new_fails:
                            await self.fail('new', 'current failure', new)
                        else:
                            await self.succeed('new', ['Latest'], new)
                        if not old_first:
                            await finish_old()
                        self.assertEqual(self.view.titles,
                                         [] if new_fails else ['Latest'])
                        self.assertEqual(self.view.problem,
                                         'current failure' if new_fails else None)

    async def test_clear_invalidates_pending_success_and_failure(self):
        for fails in (False, True):
            with self.subTest(pending_fails=fails):
                seed = await self.begin('seed')
                await self.succeed('seed', ['Visible'], seed)
                failed = await self.begin('failed')
                await self.fail('failed', 'Visible error', failed)
                pending = await self.begin('pending')
                await asyncio.wait_for(self.view.search(' \t\n '), 0.5)
                self.assertEqual(self.view.titles, [])
                self.assertIsNone(self.view.problem)
                self.assertTrue(self.api.entered.empty())
                if fails:
                    await self.fail('pending', 'Late error', pending)
                else:
                    await self.succeed('pending', ['Late title'], pending)
                self.assertEqual(self.view.titles, [])
                self.assertIsNone(self.view.problem)
                retry = await self.begin('retry')
                await self.succeed('retry', ['Recovered'], retry)
                self.assertEqual(self.view.titles, ['Recovered'])
                self.assertIsNone(self.view.problem)

    async def test_repeat_normalized_query_does_not_accept_first_response(self):
        first = await self.begin(' Books ')
        first_response = self.api.pending['books']
        second = await self.begin('BOOKS')
        await self.succeed('books', ['Second'], second)
        first_response.set_result([{'title': 'First'}])
        await asyncio.wait_for(first, 0.5)
        self.assertEqual(self.view.titles, ['Second'])
        self.assertIsNone(self.view.problem)

    async def test_clear_then_new_search_rejects_pre_clear_response(self):
        old = await self.begin('old')
        await asyncio.wait_for(self.view.search(''), 0.5)
        new = await self.begin('new')
        await self.succeed('new', ['New'], new)
        await self.fail('old', 'Before clear', old)
        self.assertEqual(self.view.titles, ['New'])
        self.assertIsNone(self.view.problem)

    async def test_current_oserror_displays_message_and_retry_recovers(self):
        failed = await self.begin('books')
        self.api.pending['books'].set_exception(OSError('connection lost'))
        outcome = (await asyncio.wait_for(
            asyncio.gather(failed, return_exceptions=True), 0.5))[0]
        with self.subTest(checkpoint='current failure message'):
            self.assertEqual(
                self.view.problem, 'connection lost',
                f'Current API failure must be displayed; observed problem='
                f'{self.view.problem!r}, task outcome={outcome!r}')
        retry = await self.begin('books')
        await self.succeed('books', ['Recovered'], retry)
        self.assertEqual(self.view.titles, ['Recovered'])
        self.assertIsNone(self.view.problem)
