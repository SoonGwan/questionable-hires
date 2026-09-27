"""Unavailable cleanup lookups must not become confirmed removal evidence."""
import contextlib
import errno
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import test_audit_project_guard as guards

helper = guards.helper


class AuditCleanupLookupTests(unittest.TestCase):
    setUp = guards.AuditProjectGuardTests.setUp

    def lookup_failure(self, code, ready):
        actual = Path.stat
        error = OSError(code, 'controlled scratch lookup failure')
        root = self.root.resolve()
        error.lookup_paths = []
        def stat(path, *args, **kwargs):
            if ready() and path.parent == root and path.name.startswith('.con-artist-'):
                error.lookup_paths.append(str(path))
                raise error
            return actual(path, *args, **kwargs)
        return stat, error

    def execute_counter(self, stop=None):
        actual = helper.execute
        calls = []
        def execute(*args):
            calls.append(args)
            if stop is not None and len(calls) == 2:
                raise stop
            return actual(*args)
        return execute, calls

    def four_checks(self, result):
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual({k:v['exit_code'] for k,v in result['checks'].items()},
                         dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        self.assertIn('AssertionError: 2', result['checks']['mutant_probe']['output'])
        self.assertIsNone(result['integrity']['owned_scratch_removed'])
        self.assertTrue(result['integrity']['selected_original_bytes_and_modes_unchanged'])

    def test_completed_native_audit_reports_unknown_lookup_and_preserves_oserror(self):
        for code in (errno.EBADF, errno.ENOTDIR, errno.ELOOP, errno.EACCES):
            with self.subTest(errno=code):
                execute, calls = self.execute_counter()
                stat, error = self.lookup_failure(code, lambda: len(calls) == 4)
                caught = None
                with patch.object(helper, 'execute', execute), patch.object(Path, 'stat', stat):
                    try:
                        result = helper.audit(self.root, self.recipe, timeout=5)
                    except OSError as raised:
                        caught = raised
                        result = raised.audit_result
                self.assertTrue(error.lookup_paths, 'Lookup fault was not reached')
                self.assertEqual((result['status'], result['integrity']['owned_scratch_removed']),
                                 ('incomplete', None))
                self.assertIs(caught, error)
                self.four_checks(error.audit_result)
                self.assertEqual(error.audit_result['integrity_error']['stage'], 'scratch_removal')
                self.assertTrue(error.audit_result['integrity']['project_guard']['unchanged'])
                self.assertEqual(len(calls), 4)
                self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_existing_runner_failure_keeps_identity_and_unknown_removal(self):
        error = OSError('controlled second runner failure')
        execute, calls = self.execute_counter(stop=error)
        stat, lookup_error = self.lookup_failure(errno.EBADF, lambda: len(calls) == 2)
        with patch.object(helper, 'execute', execute), patch.object(Path, 'stat', stat):
            with self.assertRaises(OSError) as caught:
                helper.audit(self.root, self.recipe, timeout=5)
        self.assertIs(caught.exception, error)
        self.assertTrue(lookup_error.lookup_paths, 'Lookup fault was not reached')
        result = error.audit_result
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests'])
        self.assertIn('Ran 1 test', result['checks']['correct_tests']['output'])
        self.assertEqual(result['execution_error']['message'], str(error))
        self.assertIsNone(result['integrity']['owned_scratch_removed'])
        self.assertEqual(len(calls), 2)

    def test_existing_project_guard_error_keeps_identity_and_unknown_removal(self):
        execute, calls = self.execute_counter()
        actual = helper.project_inventory
        inventories = []
        error = PermissionError('controlled final project inventory failure')
        def inventory(root):
            inventories.append(root)
            if len(inventories) == 2:
                raise error
            return actual(root)
        stat, lookup_error = self.lookup_failure(errno.EBADF, lambda: len(calls) == 4)
        with patch.object(helper, 'execute', execute), patch.object(helper, 'project_inventory', inventory), \
                patch.object(Path, 'stat', stat):
            with self.assertRaises(PermissionError) as caught:
                helper.audit(self.root, self.recipe, timeout=5)
        self.assertIs(caught.exception, error)
        self.assertTrue(lookup_error.lookup_paths, 'Lookup fault was not reached')
        self.four_checks(error.audit_result)
        self.assertEqual(error.audit_result['integrity_error']['stage'], 'project_guard')
        self.assertIsNone(error.audit_result['integrity']['project_guard']['unchanged'])

    def test_cli_returns_incomplete_json_with_unknown_removal(self):
        execute, calls = self.execute_counter()
        stat, lookup_error = self.lookup_failure(errno.EBADF, lambda: len(calls) == 4)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(helper, 'execute', execute), patch.object(Path, 'stat', stat), \
                patch.object(sys, 'argv', ['audit.py', '--spec', '-', '--source', str(self.root)]), \
                patch.object(sys, 'stdin', io.StringIO(json.dumps(self.recipe))), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = helper.main()
            except SystemExit as error:
                code = error.code
        self.assertTrue(lookup_error.lookup_paths, 'Lookup fault was not reached')
        self.assertEqual(code, 2)
        self.assertIn('controlled scratch lookup failure', stderr.getvalue())
        self.four_checks(json.loads(stdout.getvalue()))
        self.assertEqual(len(calls), 4)

    def test_batch_stops_after_unknown_removal_without_extra_native_checks(self):
        common = {k:self.recipe[k] for k in ('files','imports','tests','guard_project')}
        common['mutations'] = [dict(target='service.py', old='return 1', new='return '+str(n),
                                    probe=self.recipe['probe']) for n in (2,3,4)]
        execute, calls = self.execute_counter()
        stat, error = self.lookup_failure(errno.EBADF, lambda: len(calls) >= 4)
        caught = None
        with patch.object(helper, 'execute', execute), patch.object(Path, 'stat', stat):
            try:
                result = helper.audit_batch(self.root, common, timeout=5)
            except OSError as raised:
                caught = raised
                result = raised.audit_result
        self.assertTrue(error.lookup_paths, 'Lookup fault was not reached')
        self.assertEqual(len(calls), 4)
        self.assertIs(caught, error)
        self.assertEqual(result['unrun_mutations'], 2)
        self.assertEqual(len(result['audits']), 1)
        self.four_checks(result['audits'][0])
        self.assertEqual(len(calls), 4)

    def test_dangling_owned_symlink_is_present_not_removed(self):
        actual = helper.tempfile.TemporaryDirectory
        owner = self
        class DanglingScratch:
            def __init__(self, *args, **kwargs):
                self.directory = actual(*args, **kwargs)
            def __enter__(self):
                return self.directory.name
            def __exit__(self, *args):
                self.directory.cleanup()
                path = Path(self.directory.name)
                path.symlink_to(owner.root/'absent-target')
                owner.addCleanup(path.unlink)
        with patch.object(helper.tempfile, 'TemporaryDirectory', DanglingScratch):
            with self.assertRaises(RuntimeError) as caught:
                helper.audit(self.root, dict(self.recipe, guard_project=False), timeout=5)
        result = caught.exception.audit_result
        self.assertEqual(len(result['checks']), 4)
        self.assertFalse(result['integrity']['owned_scratch_removed'])
        self.assertEqual(result['integrity_error']['stage'], 'scratch_removal')


if __name__ == '__main__':
    unittest.main()
