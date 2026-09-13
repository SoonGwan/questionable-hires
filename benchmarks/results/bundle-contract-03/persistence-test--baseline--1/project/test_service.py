import unittest
from service import save

class SaveTests(unittest.TestCase):
    def test_save(self):
        self.assertTrue(save([], 'record')['ok'])
