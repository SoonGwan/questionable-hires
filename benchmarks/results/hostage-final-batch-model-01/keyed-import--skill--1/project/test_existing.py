import unittest
from importer import Importer


class ExistingContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_active_call_forwards_arguments_and_returns_persist_result(self):
        key, payload, result = 'catalog', object(), object()
        observed = []
        async def fetch(received):
            observed.append(('fetch', received))
            return payload
        async def persist(received, data):
            self.assertIs(data, payload)
            observed.append(('persist', received))
            return result
        self.assertIs(await Importer().import_one(key, fetch, persist), result)
        self.assertEqual(observed, [('fetch', key), ('persist', key)])

    async def test_fetch_failure_preserves_exception_and_skips_persist(self):
        error = ValueError('unavailable catalog')
        async def fetch(key):
            raise error
        async def persist(key, payload):
            self.fail('persist ran after failed fetch')
        with self.assertRaises(ValueError) as caught:
            await Importer().import_one('catalog', fetch, persist)
        self.assertIs(caught.exception, error)
