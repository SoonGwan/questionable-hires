"""Actual native observations must survive a failed final integrity check."""
import json
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_audit_project_guard as guard_tests

helper = guard_tests.helper


class AuditGuardEvidenceTests(unittest.TestCase):
    setUp = guard_tests.AuditProjectGuardTests.setUp

    def inject(self, body):
        path = self.root / 'test_service.py'
        path.write_text(path.read_text() + '\nfrom pathlib import Path\n'
                        + 'def setUpModule():\n'
                        + '    original = Path(__file__).resolve().parents[2]\n'
                        + '\n'.join('    ' + line for line in body.splitlines()) + '\n')

    def cli(self, recipe=None, timeout=5):
        process = subprocess.run([sys.executable, '-B', helper.__file__, '--source',
            str(self.root), '--spec', '-', '--timeout', str(timeout)],
            input=json.dumps(recipe or self.recipe), text=True, capture_output=True)
        self.assertEqual(process.returncode, 2, process.stderr)
        self.assertIn('Audit not established:', process.stderr)
        self.assertTrue(process.stdout.strip(), 'Completed checks were discarded')
        return json.loads(process.stdout)

    def checks(self, result, value=2):
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual({key: check['exit_code'] for key, check in result['checks'].items()},
                         dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        self.assertIn('AssertionError: ' + str(value), result['checks']['mutant_probe']['output'])
        self.assertIn('Ran 1 test', result['checks']['mutant_tests']['output'])
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def batch(self):
        common = {key: self.recipe[key] for key in ('files', 'imports', 'tests', 'guard_project')}
        common['mutations'] = [dict(target='service.py', old='return 1', new='return ' + str(n),
                                    probe=self.recipe['probe']) for n in (2, 3, 4)]
        return common

    def test_cli_selected_change_retains_native_checks_without_restoration(self):
        self.inject("path = original / 'service.py'\npath.write_text(path.read_text() + '# changed\\n')")
        result = self.cli()
        self.checks(result)
        self.assertFalse(result['integrity']['selected_original_bytes_and_modes_unchanged'])
        self.assertIsNone(result['integrity']['project_guard']['unchanged'])
        self.assertIn('# changed', (self.root / 'service.py').read_text())

    def test_cli_project_change_retains_native_checks(self):
        self.inject("(original / 'notes.txt').write_text('changed')")
        result = self.cli()
        self.checks(result)
        self.assertTrue(result['integrity']['selected_original_bytes_and_modes_unchanged'])
        self.assertFalse(result['integrity']['project_guard']['unchanged'])
        self.assertEqual((self.root / 'notes.txt').read_text(), 'changed')

    def test_timeout_then_guard_retains_only_executed_phase(self):
        self.inject("(original / 'notes.txt').write_text('changed')\nimport time\ntime.sleep(2)")
        result = self.cli(timeout=0.3)
        self.assertEqual(list(result['checks']), ['correct_tests'])
        self.assertTrue(result['checks']['correct_tests']['timed_out'])
        self.assertNotEqual(result['checks']['correct_tests']['exit_code'], 0)
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        self.assertFalse(result['integrity']['project_guard']['unchanged'])

    def test_api_preserves_runtime_error_type_and_attaches_checks(self):
        self.inject("(original / 'notes.txt').write_text('changed')")
        with self.assertRaises(RuntimeError) as caught:
            helper.audit(self.root, self.recipe, timeout=5)
        self.assertIs(type(caught.exception), RuntimeError)
        result = getattr(caught.exception, 'audit_result', None)
        self.assertIsNotNone(result, 'Completed checks were discarded')
        self.checks(result)

    def test_batch_retains_prior_checks_and_references_stops_later_mutations(self):
        self.inject("if service.value() == 3:\n    (original / 'notes.txt').write_text('changed')\n"
                    "if service.value() == 4:\n    (original / 'must-not-run').write_text('ran')")
        result = self.cli(self.batch())
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 2)
        self.assertEqual(result['audits'][0]['status'], 'observed')
        second = result['audits'][1]
        self.checks(second, 3)
        for key in ('correct_tests', 'correct_probe'):
            self.assertEqual(second['checks'][key]['observation_ref'], '#/audits/0/checks/' + key)
            self.assertNotIn('output', second['checks'][key])
        self.assertEqual(result['unrun_mutations'], 1)
        self.assertFalse((self.root / 'must-not-run').exists())

    def test_inventory_error_remains_oserror_with_unknown_guard(self):
        real = helper.project_inventory
        calls = []
        def inventory(root):
            calls.append(root)
            if len(calls) == 2:
                raise OSError('controlled inventory read failure')
            return real(root)
        with patch.object(helper, 'project_inventory', side_effect=inventory):
            with self.assertRaises(OSError) as caught:
                helper.audit(self.root, self.recipe, timeout=5)
        self.assertIs(type(caught.exception), OSError)
        result = getattr(caught.exception, 'audit_result', None)
        self.assertIsNotNone(result, 'Completed checks were discarded')
        self.checks(result)
        self.assertIsNone(result['integrity']['project_guard']['unchanged'])

    def test_batch_runtime_error_still_raises_with_prior_observations(self):
        self.inject("if service.value() == 3:\n    (original / 'notes.txt').write_text('changed')")
        with self.assertRaises(RuntimeError) as caught:
            helper.audit_batch(self.root, self.batch(), timeout=5)
        self.assertIs(type(caught.exception), RuntimeError)
        result = caught.exception.audit_result
        self.assertEqual(len(result['audits']), 2)
        self.checks(result['audits'][1], 3)
        self.assertEqual(result['unrun_mutations'], 1)

    def test_first_batch_inventory_error_still_raises(self):
        real = helper.project_inventory
        calls = []
        def inventory(root):
            calls.append(root)
            if len(calls) == 2:
                raise OSError('controlled first audit inventory failure')
            return real(root)
        with patch.object(helper, 'project_inventory', side_effect=inventory):
            with self.assertRaises(OSError) as caught:
                helper.audit_batch(self.root, self.batch(), timeout=5)
        result = caught.exception.audit_result
        self.assertEqual(len(result['audits']), 1)
        self.checks(result['audits'][0])
        self.assertEqual(result['unrun_mutations'], 2)

    def test_batch_inventory_error_keeps_existing_return_semantics(self):
        real = helper.project_inventory
        calls = []
        def inventory(root):
            calls.append(root)
            if len(calls) == 4:
                raise OSError('controlled second audit inventory failure')
            return real(root)
        with patch.object(helper, 'project_inventory', side_effect=inventory):
            result = helper.audit_batch(self.root, self.batch(), timeout=5)
        self.assertEqual(len(result['audits']), 2)
        self.checks(result['audits'][1], 3)
        self.assertEqual(result['unrun_mutations'], 1)
        self.assertIsNone(result['audits'][1]['integrity']['project_guard']['unchanged'])

    def test_unremoved_scratch_is_reported_false_without_losing_checks(self):
        actual = helper.tempfile.TemporaryDirectory
        owner = self
        class RetainedScratch:
            def __init__(self, *args, **kwargs):
                self.directory = actual(*args, **kwargs)
                owner.addCleanup(self.directory.cleanup)

            def __enter__(self):
                return self.directory.name

            def __exit__(self, *args):
                pass  # Controlled removal failure; author cleanup runs afterward.

        recipe = dict(self.recipe, guard_project=False)
        with patch.object(helper.tempfile, 'TemporaryDirectory', RetainedScratch):
            with self.assertRaises(RuntimeError) as caught:
                helper.audit(self.root, recipe, timeout=5)
        result = caught.exception.audit_result
        self.assertEqual(len(result['checks']), 4)
        self.assertEqual(result['integrity_error']['stage'], 'scratch_removal')
        self.assertFalse(result['integrity']['owned_scratch_removed'])
        self.assertTrue(list(self.root.glob('.con-artist-*')))


if __name__ == '__main__':
    unittest.main()
