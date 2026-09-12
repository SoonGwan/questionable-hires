import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name == 'posix', 'Exported runner requires POSIX')
class NestedInteractionReplayTests(unittest.TestCase):
    def test_exported_projects_reproduce_without_private_logs_or_git(self):
        for arm, failures in [('baseline', 2), ('skill', 1)]:
            with self.subTest(arm=arm), tempfile.TemporaryDirectory() as directory:
                project = Path(directory) / 'project'
                source = ROOT / 'benchmarks/results/interaction-nested-01' / (
                    'nested-search-qa--' + arm + '--1') / 'project'
                shutil.copytree(source, project)
                before = {str(p.relative_to(project)): p.read_bytes()
                          for p in project.rglob('*') if p.is_file()}
                self.assertFalse((project / '.git').exists())
                process = subprocess.run(
                    [sys.executable, '-B', '../../tools/check.py', '--timeout', '3',
                     '--', sys.executable, '-B', '-m', 'unittest', 'discover',
                     '-s', 'qa', '-p', 'test_*.py', '-v'],
                    cwd=project / 'apps/catalog', capture_output=True, text=True,
                    timeout=10)
                self.assertEqual(process.returncode, 1, process.stderr)
                result = json.loads(process.stdout)
                self.assertEqual(result['exit_code'], 1)
                self.assertFalse(result['timed_out'])
                self.assertTrue(result['cleanup_complete'])
                self.assertFalse(result['output_truncated'])
                self.assertIn('FAILED (failures=' + str(failures) + ')', result['output'])
                self.assertIn('AssertionError: Lists differ:', result['output'])
                self.assertIn(' ... ok', result['output'])
                self.assertNotIn('ImportError', result['output'])
                self.assertEqual(before, {str(p.relative_to(project)): p.read_bytes()
                                         for p in project.rglob('*') if p.is_file()})
