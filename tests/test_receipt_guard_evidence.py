"""A preservation failure must retain completed native evidence without success."""
import json
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_receipt_helper as fixture

helper = fixture.helper


class ReceiptGuardEvidenceTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def inject_owned_change(self, *, delay=0):
        note = self.root / 'notes.txt'
        note.write_text('original')
        # This deliberate side effect is confined to the author-owned fixture.
        setup = ('\nfrom pathlib import Path\nimport time\n'
                 'def setUpModule():\n'
                 f'    Path({str(note)!r}).write_text("changed!")\n'
                 f'    time.sleep({delay!r})\n')
        (self.root / 'test_rule.py').write_text(self.tests + setup)
        return note

    def cli(self, recipe, *options):
        return subprocess.run([sys.executable, '-B', str(fixture.SCRIPT),
            '--source', str(self.root), '--spec', '-', *options],
            input=json.dumps(recipe), text=True, capture_output=True, timeout=8)

    def assert_retained(self, result, *, phases=('before', 'after')):
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(tuple(result['checks']), phases)
        self.assertEqual(result['revisions'], dict(before=self.before, after=self.after))
        self.assertTrue(result['comparison_copies_removed'])
        self.assertFalse(list(self.root.glob('.receipt-*')))
        if phases == ('before', 'after'):
            self.assertEqual([c['native_exit_code'] for c in result['checks'].values()], [1, 0])
            self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
            for check in result['checks'].values():
                self.assertEqual(check['suite_observation']['tests'], 1)
                self.assertEqual(check['suite_observation']['skipped'], 0)
                self.assertIn('Verified copied import: rule ', check['output'])

    def test_cli_selected_change_retains_both_results_but_exits_two(self):
        note = self.inject_owned_change()
        run = self.cli(dict(self.recipe, watch=['notes.txt']))
        self.assertEqual(run.returncode, 2)
        self.assertIn('Selected originals changed; not restored: notes.txt', run.stderr)
        self.assertTrue(run.stdout, 'Completed native evidence was discarded')
        result = json.loads(run.stdout)
        self.assert_retained(result)
        self.assertFalse(result['originals']['unchanged'])
        self.assertEqual(result['originals']['changed'], ['notes.txt'])
        self.assertEqual(result['preservation_error']['stage'], 'originals')
        self.assertEqual(note.read_text(), 'changed!')

    def test_module_tree_change_retains_results_and_distinct_guard_states(self):
        note = self.inject_owned_change()
        run = self.cli(dict(self.recipe, guard_tree=True, invocation='module'), '--pretty')
        self.assertEqual(run.returncode, 2)
        self.assertIn('Project tree changed', run.stderr)
        self.assertTrue(run.stdout, 'Completed native evidence was discarded')
        result = json.loads(run.stdout)
        self.assert_retained(result)
        self.assertTrue(result['originals']['unchanged'])
        self.assertFalse(result['tree_guard']['unchanged'])
        self.assertEqual(result['tree_guard']['changed'], ['notes.txt'])
        self.assertEqual(result['preservation_error']['stage'], 'tree_guard')
        self.assertEqual(note.read_text(), 'changed!')

    def test_timeout_then_guard_failure_keeps_only_executed_phase(self):
        self.inject_owned_change(delay=2)
        run = self.cli(dict(self.recipe, watch=['notes.txt']), '--timeout', '.3')
        self.assertEqual(run.returncode, 2)
        self.assertTrue(run.stdout, 'Timed-out native observation was discarded')
        result = json.loads(run.stdout)
        self.assert_retained(result, phases=('before',))
        self.assertTrue(result['checks']['before']['timed_out'])
        self.assertEqual(result['checks']['before']['native_exit_code'], -9)
        self.assertFalse(result['originals']['unchanged'])

    def test_api_still_raises_runtime_error_with_partial_evidence(self):
        self.inject_owned_change()
        with self.assertRaisesRegex(RuntimeError, 'Selected originals changed') as caught:
            helper.compare(self.root, dict(self.recipe, watch=['notes.txt']))
        result = getattr(caught.exception, 'comparison_result', None)
        self.assertIsNotNone(result, 'API guard error lost completed native checks')
        self.assert_retained(result)

    def test_unreadable_final_inventory_does_not_claim_tree_unchanged(self):
        original = helper.tree_inventory
        calls = []
        def inventory(root):
            calls.append(root)
            if len(calls) == 2:
                raise OSError('controlled final inventory unavailable')
            return original(root)
        with patch.object(helper, 'tree_inventory', side_effect=inventory):
            with self.assertRaisesRegex(OSError, 'controlled final inventory unavailable') as caught:
                helper.compare(self.root, dict(self.recipe, guard_tree=True))
        result = getattr(caught.exception, 'comparison_result', None)
        self.assertIsNotNone(result, 'Unreadable guard lost completed native checks')
        self.assert_retained(result)
        self.assertTrue(result['originals']['unchanged'])
        self.assertIsNone(result['tree_guard']['unchanged'])
        self.assertEqual(result['preservation_error']['type'], 'OSError')

    def test_failed_copy_cleanup_is_not_reported_as_removed(self):
        self.inject_owned_change()
        native = helper.tempfile.TemporaryDirectory
        class Unremoved:
            def __enter__(inner):
                inner.owned = native(prefix='.receipt-', dir=self.root)
                inner.path = inner.owned.__enter__()
                self.addCleanup(inner.owned.cleanup)
                return inner.path
            def __exit__(inner, *args):
                raise OSError('controlled copy cleanup failure')
        with patch.object(helper.tempfile, 'TemporaryDirectory', return_value=Unremoved()):
            with self.assertRaisesRegex(RuntimeError, 'Selected originals changed') as caught:
                helper.compare(self.root, dict(self.recipe, watch=['notes.txt']))
        result = getattr(caught.exception, 'comparison_result', None)
        self.assertIsNotNone(result, 'Guard error lost completed native checks')
        self.assertEqual(result['status'], 'incomplete')
        self.assertFalse(result['comparison_copies_removed'])
        self.assertTrue(list(self.root.glob('.receipt-*')))
        self.assertEqual([c['native_exit_code'] for c in result['checks'].values()], [1, 0])


if __name__ == '__main__':
    unittest.main()
