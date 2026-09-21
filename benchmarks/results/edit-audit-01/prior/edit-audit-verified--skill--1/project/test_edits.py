import unittest
from text_edits import apply_edits

class EditTests(unittest.TestCase):
    def test_multiple_edits(self):
        edits = [(5, 7, "XY"), (1, 3, "Q")]
        result = apply_edits("αβγδεζηθ", edits)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 7)

    def test_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlapping edits"):
            apply_edits("abcdef", [(3, 5, "Y"), (1, 4, "X")])

    def test_controls(self):
        self.assertEqual(apply_edits("αβγ", []), "αβγ")
        self.assertEqual(apply_edits("αβγ", [(0, 1, ""), (1, 3, "Z")]), "Z")
        with self.assertRaisesRegex(ValueError, "invalid range"):
            apply_edits("abc", [(2, 4, "Z")])
