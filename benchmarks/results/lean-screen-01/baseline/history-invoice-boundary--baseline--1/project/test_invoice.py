import unittest
from invoice import invoice_total


class InvoiceTests(unittest.TestCase):
    def test_positive_half_cent(self):
        self.assertEqual(invoice_total("1.005"), 101)

    def test_negative_half_cent(self):
        self.assertEqual(invoice_total("-1.005"), -101)

    def test_exact_cents(self):
        self.assertEqual(invoice_total("2.34"), 234)
