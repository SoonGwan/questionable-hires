from tests.support import CatalogCase


class ExistingChecks(CatalogCase):
    async def test_normal_normalizes_query_and_deduplicates_titles(self):
        task = await self.begin(' Books ')
        await self.succeed('books', ['One', 'One', 'Two'], task)
        self.assertEqual(self.view.titles, ['One', 'Two'])
        self.assertIsNone(self.view.problem)

    async def test_blank_does_not_call_api(self):
        await self.view.search('   ')
        self.assertEqual(self.view.titles, [])
        self.assertIsNone(self.view.problem)
        self.assertTrue(self.api.entered.empty())

    async def test_current_failure_then_retry(self):
        failed = await self.begin('books')
        await self.fail('books', 'offline', failed)
        self.assertEqual(self.view.problem, 'offline')
        retry = await self.begin('books')
        await self.succeed('books', ['Recovered'], retry)
        self.assertEqual(self.view.titles, ['Recovered'])
        self.assertIsNone(self.view.problem)
