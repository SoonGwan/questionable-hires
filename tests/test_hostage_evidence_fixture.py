import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('handoff_fixture', ROOT / 'benchmarks/hostage_evidence_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class HandoffEvidenceFixtureTests(unittest.TestCase):
    def test_frozen_handoff_fingerprints_distinguish_three_states(self):
        cases = json.loads((ROOT / 'benchmarks/hostage-evidence-cases.json').read_text())
        self.assertEqual([c['id'] for c in cases], ['evidence-matching', 'evidence-stale', 'evidence-absent'])
        for case in cases:
            current = dict(case['files'], **case.get('working_files', {}))
            if case['id'] == 'evidence-absent':
                self.assertNotIn('verification/prior.json', current)
                continue
            report = json.loads(current['verification/prior.json'])
            self.assertEqual(report['command'], fixture.COMMAND)
            self.assertEqual(report['test_count'], 6)
            self.assertEqual(report['exit_code'], 0)
            self.assertIn('Ran 6 tests', report['output'])
            mismatch = [p for p, digest in report['inputs_sha256'].items()
                        if hashlib.sha256(current[p].encode()).hexdigest() != digest]
            self.assertEqual(mismatch, ['form.py'] if case['id'] == 'evidence-stale' else [])

    def test_native_preflight_preserves_actual_six_test_failure_path(self):
        _, observations = fixture.prepared()
        self.assertEqual([o['exit_code'] for o in observations], [0, 1])
        self.assertIn('FAILED (failures=6)', observations[1]['output'])
        self.assertIn('AssertionError: True is not False', observations[1]['output'])
