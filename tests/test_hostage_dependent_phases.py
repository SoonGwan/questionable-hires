import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('phase_probe', ROOT / 'benchmarks/probe_hostage_dependent_phases.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class DependentPhaseControls(unittest.TestCase):
    def test_real_retained_assertions_detect_faults_without_secondary_unbound_errors(self):
        # Archives also include these tracked raw artifacts; no Git history needed.
        with tempfile.TemporaryDirectory(prefix='phase-regression-', dir=ROOT) as scratch:
            with mock.patch.object(probe, 'frozen', side_effect=lambda name: (ROOT / name).read_bytes()):
                report = probe.probe(Path(scratch))
        self.assertEqual(len(report['checks']), 12)
        for check in report['checks']:
            self.assertTrue(check['matched'], check['output'])
            if check['variant'] in ('final', 'valid_duplicate_false'):
                self.assertIn('\nOK\n', check['output'])
            elif check['mode'] == 'dependent_phases_unwind':
                self.assertNotIn('UnboundLocalError', check['output'])
                if check['variant'] == 'missing_guard':
                    self.assertIn('AssertionError: duplicate invoked a callback', check['output'])
                if check['variant'] == 'missing_cleanup':
                    self.assertIn('AssertionError: Items in the first set but not the second:', check['output'])
                if check['variant'] == 'blocks_other_keys':
                    self.assertIn('Application task completed before expected callback entry', check['output'])

    def test_independent_scenario_subtests_are_preserved(self):
        source = (ROOT / probe.PROJECT / 'test_importer.py').read_text()
        corrected = probe.adapt(source)
        def with_counts(text):
            return {node.name: sum(isinstance(n, ast.With) for n in ast.walk(node))
                    for node in ast.walk(ast.parse(text)) if isinstance(node, ast.AsyncFunctionDef)}
        before, after = with_counts(source), with_counts(corrected)
        for name in before:
            self.assertEqual(after[name], before[name] - int(name in probe.TARGETS))
