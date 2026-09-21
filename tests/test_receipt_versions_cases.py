import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases

spec = importlib.util.spec_from_file_location('versions_receipt', ROOT/'skills/receipt/scripts/compare.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ReceiptVersionsCasesTests(unittest.TestCase):
    def test_fresh_import_native_failures_controls_and_preservation(self):
        for case in cases(sys.executable):
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
                project = Path(scratch)/'project'
                run.prepare(case, project)
                original = helper.tree_inventory(project)
                fresh = subprocess.run([sys.executable, '-B', '-c',
                    'import windows, pathlib; '
                    'assert pathlib.Path(windows.__file__).resolve() == pathlib.Path("windows.py").resolve(); '
                    'assert windows.merge_windows([(1, 10), (2, 3)]) == [(1, 10)]'],
                    cwd=project, capture_output=True, text=True, timeout=15)
                self.assertEqual(fresh.returncode, 0, fresh.stderr)
                multiple = case['id'].endswith('multiple')
                recipe = dict(fixed=['test_windows.py'], vary=['windows.py'],
                    before='HEAD~2' if multiple else 'HEAD^', after='HEAD',
                    imports=['windows'], runner='unittest', tests=['-v', 'test_windows'],
                    guard_tree=True, additional_before=['HEAD^'] if multiple else [])
                result = helper.compare(project, recipe, python=sys.executable)
                expected = [('before', 2), ('before_2', 1), ('after', 0)] if multiple else [('before', 1), ('after', 0)]
                self.assertEqual(list(result['checks']), [label for label, _ in expected])
                for label, failures in expected:
                    check = result['checks'][label]
                    self.assertEqual(check['exit_code'], int(bool(failures)), check['output'])
                    self.assertIn('Ran 6 tests', check['output'])
                    self.assertIn(f'FAILED (failures={failures})' if failures else 'OK', check['output'])
                    self.assertIn('Verified copied import: windows', check['output'])
                    self.assertFalse(check['timed_out'])
                    self.assertFalse(check['output_truncated'])
                    self.assertEqual(len(result['revisions'][label]), 40)
                    if failures:
                        self.assertIn('[(1, 3)] != [(1, 10)]', check['output'])
                    if failures == 2:
                        self.assertIn('[(1, 3), (3, 5)] != [(1, 5)]', check['output'])
                self.assertTrue(result['tree_guard']['unchanged'])
                self.assertTrue(result['comparison_copies_removed'])
                self.assertEqual(original, helper.tree_inventory(project))

    def test_control_changes_only_requested_revision_count(self):
        single, multiple = cases(sys.executable)
        self.assertEqual(single['history'], multiple['history'])
        self.assertEqual(single['criteria'], multiple['criteria'])
        self.assertEqual(single['task'].replace('HEAD^ and HEAD', 'HEAD~2, HEAD^ and HEAD'), multiple['task'])
