from pathlib import Path
import unittest
from client import Client

BASE = Path(__file__).resolve().parent

class PathTests(unittest.TestCase):
    def test_single_root(self):
        self.assertEqual(Client(BASE / "alpha").load(), 111)

    def test_other_filename(self):
        self.assertEqual(Client(BASE / "alpha").load("other.txt"), 333)

    def test_switch_root(self):
        client = Client(BASE / "alpha")
        self.assertEqual(client.load(), 111)
        client.select_root(BASE / "beta")
        self.assertEqual(client.load(), 222)
        client.select_root(BASE / "alpha")
        self.assertEqual(client.load(), 111)
