from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'benchmarks'))
import eventemitter_boundary_cases as cases


class EventEmitterBoundaryControls(unittest.TestCase):
    def test_native_assertions_reject_upstream_and_partial_fix(self):
        rows = cases.preflight()
        self.assertEqual([(r['task'], r['variant'], r['exit_code']) for r in rows], [
            ('once-reentrant-dispatch', 'upstream', 1),
            ('once-reentrant-dispatch', 'corrected', 0),
            ('once-reentrant-dispatch', 'partial-multi-path-only', 1),
            ('empty-event-removal', 'upstream', 1),
            ('empty-event-removal', 'corrected', 0)])
        for row in rows:
            self.assertEqual(row['stderr'], '')
            self.assertNotIn('SyntaxError', row['output'])
            if row['exit_code']: self.assertIn('AssertionError', row['output'])

    def test_source_and_license_identities(self):
        self.assertEqual(set(cases.files()), {'index.js', 'LICENSE', 'AGENTS.md', 'existing.test.cjs'})
