import unittest
from settings import resolve

class SettingsTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(resolve({'retries': 3}, {}, {}), {'retries': 3})
    def test_environment(self):
        self.assertEqual(resolve({'retries': 3}, {'retries': 4}, {}), {'retries': 4})
    def test_override(self):
        self.assertEqual(resolve({'retries': 3}, {}, {'retries': 5}), {'retries': 5})
    def test_absent_override(self):
        self.assertEqual(resolve({'retries': 3}, {}, {'retries': None}), {'retries': 3})
