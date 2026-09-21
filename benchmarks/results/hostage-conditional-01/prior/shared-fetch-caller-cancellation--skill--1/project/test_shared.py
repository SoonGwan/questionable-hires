import unittest
from shared import Loader
class Existing(unittest.IsolatedAsyncioTestCase):
    async def test_single_result(self):
        value = object()
        async def fetch(key):
            self.assertEqual(key, "one")
            return value
        self.assertIs(await Loader(fetch).load("one"), value)
