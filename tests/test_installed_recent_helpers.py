"""Keep recent installed-helper executions in the ordinary offline test suite."""
import importlib.util
import json
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
    def test_installed_sequence_probe_preserves_behavior_and_incomplete_diagnostics(self):
        with tempfile.TemporaryDirectory(prefix='installed-sequence-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary)
            installed = project / '.agents/skills'
            setup = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'scripts/install.py'),
                '--dest', str(installed), '--skill', 'mother-in-law'], cwd=project,
                capture_output=True, text=True, timeout=15)
            self.assertEqual(setup.returncode, 0, setup.stderr)
            inventory = checker.inventory(installed)
            source = project / 'component.py'
            source.write_text('''class Guarded:
    def __init__(self):
        self.result, self.generation = None, 0
    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        value = await fetch(query)
        if generation == self.generation:
            self.result = value
class Unguarded:
    result = None
    async def run(self, query, fetch):
        self.result = await fetch(query)
class BrokenSetup:
    async def run(self, query, fetch):
        raise RuntimeError('request setup failed')
''')
            source.chmod(0o600)
            before = source.read_bytes(), source.stat().st_mode & 0o777
            for name, expected in (('Guarded', 0), ('Unguarded', 1), ('BrokenSetup', 2)):
                with self.subTest(component=name):
                    process = subprocess.run([sys.executable, '-I', '-B',
                        str(installed / 'mother-in-law/scripts/sequence_probe.py'),
                        '--root', str(project), '--source', 'component.py', '--class-name', name],
                        cwd=project, capture_output=True, text=True, timeout=2)
                    self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
                    self.assertEqual(process.stderr, '')
                    evidence = json.loads(process.stdout)
                    self.assertEqual(evidence['complete'], expected != 2)
                    if expected == 2:
                        self.assertIn('RuntimeError: request setup failed', evidence['error'])
                    else:
                        self.assertEqual([c['passed'] for c in evidence['cases']],
                                         [True, expected == 0])
            self.assertEqual((source.read_bytes(), source.stat().st_mode & 0o777), before)
            self.assertEqual(checker.inventory(installed), inventory)
            self.assertEqual({p.name for p in project.iterdir()}, {'.agents', 'component.py'})

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
