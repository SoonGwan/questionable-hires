import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('guarded_audit', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


@unittest.skipUnless(os.name == 'posix', 'POSIX audit helper')
class AuditProjectGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'service.py').write_text('def value():\n    return 1\n')
        (self.root / 'test_service.py').write_text('import unittest\nimport service\nclass Test(unittest.TestCase):\n    def test_value(self):\n        self.assertGreater(service.value(), 0)\n')
        (self.root / 'notes.txt').write_text('owner notes')
        self.recipe = dict(files=['service.py', 'test_service.py'], imports=['service'],
            tests=['-v', 'test_service'], target='service.py', old='return 1', new='return 2',
            probe='import service\nassert service.value() == 1, service.value()\n', guard_project=True)

    def test_native_checks_preserve_real_git_notes_modes_and_cleanup(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        (self.root / 'notes.txt').chmod(0o600)
        before = helper.project_inventory(self.root)
        result = helper.audit(self.root, self.recipe, python=sys.executable, timeout=5)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual({k: v['exit_code'] for k, v in result['checks'].items()},
                         dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1))
        self.assertIn('AssertionError: 2', result['checks']['mutant_probe']['output'])
        self.assertIn('Ran 1 test', result['checks']['correct_tests']['output'])
        self.assertEqual(helper.project_inventory(self.root), before)
        self.assertTrue(result['integrity']['project_guard']['unchanged'])
        self.assertEqual(result['integrity']['project_guard']['entries'], len(before[0]))
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_unselected_edits_additions_deletions_modes_and_git_are_detected_not_restored(self):
        actions = ('edit', 'add', 'delete', 'mode', 'git')
        for action in actions:
            with self.subTest(action=action):
                notes = self.root / 'notes.txt'
                notes.write_text('owner notes')
                notes.chmod(0o600)
                metadata = self.root / '.git'
                metadata.mkdir(exist_ok=True)
                (metadata / 'HEAD').write_text('original')
                calls = []
                def execute(*args):
                    if not calls:
                        if action == 'edit': notes.write_text('changed')
                        elif action == 'add': (self.root / 'new.txt').write_text('new')
                        elif action == 'delete': notes.unlink()
                        elif action == 'mode': notes.chmod(0o644)
                        else: (metadata / 'HEAD').write_text('changed')
                    calls.append(1)
                    return dict(exit_code=0, timed_out=False, output='', output_truncated=False)
                with patch.object(helper, 'execute', side_effect=execute):
                    with self.assertRaisesRegex(RuntimeError, 'Project tree changed.*not restored'):
                        helper.audit(self.root, self.recipe)
                self.assertFalse(list(self.root.glob('.con-artist-*')))
                if action == 'edit': self.assertEqual(notes.read_text(), 'changed')
                elif action == 'add': self.assertEqual((self.root / 'new.txt').read_text(), 'new')
                elif action == 'delete': self.assertFalse(notes.exists())
                elif action == 'mode': self.assertEqual(notes.stat().st_mode & 0o777, 0o644)
                else: self.assertEqual((metadata / 'HEAD').read_text(), 'changed')

    def test_opt_out_does_not_inventory_unselected_tree(self):
        self.recipe['guard_project'] = False
        with patch.object(helper, 'project_inventory', side_effect=AssertionError('unexpected full read')):
            result = helper.audit(self.root, self.recipe, python=sys.executable)
        self.assertNotIn('project_guard', result['integrity'])

    def test_invalid_flag_and_inventory_budgets_refuse_before_execution(self):
        with patch.object(helper, 'execute') as execute:
            for value in (1, 'true', None, []):
                with self.assertRaisesRegex(ValueError, 'boolean'):
                    helper.audit(self.root, dict(self.recipe, guard_project=value))
            with patch.object(helper, 'MAX_GUARD_BYTES', 5), self.assertRaisesRegex(ValueError, '20 MB'):
                helper.audit(self.root, self.recipe)
            with patch.object(helper, 'MAX_GUARD_ENTRIES', 2), self.assertRaisesRegex(ValueError, '10000'):
                helper.audit(self.root, self.recipe)
            execute.assert_not_called()
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_link_target_is_not_read_and_special_file_is_refused(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'target'
            target.write_text('outside')
            (self.root / 'link').symlink_to(target)
            before = helper.project_inventory(self.root)
            target.write_text('changed outside')
            self.assertEqual(helper.project_inventory(self.root), before)
            self.assertEqual(before[0]['link'][0], 'symlink')
        os.mkfifo(self.root / 'fifo')
        with self.assertRaisesRegex(ValueError, 'supports files'):
            helper.project_inventory(self.root)

    def test_file_replaced_by_fifo_is_rejected_without_read(self):
        original_open = helper.os.open
        victim = self.root / 'notes.txt'
        def raced_open(path, flags):
            if path == victim:
                victim.unlink()
                os.mkfifo(victim)
            return original_open(path, flags)
        with patch.object(helper.os, 'open', side_effect=raced_open):
            with self.assertRaisesRegex(ValueError, 'changed while opening'):
                helper.project_inventory(self.root)

    def test_early_incomplete_and_interruption_still_verify_guard(self):
        with patch.object(helper, 'execute', return_value=dict(exit_code=7, timed_out=False, output='', output_truncated=False)):
            result = helper.audit(self.root, self.recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['integrity']['project_guard']['unchanged'])
        with patch.object(helper, 'execute', side_effect=KeyboardInterrupt), self.assertRaises(KeyboardInterrupt):
            helper.audit(self.root, self.recipe)
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_batch_guard_retains_baseline_reuse_and_native_fault_results(self):
        common = {k: v for k, v in self.recipe.items() if k not in ('target', 'old', 'new', 'probe')}
        common['mutations'] = [dict(target='service.py', old='return 1', new='return ' + str(value),
                                    probe=self.recipe['probe']) for value in (2, 3)]
        result = helper.audit_batch(self.root, common, python=sys.executable, timeout=5)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(len(result['audits']), 2)
        self.assertTrue(result['audits'][1]['correct_tests_reused'])
        for audit in result['audits']:
            self.assertTrue(audit['integrity']['project_guard']['unchanged'])
            self.assertEqual(audit['checks']['mutant_probe']['exit_code'], 1)

    def test_real_cli_stdin_reports_guard_and_does_not_hide_mutant_failure(self):
        result = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'skills/con-artist/scripts/audit.py'),
            '--source', str(self.root), '--spec', '-', '--timeout', '5'],
            input=json.dumps(self.recipe), cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertTrue(evidence['integrity']['project_guard']['unchanged'])
        self.assertEqual(evidence['checks']['mutant_probe']['exit_code'], 1)
        self.assertIn('AssertionError: 2', evidence['checks']['mutant_probe']['output'])
        self.assertEqual({p.name for p in self.root.iterdir()}, {'service.py', 'test_service.py', 'notes.txt'})
