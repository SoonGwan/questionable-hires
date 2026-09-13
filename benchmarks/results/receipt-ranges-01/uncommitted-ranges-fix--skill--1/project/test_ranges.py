import unittest
import ranges

class RangeTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(ranges.coalesce([]), [])
    def test_disjoint(self):
        self.assertEqual(ranges.coalesce([(5, 7), (1, 3)]), [(1, 3), (5, 7)])
    def test_overlap(self):
        self.assertEqual(ranges.coalesce([(1, 4), (3, 8)]), [(1, 8)])
    def test_nested(self):
        self.assertEqual(ranges.coalesce([(1, 9), (2, 3)]), [(1, 9)])
    def test_touching(self):
        self.assertEqual(ranges.coalesce([(1, 4), (4, 8)]), [(1, 8)])
    def test_bridge(self):
        self.assertEqual(ranges.coalesce([(7, 9), (1, 4), (4, 7)]), [(1, 9)])
    def test_input_preserved(self):
        value = [(6, 9), (1, 3)]
        ranges.coalesce(value)
        self.assertEqual(value, [(6, 9), (1, 3)])
