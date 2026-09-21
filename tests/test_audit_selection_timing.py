import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('selection_timing', ROOT / 'benchmarks/time_audit_selection_reuse.py')
timing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(timing)


class AuditSelectionTimingTests(unittest.TestCase):
    def test_published_timing_contains_all_native_attempts_and_same_mutant_outcomes(self):
        folder = ROOT / 'benchmarks/results/audit-selection-timing-01'
        manifest = json.loads((folder / 'manifest.json').read_text())
        rows = [json.loads(path.read_text()) for path in sorted(folder.glob('cell-*.json'))]
        self.assertEqual([{k: row[k] for k in ('case', 'repeat', 'arm')} for row in rows], manifest['schedule'])
        self.assertEqual(timing.summarize(rows), json.loads((folder / 'summary.json').read_text()))
        for row in rows:
            observation = row['observation']
            self.assertEqual(observation['helper_sha256'], manifest['helper_sha256'][row['arm']])
            self.assertEqual(set(observation['cases']), {row['case']})
            case = observation['cases'][row['case']]
            original_count = {'adjacent-control': 2, 'revisited-selection': 3, 'alternating-eight': 8}[row['case']]
            self.assertEqual(case['correct_executions'], original_count if row['arm'] == 'before' else 2)
            self.assertEqual(case['mutant_executions'], len(case['selections']))
            self.assertEqual(len(case['executions']), case['correct_executions'] + case['mutant_executions'])
            mutants = [e for e in case['executions'] if e['phase'] == 'mutant-tests']
            self.assertEqual([e['exit_code'] for e in mutants], [int(s == 'stored') for s in case['selections']])
            for event in case['executions']:
                self.assertFalse(event['timed_out'] or event['output_truncated'])
                self.assertIn('Ran 1 test', event['output'])
            self.assertTrue(case['originals_preserved'] and case['owned_scratch_removed'])

    def test_fixed_schedule_and_complete_ratio_accounting(self):
        rows = [dict(c, elapsed_seconds=2 if c['arm'] == 'before' else 1) for c in timing.schedule()]
        self.assertEqual(len(rows), 18)
        summary = timing.summarize(rows)
        self.assertEqual(set(summary), set(timing.CASES))
        self.assertTrue(all(s['after_over_before_mean'] == 0.5 for s in summary.values()))
        for incomplete in (rows[:-1], rows + [rows[0]], rows[1:] + [rows[0], rows[0]]):
            with self.assertRaises(ValueError): timing.summarize(incomplete)
        with self.assertRaises(ValueError):
            timing.summarize([dict(rows[0], elapsed_seconds=float('nan')), *rows[1:]])
