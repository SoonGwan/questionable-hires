import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ConArtistExampleTests(unittest.TestCase):
    def test_selection_recipe_runs_distinct_baselines_and_real_detection(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            project = Path(directory) / 'example'
            shutil.copytree(ROOT / 'examples/con-artist-batch', project)
            before = {p.name: p.read_bytes() for p in project.iterdir()}
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(ROOT / 'skills/con-artist/scripts/audit.py'),
                 '--source', str(project), '--spec', str(project / 'selection-recipe.json')],
                cwd=directory, text=True, capture_output=True, timeout=15)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['status'], 'observed')
            self.assertEqual(len(result['audits']), 2)
            for audit, mutant_exit in zip(result['audits'], (0, 1)):
                self.assertFalse(audit.get('correct_tests_reused', False))
                self.assertEqual(set(audit['checks']), {'correct_tests', 'mutant_tests'})
                self.assertEqual(audit['checks']['correct_tests']['exit_code'], 0)
                self.assertEqual(audit['checks']['mutant_tests']['exit_code'], mutant_exit)
                for check in audit['checks'].values():
                    self.assertIn('Ran 1 test', check['output'])
                    self.assertFalse(check['timed_out'])
                    self.assertFalse(check['output_truncated'])
                self.assertTrue(audit['integrity']['owned_scratch_removed'])
            failure = result['audits'][1]['checks']['mutant_tests']['output']
            self.assertIn("AssertionError: Lists differ: ['existing'] != ['existing', 'new']", failure)
            self.assertEqual(before, {p.name: p.read_bytes() for p in project.iterdir()})

    def test_documented_recipe_preserves_sources_and_exposes_both_faults(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'example'
            shutil.copytree(ROOT / 'examples/con-artist-batch', project)
            before = {p.name: p.read_bytes() for p in project.iterdir()}
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(ROOT / 'skills/con-artist/scripts/audit.py'),
                 '--source', str(project), '--spec', str(project / 'recipe.json')],
                cwd=directory, text=True, capture_output=True, timeout=15)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['status'], 'observed')
            self.assertEqual(len(result['audits']), 2)
            for audit, values in zip(result['audits'],
                                     ["['existing']", "['existing', 'new', 'new']"]):
                self.assertEqual({k: v['exit_code'] for k, v in audit['checks'].items()},
                                 dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
                self.assertIn('AssertionError: ' + values, audit['checks']['mutant_probe']['output'])
                for check in audit['checks'].values():
                    self.assertFalse(check['timed_out'])
                    if 'output' in check:
                        self.assertFalse(check['output_truncated'])
                        self.assertIn('Verified copied import: service', check['output'])
            for name in ('correct_tests', 'correct_probe'):
                second = result['audits'][1]
                self.assertTrue(second[name + '_reused'])
                self.assertEqual(second['checks'][name]['observation_ref'],
                                 '#/audits/0/checks/' + name)
                self.assertNotIn('output', second['checks'][name])
            self.assertEqual(before, {p.name: p.read_bytes() for p in project.iterdir()})
