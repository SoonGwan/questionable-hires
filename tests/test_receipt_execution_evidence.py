"""Returned native results survive later ordinary errors; failures stay failures."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_receipt_helper as fixture
import test_receipt_node_compare as node_fixture

helper = fixture.helper


class ReceiptExecutionEvidenceTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def partial(self, error, labels, *, removed=True):
        result = getattr(error, 'comparison_result', None)
        self.assertIsNotNone(result, 'Previously returned native evidence was discarded')
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), labels)
        self.assertEqual(result['execution_error']['type'], type(error).__name__)
        self.assertEqual(result['execution_error']['message'], str(error))
        self.assertTrue(result['originals']['unchanged'])
        self.assertIs(result['comparison_copies_removed'], removed)
        self.assertEqual(bool(list(self.root.glob('.receipt-*'))), not removed)
        for check in result['checks'].values():
            self.assertEqual(check['suite_observation']['tests'], 1)
            self.assertEqual(check['suite_observation']['skipped'], 0)
            self.assertIn('Verified copied import: rule ', check['output'])
        return result

    def failing_runner(self, position, error, *, after_return=False):
        actual = helper.run_check
        calls = []
        def run(*args):
            calls.append(args)
            if len(calls) == position:
                if after_return:
                    returned = actual(*args)
                    self.assertEqual(returned['native_exit_code'], 0)
                raise error
            return actual(*args)
        return run, calls

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

    def test_runner_error_retains_only_checks_returned_to_comparison(self):
        error = OSError('controlled second runner failure')
        execute, calls = self.failing_runner(2, error, after_return=True)
        with patch.object(helper, 'run_check', execute):
            with self.assertRaises(OSError) as caught:
                helper.compare(self.root, dict(self.recipe, guard_tree=True), timeout=5)
        self.assertIs(caught.exception, error)
        result = self.partial(error, ['before'])
        self.assertEqual(len(calls), 2)
        self.assertEqual(result['checks']['before']['native_exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertTrue(result['tree_guard']['unchanged'])

    def test_copy_error_retains_completed_before_without_starting_after(self):
        actual = Path.write_bytes
        error = PermissionError('controlled after-copy write failure')
        def write(path, content):
            if path.name == 'rule.py' and path.parent.name == 'after':
                raise error
            return actual(path, content)
        with patch.object(Path, 'write_bytes', write), patch.object(helper, 'run_check', wraps=helper.run_check) as execute:
            with self.assertRaises(PermissionError) as caught:
                helper.compare(self.root, self.recipe, timeout=5)
        self.assertIs(caught.exception, error)
        self.partial(error, ['before'])
        self.assertEqual(execute.call_count, 1)

    def test_unreadable_copy_absence_stays_unknown_without_masking_runner_error(self):
        actual = helper.os.lstat
        error = OSError('controlled second runner failure')
        execute, calls = self.failing_runner(2, error)
        def unavailable(path, *args, **kwargs):
            try:
                return actual(path, *args, **kwargs)
            except FileNotFoundError:
                if Path(path).name.startswith('.receipt-'):
                    raise PermissionError('controlled post-cleanup lookup failure')
                raise
        with patch.object(helper, 'run_check', execute), patch.object(helper.os, 'lstat', unavailable):
            with self.assertRaises(OSError) as caught:
                helper.compare(self.root, self.recipe, timeout=5)
        self.assertIs(caught.exception, error)
        result = getattr(error, 'comparison_result', None)
        self.assertIsNotNone(result)
        self.assertIsNone(result['comparison_copies_removed'], 'Unverified absence became confirmed removal')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertTrue(result['originals']['unchanged'])
        self.assertEqual(len(calls), 2)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_cleanup_error_retains_both_results_and_remaining_copy(self):
        with patch.object(helper.tempfile, 'TemporaryDirectory', self.retained_scratch()):
            with self.assertRaises(PermissionError) as caught:
                helper.compare(self.root, self.recipe, timeout=5)
        result = self.partial(caught.exception, ['before', 'after'], removed=False)
        self.assertEqual([c['native_exit_code'] for c in result['checks'].values()], [1, 0])

    def test_later_guard_keeps_execution_error_and_original_exception_precedence(self):
        with patch.object(helper.tempfile, 'TemporaryDirectory', self.retained_scratch()):
            with self.assertRaises(RuntimeError) as caught:
                helper.compare(self.root, dict(self.recipe, guard_tree=True), timeout=5)
        result = getattr(caught.exception, 'comparison_result', None)
        self.assertIsNotNone(result)
        self.assertIn('execution_error', result, 'Cleanup diagnostic was discarded by final guard')
        self.assertEqual(result['execution_error']['type'], 'PermissionError')
        self.assertEqual(result['preservation_error']['type'], 'RuntimeError')
        self.assertEqual(list(result['checks']), ['before', 'after'])
        self.assertTrue(result['originals']['unchanged'])
        self.assertFalse(result['tree_guard']['unchanged'])
        self.assertFalse(result['comparison_copies_removed'])

    def test_multiple_versions_stop_with_prior_returned_results(self):
        (self.root/'rule.py').write_text('def eligible(n): return n > 20\n')
        third = self.commit()
        error = subprocess.TimeoutExpired(['controlled-runner'], 5)
        execute, calls = self.failing_runner(3, error)
        with patch.object(helper, 'run_check', execute):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                helper.compare(self.root, dict(self.recipe, additional_before=[third]), timeout=5)
        self.assertIs(caught.exception, error)
        result = self.partial(error, ['before', 'before_2'])
        self.assertEqual(len(calls), 3)
        self.assertEqual(result['revisions']['before_2'], third)
        self.assertEqual([c['native_exit_code'] for c in result['checks'].values()], [1, 1])
        self.assertNotIn('after', result['checks'])

    def test_cli_main_emits_partial_json_and_failure_diagnostic(self):
        error = OSError('controlled second CLI runner failure')
        execute, calls = self.failing_runner(2, error)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(helper, 'run_check', execute), \
                patch.object(sys, 'argv', ['compare.py', '--source', str(self.root), '--spec', '-']), \
                patch.object(sys, 'stdin', io.StringIO(json.dumps(self.recipe))), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                status = helper.main()
            except SystemExit as exit_status:
                status = exit_status.code
        self.assertEqual(status, 2)
        self.assertIn(str(error), stderr.getvalue())
        self.assertTrue(stdout.getvalue(), 'CLI discarded the completed native result')
        result = json.loads(stdout.getvalue())
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertEqual(result['checks']['before']['native_exit_code'], 1)
        self.assertTrue(result['comparison_copies_removed'])
        self.assertEqual(len(calls), 2)

    def test_first_error_and_interrupt_keep_original_no_result_behavior(self):
        for position, error in [(1, OSError('first runner')), (2, KeyboardInterrupt())]:
            with self.subTest(position=position, error=type(error).__name__):
                execute, calls = self.failing_runner(position, error)
                with patch.object(helper, 'run_check', execute):
                    with self.assertRaises(type(error)) as caught:
                        helper.compare(self.root, self.recipe, timeout=5)
                self.assertIs(caught.exception, error)
                self.assertFalse(hasattr(error, 'comparison_result'))
                self.assertEqual(len(calls), position)
                self.assertFalse(list(self.root.glob('.receipt-*')))


@unittest.skipUnless(node_fixture.NODE, 'Requires Node')
class ReceiptNodeExecutionEvidenceTests(unittest.TestCase):
    setUpClass = node_fixture.NodeComparisonTests.setUpClass
    setUp = node_fixture.NodeComparisonTests.setUp
    git = node_fixture.NodeComparisonTests.git
    commit = node_fixture.NodeComparisonTests.commit

    def test_node_error_retains_actual_before_result(self):
        actual = helper.run_node_check
        error = OSError('controlled second Node runner failure')
        calls = []
        def run(*args):
            calls.append(args)
            if len(calls) == 2:
                raise error
            return actual(*args)
        with patch.object(helper, 'run_node_check', run):
            with self.assertRaises(OSError) as caught:
                helper.compare(self.root, self.recipe, node=node_fixture.NODE, timeout=5)
        self.assertIs(caught.exception, error)
        result = getattr(error, 'comparison_result', None)
        self.assertIsNotNone(result, 'Actual native Node evidence was discarded')
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertEqual(result['checks']['before']['native_exit_code'], 1)
        self.assertIn('not ok 1 - age boundary', result['checks']['before']['output'])
        self.assertTrue(result['tree_guard']['unchanged'])
        self.assertTrue(result['comparison_copies_removed'])
        self.assertEqual(len(calls), 2)
