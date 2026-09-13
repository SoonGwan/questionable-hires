import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('report_cases', ROOT / 'benchmarks/con_artist_report_cases.py')
FIXTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXTURE)


class ConArtistReportFixtureTests(unittest.TestCase):
    def test_generated_report_preserves_survivors_setup_failure_and_references(self):
        case = FIXTURE.cases()[0]
        self.assertEqual(case['id'], 'con-artist-report-reference-v2')
        result = json.loads(case['files']['audit-result.json'])
        self.assertEqual(result['status'], 'incomplete')
        first, third, invalid = result['audits']
        self.assertEqual(first['checks']['correct_tests']['exit_code'], 0)
        for audit in (first, third):
            self.assertEqual(audit['checks']['mutant_tests']['exit_code'], 0)
            self.assertEqual(audit['checks']['correct_probe']['exit_code'], 0)
            self.assertEqual(audit['checks']['mutant_probe']['exit_code'], 1)
            self.assertIn('AssertionError', audit['checks']['mutant_probe']['output'])
        self.assertEqual(invalid['checks']['mutant_tests']['exit_code'], 7)
        self.assertIn('SyntaxError', invalid['checks']['mutant_tests']['output'])
        self.assertNotIn('probe_skipped', invalid)
        self.assertNotIn('correct_probe', invalid['checks'])
        for audit in (invalid, third):
            self.assertTrue(audit['correct_tests_reused'])
            self.assertEqual(audit['checks']['correct_tests']['observation_ref'], '#/audits/0/checks/correct_tests')
            self.assertNotIn('output', audit['checks']['correct_tests'])
