import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run
from receipt_selection_cases import cases

spec = importlib.util.spec_from_file_location('selection_receipt', ROOT/'skills/receipt/scripts/compare.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ReceiptSelectionCasesTests(unittest.TestCase):
    def check_observations(self, observations):
        before, after = observations['before'], observations['after']
        self.assertEqual(before['exit_code'], 1, before['output'])
        self.assertIn('Ran 5 tests', before['output'])
        self.assertIn('FAILED (failures=2)', before['output'])
        self.assertIn("{'a': 5, 'b': 4} != {'a': 3, 'b': 4}", before['output'])
        self.assertIn('ValueError not raised', before['output'])
        self.assertEqual(after['exit_code'], 0, after['output'])
        self.assertIn('Ran 5 tests', after['output'])
        self.assertIn('OK', after['output'])

    def test_native_and_helper_reject_real_defects_and_pass_same_fixed_tests(self):
        for case in cases():
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
                project = Path(scratch)/'project'
                run.prepare(case, project)
                status = run.command(['git', 'status', '--porcelain'], project)
                original = run.resource_manifest(project)
                if case['id'].endswith('present'):
                    process = subprocess.run([sys.executable, '-B', 'tools/compare_allocation.py', 'HEAD^', 'HEAD'],
                        cwd=project, capture_output=True, text=True, timeout=20)
                    self.assertEqual(process.returncode, 0, process.stderr)
                    native = json.loads(process.stdout)
                    self.check_observations(native['checks'])
                    self.assertTrue(native['originals_unchanged'])
                    self.assertTrue(native['comparison_copies_removed'])
                    for check in native['checks'].values():
                        self.assertIn(str(project), check['output'])
                        self.assertIn('NATIVE COPIED IMPORT:', check['output'])
                recipe = dict(fixed=['test_allocation.py'], vary=['allocation.py'],
                    before='HEAD^', after='HEAD', imports=['allocation'],
                    runner='unittest', tests=['-v', 'test_allocation'], guard_tree=True)
                observed = helper.compare(project, recipe, python=sys.executable)
                self.check_observations(observed['checks'])
                self.assertTrue(observed['comparison_copies_removed'])
                self.assertTrue(observed['tree_guard']['unchanged'])
                self.assertTrue(observed['originals']['unchanged'])
                for check in observed['checks'].values():
                    self.assertIn('Verified copied import: allocation', check['output'])
                    self.assertFalse(check['timed_out'])
                    self.assertFalse(check['output_truncated'])
                self.assertEqual(original, run.resource_manifest(project))
                self.assertEqual(status, run.command(['git', 'status', '--porcelain'], project))

    def test_matched_pair_varies_support_not_implementation_or_assertions(self):
        present, absent = cases()
        for index in (0, 1):
            for name in ('allocation.py', 'test_allocation.py'):
                self.assertEqual(present['history'][index]['files'].get(name), absent['history'][index]['files'].get(name))
        self.assertEqual(present['task'], absent['task'])
        self.assertNotIn('tools/compare_allocation.py', absent['history'][0]['files'])
