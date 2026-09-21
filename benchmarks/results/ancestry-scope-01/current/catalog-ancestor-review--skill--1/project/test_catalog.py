import unittest
from catalog import Catalog

class CatalogTests(unittest.TestCase):
    def test_shared_catalog(self):
        calls = []
        def fetch(tenant, item):
            calls.append((tenant, item))
            return tenant + ':' + item
        catalog = Catalog(fetch)
        self.assertEqual(catalog.lookup('east', '17'), 'east:17')
        self.assertEqual(catalog.lookup('west', '17'), 'west:17')
        self.assertEqual(catalog.lookup('east', '17'), 'east:17')
        self.assertEqual(calls, [('east', '17'), ('west', '17')])

    def test_single_tenant(self):
        catalog = Catalog(lambda tenant, item: tenant + ':' + item)
        self.assertEqual(catalog.lookup('east', '17'), 'east:17')
        self.assertEqual(catalog.lookup('east', '18'), 'east:18')
