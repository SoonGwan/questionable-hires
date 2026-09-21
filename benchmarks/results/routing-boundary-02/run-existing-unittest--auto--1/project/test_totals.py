import unittest
from totals import total

class Totals(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total([]), 0)
    def test_mixed(self):
        self.assertEqual(total([4, -1, 2]), 5)
