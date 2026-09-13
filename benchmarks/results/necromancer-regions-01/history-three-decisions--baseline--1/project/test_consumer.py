import unittest
from consumer import render

class RenderTests(unittest.TestCase):
    def test_legacy(self):
        self.assertEqual(render({'name': 'Ada', 'amount': 0}), ('unknown', 'Ada', 0))
    def test_empty(self):
        self.assertEqual(render({'name': 'Ada', 'display_name': '', 'code': '', 'amount': 2}), ('unknown', 'Ada', 2))
    def test_current(self):
        self.assertEqual(render({'name': 'Ada', 'display_name': 'A', 'code': 'X', 'amount': 3}), ('X', 'A', 3))
    def test_negative(self):
        with self.assertRaises(ValueError):
            render({'name': 'Ada', 'amount': -1})
