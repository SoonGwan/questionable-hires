import unittest
from windows import merge_windows

class WindowsTests(unittest.TestCase):
    def test_touching(self):
        self.assertEqual(merge_windows([(1, 3), (3, 5)]), [(1, 5)])

    def test_nested(self):
        self.assertEqual(merge_windows([(1, 10), (2, 3)]), [(1, 10)])

    def test_chain(self):
        self.assertEqual(merge_windows([(7, 9), (1, 5), (4, 8)]), [(1, 9)])

    def test_disjoint(self):
        self.assertEqual(merge_windows([(5, 7), (1, 3)]), [(1, 3), (5, 7)])

    def test_empty(self):
        self.assertEqual(merge_windows([]), [])

    def test_input_preserved(self):
        source = [(5, 7), (1, 3)]
        result = merge_windows(source)
        self.assertEqual(source, [(5, 7), (1, 3)])
        self.assertIsNot(result, source)
