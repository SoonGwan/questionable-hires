import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AuditSelectionObservationTests(unittest.TestCase):
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
