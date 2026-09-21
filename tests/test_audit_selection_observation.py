import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AuditSelectionObservationTests(unittest.TestCase):
    def test_after_observations_reduce_only_revisited_normal_executions(self):
        before = json.loads((ROOT / 'benchmarks/results/audit-selection-reuse-01.json').read_text())
        for version in ('02', '03'):
            after = json.loads((ROOT / ('benchmarks/results/audit-selection-reuse-' + version + '.json')).read_text())
            self.assertEqual(after['source'], before['source'])
            self.assertEqual(after['tests'], before['tests'])
            self.assertNotEqual(after['helper_sha256'], before['helper_sha256'])
            for name, case in after['cases'].items():
                self.assertEqual(case['selections'], before['cases'][name]['selections'])
                self.assertEqual(case['correct_executions'], 2)
                self.assertEqual(case['mutant_executions'], before['cases'][name]['mutant_executions'])
                calls = case['executions']
                self.assertEqual(len(calls), 2 + case['mutant_executions'])
                mutants = [c for c in calls if c['phase'] == 'mutant-tests']
                self.assertEqual([c['exit_code'] for c in mutants], [int(s == 'stored') for s in case['selections']])
                self.assertTrue(all(not c['timed_out'] and not c['output_truncated'] and 'Ran 1 test' in c['output'] for c in calls))
                self.assertTrue(case['originals_preserved'] and case['owned_scratch_removed'])

    def test_all_native_cases_preserve_execution_and_detection_evidence(self):
        report = json.loads((ROOT / 'benchmarks/results/audit-selection-reuse-01.json').read_text())
        expected = {'adjacent-control': (2, 3), 'revisited-selection': (3, 3),
                    'alternating-eight': (8, 8)}
        self.assertEqual(set(report['cases']), set(expected))
        for name, (correct, mutant) in expected.items():
            case = report['cases'][name]
            with self.subTest(name=name):
                self.assertEqual(case['correct_executions'], correct)
                self.assertEqual(case['mutant_executions'], mutant)
                self.assertEqual(len(case['executions']), correct + mutant)
                self.assertTrue(case['originals_preserved'])
                self.assertTrue(case['owned_scratch_removed'])
                mutants = [c for c in case['executions'] if c['phase'] == 'mutant-tests']
                self.assertEqual([c['exit_code'] for c in mutants], [int(s == 'stored') for s in case['selections']])
                for call in case['executions']:
                    self.assertFalse(call['timed_out'])
                    self.assertFalse(call['output_truncated'])
                    self.assertIn('Ran 1 test', call['output'])
                    if call['phase'] == 'correct-tests':
                        self.assertEqual(call['exit_code'], 0)
