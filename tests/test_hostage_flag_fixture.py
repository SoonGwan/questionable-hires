import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('flag_fixture', ROOT / 'benchmarks/hostage_flag_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class FlagFixtureTests(unittest.TestCase):
    def test_frozen_inputs_match_and_do_not_include_author_oracle(self):
        frozen = json.loads((ROOT / 'benchmarks/hostage-flag-cases.json').read_text())
        self.assertEqual(frozen, fixture.cases())
        self.assertEqual(frozen[0]['task'], frozen[1]['task'])
        for case in frozen:
            self.assertEqual(set(case['files']), {'flags.py', 'worker.py', 'test_flags.py',
                             'requirements.md', 'notes.txt', 'verification/owner.txt'})

    def test_actual_native_positive_and_relevant_failure(self):
        correct, broken = fixture.preflight()
        self.assertEqual((correct['exit_code'], broken['exit_code']), (0, 1))
        self.assertIn('Ran 5 tests', correct['output'])
        self.assertIn('AssertionError: True is not False', broken['output'])
        self.assertIn('ValueError not raised', broken['output'])
        self.assertNotIn('ERROR:', broken['output'])
