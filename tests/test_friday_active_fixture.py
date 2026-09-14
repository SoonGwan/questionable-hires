import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('friday_active_fixture', ROOT / 'benchmarks/friday_active_cases.py')
fixture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixture)


class ActiveReleaseFixtureTests(unittest.TestCase):
    def test_frozen_cases_match_and_oracle_is_not_model_input(self):
        cases = fixture.cases()
        self.assertEqual(cases, json.loads((ROOT / 'benchmarks/friday-active-cases.json').read_text()))
        self.assertEqual(len(cases), 2)
        for case in cases:
            self.assertNotIn('test_release.py', case['files'])
        first, second = cases
        self.assertEqual({k: v for k, v in first['files'].items() if k != 'release.json'},
                         {k: v for k, v in second['files'].items() if k != 'release.json'})

    def test_native_pass_and_active_reader_failure_preserve_inputs(self):
        results = fixture.preflight()
        self.assertEqual([r['exit_code'] for r in results], [0, 1])
        self.assertIn('active reader incompatible: no such column: name', results[1]['output'])
