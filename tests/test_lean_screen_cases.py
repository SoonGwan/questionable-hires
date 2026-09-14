import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import lean_screen_cases as screen
from lean_entries import BODIES


class LeanScreenCasesTests(unittest.TestCase):
    def test_exact_eight_roles_and_preserved_selected_inputs(self):
        cases = screen.cases()
        self.assertEqual(len(cases), 8)
        self.assertEqual({c['skill'] for c in cases}, set(BODIES))
        for case, (filename, identity, _) in zip(cases, screen.SELECTION):
            frozen = json.loads((ROOT/'benchmarks'/filename).read_text())
            self.assertEqual(case, next(c for c in frozen if c['id'] == identity))
        self.assertEqual(cases[-1]['files'], screen.FRIDAY['files'])
        self.assertEqual(cases[-1]['task'], screen.FRIDAY['task'].replace(' using $friday', ''))
        self.assertIn(' using $friday', screen.FRIDAY['task'])
        self.assertTrue(all('$' not in c['task'] for c in cases))

    def test_independent_builds_and_input_hashes(self):
        first = screen.cases()
        first[-1]['files']['release.md'] = 'changed locally'
        self.assertNotEqual(first[-1]['files'], screen.cases()[-1]['files'])
        hashes = screen.source_hashes()
        self.assertEqual(len(hashes), 9)
        self.assertEqual(hashes, screen.source_hashes())
        self.assertTrue(all(len(value) == 64 for value in hashes.values()))


if __name__ == '__main__':
    unittest.main()
