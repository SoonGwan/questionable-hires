import unittest

from eligibility import eligible


class EligibilityBoundaryTest(unittest.TestCase):
    def test_age_boundary(self):
        for age, expected in ((17, False), (18, True), (19, True)):
            with self.subTest(age=age):
                self.assertIs(eligible(age), expected)


if __name__ == "__main__":
    unittest.main()
