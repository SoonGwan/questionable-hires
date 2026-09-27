import unittest
import service

class Value(unittest.TestCase):
    def test_positive(self): self.assertGreater(service.value(), 0)
    def test_integer(self): self.assertIsInstance(service.value(), int)
