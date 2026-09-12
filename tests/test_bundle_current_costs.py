from decimal import Decimal
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BundleCurrentCostsTests(unittest.TestCase):
    def test_all_scheduled_costs_reconcile_without_double_counting_cache(self):
        data = json.loads((ROOT / 'benchmarks/results/bundle-current-02-costs.json').read_text(),
                          parse_float=Decimal)
        cases_file = ROOT / 'benchmarks/fast-cases.json'
        self.assertEqual(data['cases_sha256'], hashlib.sha256(cases_file.read_bytes()).hexdigest())
        cases = {c['id'] for c in json.loads(cases_file.read_text())}
        expected = {(case, arm, 1) for case in cases for arm in ('baseline', 'skill')}
        self.assertEqual(len(data['rows']), len(expected))
        self.assertEqual({(r['case'], r['arm'], r['repeat']) for r in data['rows']}, expected)
        totals = {arm: [0, Decimal(0)] for arm in ('baseline', 'skill')}
        for row in data['rows']:
            self.assertTrue(row['completed'])
            self.assertFalse(row['timed_out'])
            self.assertEqual(row['exit_code'], 0)
            self.assertEqual(row['terminal_event']['type'], 'turn.completed')
            self.assertEqual(row['usage'], row['terminal_event']['usage'])
            usage = row['usage']
            for key in ('input_tokens', 'output_tokens', 'cached_input_tokens'):
                self.assertIs(type(usage[key]), int)
                self.assertGreaterEqual(usage[key], 0)
            self.assertLessEqual(usage['cached_input_tokens'], usage['input_tokens'])
            self.assertGreater(row['elapsed_seconds'], 0)
            totals[row['arm']][0] += usage['input_tokens'] + usage['output_tokens']
            totals[row['arm']][1] += row['elapsed_seconds']
        self.assertEqual(totals, {'baseline': [605780, Decimal('318.492')],
                                  'skill': [668334, Decimal('392.015')]})
        # Numerical consistency is not proof of task success or capture completeness.
