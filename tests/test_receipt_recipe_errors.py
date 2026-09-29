"""CLI recipe errors must identify the input fault before project execution."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/receipt/scripts/compare.py'
RECIPE = dict(fixed=['test_rule.py'], vary=['rule.py'], before='HEAD^', after='HEAD',
              imports=['rule'], runner='unittest', tests=['test_rule'])


class ReceiptRecipeErrorTests(unittest.TestCase):
    def reject(self, raw, *messages, from_file=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / 'untouched.txt'
            marker.write_bytes(b'preserve me')
            recipe_path = root / 'recipe.json'
            if from_file:
                recipe_path.write_text(raw, encoding='utf-8')
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(SCRIPT), '--source', str(root),
                 '--spec', str(recipe_path) if from_file else '-'],
                input='' if from_file else raw, text=True, capture_output=True, timeout=5)
            self.assertEqual(process.returncode, 2, process.stderr)
            self.assertEqual(process.stdout, '')
            for message in messages:
                self.assertIn(message, process.stderr)
            self.assertNotIn('fatal:', process.stderr)
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)
            return process.stderr

    def test_unknown_option_identified(self):
        self.reject(json.dumps(dict(RECIPE, guard_trees=True)),
                    'unknown keys: ["guard_trees"]')

    def test_missing_option_identified(self):
        recipe = dict(RECIPE)
        del recipe['tests']
        self.reject(json.dumps(recipe), 'missing keys: ["tests"]')

    def test_missing_and_unknown_reported_together(self):
        recipe = dict(RECIPE)
        recipe['test'] = recipe.pop('tests')
        self.reject(json.dumps(recipe), 'missing keys: ["tests"]',
                    'unknown keys: ["test"]')

    def test_non_object_has_specific_diagnostic(self):
        self.reject('[]', 'Recipe must be a JSON object')

    def test_duplicate_top_level_rejected_from_stdin_and_file(self):
        raw = json.dumps(RECIPE)[:-1] + ', "tests": ["different_test"]}'
        for from_file in (False, True):
            with self.subTest(from_file=from_file):
                self.reject(raw, 'Duplicate recipe key: "tests"', from_file=from_file)

    def test_nested_and_escaped_duplicates_rejected(self):
        for raw, key in (
            (json.dumps(RECIPE).replace('"after": "HEAD"',
             '"after": {"working_tree": false, "working_tree": true}'), 'working_tree'),
            (json.dumps(RECIPE)[:-1] + ', "runn\\u0065r": "pytest"}', 'runner'),
        ):
            with self.subTest(key=key):
                self.reject(raw, 'Duplicate recipe key: ' + json.dumps(key))

    def test_diagnostic_escapes_and_bounds_unknown_names(self):
        stderr = self.reject(json.dumps(dict(RECIPE, **{'\n' + 'x' * 5000: True})),
                             'unknown keys: ["\\n')
        self.assertLess(len(stderr), 400)
        self.assertEqual(stderr.count('\n'), 1)


if __name__ == '__main__':
    unittest.main()
