import unittest
from app import quantity, payload

class Tests(unittest.TestCase):
    def test_quantity(self):
        self.assertEqual(quantity(), 2)
    def test_payload(self):
        self.assertEqual(payload(), b"\x00\xff")
