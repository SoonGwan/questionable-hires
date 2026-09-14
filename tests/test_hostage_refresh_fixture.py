import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('refresh_fixture', ROOT / 'benchmarks/hostage_refresh_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class RefreshFixtureTests(unittest.TestCase):
    def test_frozen_cases_preserve_concurrency_contract_without_author_oracle(self):
        frozen = json.loads((ROOT / 'benchmarks/hostage-refresh-cases.json').read_text())
        self.assertEqual(frozen, fixture.cases())
        self.assertEqual(frozen[0]['task'], frozen[1]['task'])
        for case in frozen:
            self.assertEqual(set(case['files']), {'preview.py', 'requirements.md', 'notes.txt'})
        self.assertNotEqual(frozen[0]['files']['preview.py'], frozen[1]['files']['preview.py'])

    def test_native_positive_and_actual_owned_state_failure(self):
        correct, broken = fixture.preflight()
        self.assertEqual((correct['exit_code'], broken['exit_code']), (0, 1))
        self.assertIn('Ran 6 tests', correct['output'])
        self.assertIn('FAILED (failures=3)', broken['output'])
        self.assertIn('AssertionError: False is not True', broken['output'])
        self.assertNotIn('ERROR:', broken['output'])
