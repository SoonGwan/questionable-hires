import unittest
from billing.service import invoice
from checks.support import example

class InvoiceTests(unittest.TestCase):
    def test_positive_tie(self):
        self.assertEqual(invoice(example('positive')), {'currency': 'USD', 'total': '1.01'})

    def test_negative_tie(self):
        self.assertEqual(invoice(example('negative')), {'currency': 'USD', 'total': '-1.01'})

    def test_sum_before_rounding(self):
        self.assertEqual(invoice(example('combined')), {'currency': 'USD', 'total': '2.01'})

    def test_empty(self):
        self.assertEqual(invoice([]), {'currency': 'USD', 'total': '0.00'})
