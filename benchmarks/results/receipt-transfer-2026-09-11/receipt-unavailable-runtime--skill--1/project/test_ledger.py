import unittest
from ledger import amount

class LedgerTests(unittest.TestCase):
    def test_rounding(self):
        self.assertEqual(amount('1.005'), '1.00')
