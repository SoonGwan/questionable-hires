import json
import unittest
import service
class Existing(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(set(json.loads(service.render([4, 4, 2]))), {"ids", "count"})
    def test_empty(self):
        self.assertEqual(json.loads(service.render([])), {"ids": [], "count": 0})
