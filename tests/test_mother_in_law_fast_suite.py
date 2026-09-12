import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'validate_mother_in_law_fast_suite',
    ROOT / 'benchmarks/validate_mother_in_law_fast_suite.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class MotherInLawFastSuiteTests(unittest.TestCase):
    def test_repository_suite_resolves_and_stays_small(self):
        suite = validator.validate()
        self.assertLessEqual(len(suite['cases']), 6)
        self.assertEqual({case['runner'] for case in suite['cases']},
                         {'generic', 'browser-container'})
        self.assertIn('clean', {case['expected'] for case in suite['cases']})

    def test_rejects_duplicate_or_unresolved_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'cases.json').write_text(json.dumps([
                {'id': 'one', 'skill': 'mother-in-law'},
            ]))
            for cases in (
                [dict(id='one', runner='generic', source='cases.json', expected='clean')] * 2,
                [dict(id='missing', runner='generic', source='cases.json', expected='clean')],
            ):
                suite = root / 'suite.json'
                suite.write_text(json.dumps(dict(
                    skill='mother-in-law', maximum_cases=6, cases=cases)))
                with self.assertRaises(ValueError):
                    validator.validate(root, suite)


if __name__ == '__main__':
    unittest.main()
