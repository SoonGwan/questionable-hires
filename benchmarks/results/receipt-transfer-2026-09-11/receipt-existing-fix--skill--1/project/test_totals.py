import unittest
from totals import accepts_total

class TotalTests(unittest.TestCase):
    def test_boundary(self):
        for cents, expected in ((4999, False), (5000, True), (5001, True)):
            with self.subTest(cents=cents):
                self.assertEqual(accepts_total(cents), expected)
