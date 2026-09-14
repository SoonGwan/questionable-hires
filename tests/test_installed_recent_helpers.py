"""Keep recent installed-helper executions in the ordinary offline test suite."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('skills_install_check', ROOT / 'benchmarks/check_skills_cli_install.py')
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class InstalledRecentHelperTests(unittest.TestCase):
    def test_installed_regions_and_native_receipt_execute_without_checkout_imports(self):
        with tempfile.TemporaryDirectory(prefix='installed-recent-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary)
            installed = project / '.agents/skills'
            result = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'scripts/install.py'),
                                     '--dest', str(installed)], cwd=project,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            before = checker.inventory(installed)
            executions = []
            def run(args, input=None, expected_exit=0):
                result = subprocess.run(args, cwd=project, input=input, capture_output=True,
                                        text=True, timeout=30)
                self.assertEqual(result.returncode, expected_exit, result.stdout + result.stderr)
                executions.append((args, result.returncode))
                return result.stdout
            report = checker.exercise_recent_helpers(installed, project, run)
            self.assertTrue(report['named_regions_complete'])
            self.assertEqual(report['missing_region_exit'], 1)
            self.assertEqual((report['receipt_native_before_exit'], report['receipt_native_after_exit']), (1, 0))
            self.assertTrue(report['receipt_original_tree_unchanged'])
            self.assertEqual(checker.inventory(installed), before)
            self.assertFalse(list(project.glob('receipt-native-*')))
            self.assertEqual(sum('python_regions.py' in ' '.join(args) for args, _ in executions), 2)
