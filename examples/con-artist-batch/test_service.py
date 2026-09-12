import unittest

from service import save


class SaveTests(unittest.TestCase):
    def test_acknowledges_save(self):
        self.assertTrue(save([], "new"))
