import unittest
from eligibility import eligible

class EligibilityTests(unittest.TestCase):
    def test_minor(self):
        self.assertFalse(eligible(17))
    def test_exactly_eighteen(self):
        self.assertTrue(eligible(18))
    def test_adult(self):
        self.assertTrue(eligible(19))
