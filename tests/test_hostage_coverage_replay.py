from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import check_hostage_coverage as replay


class CoverageReplayTests(unittest.TestCase):
    def test_retained_suites_execute_real_controls_and_reveal_key_domain_difference(self):
        result = replay.inspect()
        self.assertEqual(len(result['rows']), 10)
        for row in result['rows']:
            with self.subTest(condition=row['condition'], mutation=row['mutation']):
                self.assertFalse(row['timed_out'])
                passing = row['mutation'] == 'healthy' or (
                    row['condition'] == 'current' and row['mutation'] == 'stringify_callback_key')
                self.assertEqual(row['exit_code'], 0 if passing else 1, row['output'])
                self.assertIn('Ran 5 tests' if row['condition'] == 'baseline' else 'Ran 8 tests', row['output'])
                self.assertIn('\nOK\n' if passing else 'AssertionError:', row['output'])
                self.assertNotIn('ERROR:', row['output'])
