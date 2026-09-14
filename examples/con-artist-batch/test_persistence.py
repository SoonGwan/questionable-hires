import unittest

from service import save


class PersistenceTests(unittest.TestCase):
    def test_keeps_exact_records(self):
        store = ['existing']
        save(store, 'new')
        self.assertEqual(store, ['existing', 'new'])
