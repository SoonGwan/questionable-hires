"""Keep returned checks after copy, runner or cleanup exceptions; never infer others."""
import contextlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import test_audit_project_guard as guards

helper = guards.helper


class AuditExecutionEvidenceTests(unittest.TestCase):
    setUp = guards.AuditProjectGuardTests.setUp

    def partial(self, error, names):
        result = getattr(error, 'audit_result', None)
        self.assertIsNotNone(result, 'Previously returned native checks were discarded')
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), names)
        self.assertEqual(result['execution_error']['type'], type(error).__name__)
        self.assertTrue(result['integrity']['selected_original_bytes_and_modes_unchanged'])
        return result

    def failing_execute(self, position, exception, after_return=False):
        original = helper.execute
        calls = []
        def execute(*args):
            calls.append(args)
            if len(calls) == position:
                if after_return:
                    observed = original(*args)
                    self.assertEqual(observed['exit_code'], 0)
                raise exception
            return original(*args)
        return execute, calls

    def retained_scratch(self):
        actual = helper.tempfile.TemporaryDirectory
        owner = self
        class FailedCleanup:
            def __init__(self, *args, **kwargs):
                self.directory = actual(*args, **kwargs)
                owner.addCleanup(self.directory.cleanup)
            def __enter__(self):
                return self.directory.name
            def __exit__(self, *args):
                raise PermissionError('controlled owned-copy cleanup failure')
        return FailedCleanup

    def test_runner_exception_retains_only_returned_checks(self):
        error = OSError('controlled second runner failure')
        execute, calls = self.failing_execute(2, error, after_return=True)
        with patch.object(helper, 'execute', execute):
            with self.assertRaises(OSError) as caught:
                helper.audit(self.root, self.recipe, timeout=5)
        self.assertIs(caught.exception, error)
        result = self.partial(error, ['correct_tests'])
        self.assertIn('Ran 1 test', result['checks']['correct_tests']['output'])
        self.assertEqual(len(calls), 2)
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        self.assertTrue(result['integrity']['project_guard']['unchanged'])

    def test_copy_exception_keeps_both_returned_baselines(self):
        actual = Path.write_bytes
        error = PermissionError('controlled mutant copy write failure')
        def write(path, data):
            if path.name == 'service.py' and path.parent.name == 'mutant-tests':
                raise error
            return actual(path, data)
        with patch.object(Path, 'write_bytes', write):
            with self.assertRaises(PermissionError) as caught:
                helper.audit(self.root, self.recipe, timeout=5)
        self.assertIs(caught.exception, error)
        result = self.partial(error, ['correct_tests', 'correct_probe'])
        self.assertTrue(result['integrity']['owned_scratch_removed'])

    def test_cleanup_exception_preserves_type_and_reports_remaining_copy(self):
        with patch.object(helper.tempfile, 'TemporaryDirectory', self.retained_scratch()):
            with self.assertRaises(PermissionError) as caught:
                helper.audit(self.root, dict(self.recipe, guard_project=False), timeout=5)
        self.assertIs(type(caught.exception), PermissionError)
        result = self.partial(caught.exception, ['correct_tests', 'correct_probe', 'mutant_tests', 'mutant_probe'])
        self.assertIn('AssertionError: 2', result['checks']['mutant_probe']['output'])
        self.assertFalse(result['integrity']['owned_scratch_removed'])
        self.assertTrue(list(self.root.glob('.con-artist-*')))

    def test_cleanup_plus_guard_failure_keeps_both_errors(self):
        with patch.object(helper.tempfile, 'TemporaryDirectory', self.retained_scratch()):
            with self.assertRaises(RuntimeError) as caught:
                helper.audit(self.root, self.recipe, timeout=5)
        # The existing final project guard still supersedes the cleanup exception.
        self.assertIs(type(caught.exception), RuntimeError)
        result = getattr(caught.exception, 'audit_result', None)
        self.assertIsNotNone(result)
        self.assertIn('execution_error', result, 'Cleanup failure was discarded')
        self.assertEqual(result['execution_error']['type'], 'PermissionError')
        self.assertEqual(result['integrity_error']['type'], 'RuntimeError')
        self.assertEqual(len(result['checks']), 4)
        self.assertFalse(result['integrity']['owned_scratch_removed'])
        self.assertFalse(result['integrity']['project_guard']['unchanged'])

    def test_batch_keeps_prior_audit_and_references_then_stops(self):
        common = {k:self.recipe[k] for k in ('files', 'imports', 'tests', 'guard_project')}
        common['mutations'] = [dict(target='service.py', old='return 1', new='return '+str(n),
                                   probe=self.recipe['probe']) for n in (2,3,4)]
        execute, calls = self.failing_execute(5, OSError('controlled later runner failure'))
        with patch.object(helper, 'execute', execute):
            result = helper.audit_batch(self.root, common, timeout=5)
        self.assertEqual(len(calls), 5)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 2)
        second = result['audits'][1]
        self.assertEqual(list(second['checks']), ['correct_tests', 'correct_probe'])
        for key in second['checks']:
            self.assertEqual(second['checks'][key]['observation_ref'], '#/audits/0/checks/'+key)
            self.assertNotIn('output', second['checks'][key])
        self.assertEqual(result['unrun_mutations'], 1)

    def test_cli_returns_incomplete_json_and_existing_exit_two(self):
        execute, calls = self.failing_execute(2, OSError('controlled CLI runner failure'))
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(helper, 'execute', execute), patch.object(sys, 'argv',
                ['audit.py', '--spec', '-', '--source', str(self.root)]), \
                patch.object(sys, 'stdin', io.StringIO(json.dumps(self.recipe))), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = helper.main()
            except SystemExit as error:
                code = error.code
        self.assertEqual(code, 2)
        self.assertIn('Audit not established:', stderr.getvalue())
        self.assertTrue(stdout.getvalue(), 'CLI discarded returned evidence')
        self.assertEqual(list(json.loads(stdout.getvalue())['checks']), ['correct_tests'])
        self.assertEqual(len(calls), 2)

    def test_no_observations_and_interruptions_preserve_existing_behavior(self):
        for position, error in ((1, OSError('first runner')), (2, KeyboardInterrupt())):
            with self.subTest(position=position):
                execute, calls = self.failing_execute(position, error)
                with patch.object(helper, 'execute', execute):
                    with self.assertRaises(type(error)) as caught:
                        helper.audit(self.root, self.recipe, timeout=5)
                self.assertIs(caught.exception, error)
                self.assertFalse(hasattr(error, 'audit_result'))
                self.assertFalse(list(self.root.glob('.con-artist-*')))


if __name__ == '__main__':
    unittest.main()
