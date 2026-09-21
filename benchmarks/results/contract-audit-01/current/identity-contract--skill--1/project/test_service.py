import unittest
import service
class Existing(unittest.TestCase):
    def test_known(self):
        self.assertEqual(service.Registry({"a": {"n": 1}}).get("a"), {"n": 1})
    def test_missing(self):
        with self.assertRaises(KeyError):
            service.Registry({}).get("absent")
