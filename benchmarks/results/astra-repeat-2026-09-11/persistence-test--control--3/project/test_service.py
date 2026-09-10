import unittest
from service import save

class SaveTests(unittest.TestCase):
    def test_save(self):
        store = ['existing']
        self.assertTrue(save(store, 'record')['ok'])
        self.assertEqual(store, ['existing', 'record'])
