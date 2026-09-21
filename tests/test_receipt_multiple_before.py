import json
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_receipt_helper as fixture

helper = fixture.helper


class MultipleBeforeTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def prepare_versions(self):
        (self.root/'rule.py').write_text('def eligible(n): return n >= 17\n')
        other = self.commit()
        (self.root/'rule.py').write_text('def eligible(n): return n >= 18\n')
        tests = ('import unittest\nfrom rule import eligible\n'
                 'class Boundary(unittest.TestCase):\n'
                 '    def test_adult(self): self.assertTrue(eligible(18))\n'
                 '    def test_minor(self): self.assertFalse(eligible(17))\n')
        (self.root/'test_rule.py').write_text(tests)
        return other, dict(self.recipe, after={'working_tree': True}, guard_tree=True)

    def test_two_historical_failures_share_one_current_native_run(self):
        other, recipe = self.prepare_versions()
        before_tree = helper.tree_inventory(self.root)
        with patch.object(helper, 'run_check', wraps=helper.run_check) as native:
            first = helper.compare(self.root, recipe)
            second = helper.compare(self.root, dict(recipe, before=other))
            self.assertEqual(native.call_count, 4)
        with patch.object(helper, 'run_check', wraps=helper.run_check) as native:
            batch = helper.compare(self.root, dict(recipe, additional_before=[other]))
            self.assertEqual(native.call_count, 3)
        self.assertEqual(list(batch['checks']), ['before', 'before_2', 'after'])
        self.assertEqual(batch['revisions'], {'before': self.before, 'before_2': other, 'after': None})
        self.assertIn('test_adult', batch['checks']['before']['output'])
        self.assertIn('AssertionError: True is not false', batch['checks']['before_2']['output'])
        for key, expected in [('before', 1), ('before_2', 1), ('after', 0)]:
            check = batch['checks'][key]
            self.assertEqual(check['exit_code'], expected)
            self.assertIn('Ran 2 tests', check['output'])
            self.assertIn('Verified copied import: rule', check['output'])
            self.assertFalse(check['timed_out'])
            self.assertFalse(check['output_truncated'])
        for result in (first, second):
            self.assertEqual(result['fixed_sha256'], batch['fixed_sha256'])
            self.assertEqual(result['originals'], batch['originals'])
        self.assertTrue(batch['comparison_copies_removed'])
        self.assertEqual(helper.tree_inventory(self.root), before_tree)

    def test_invalid_or_duplicate_revisions_never_run_native_tests(self):
        for value in (None, 'HEAD', [None], [''], ['--all'], ['HEAD']*8,
                      [self.before], [self.before+'~0'], ['missing-ref']):
            with self.subTest(value=value), patch.object(helper, 'run_check') as native:
                with self.assertRaises((ValueError, RuntimeError)):
                    helper.compare(self.root, dict(self.recipe, additional_before=value))
                native.assert_not_called()

    def test_incomplete_first_check_does_not_claim_other_versions(self):
        other, recipe = self.prepare_versions()
        with patch.object(helper, 'run_check', return_value={'exit_code': 7, 'timed_out': False}) as native:
            result = helper.compare(self.root, dict(recipe, additional_before=[other]))
        self.assertEqual(native.call_count, 1)
        self.assertEqual(list(result['checks']), ['before'])
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['comparison_copies_removed'])

    def test_default_single_pair_still_has_two_native_runs(self):
        with patch.object(helper, 'run_check', wraps=helper.run_check) as native:
            result = helper.compare(self.root, dict(self.recipe, additional_before=[]))
        self.assertEqual(native.call_count, 2)
        self.assertEqual(list(result['checks']), ['before', 'after'])

    def test_extra_versions_do_not_bypass_shared_snapshot_budget(self):
        padding = '#' + 'x'*6_000_000 + '\n'
        (self.root/'rule.py').write_text(padding + 'def eligible(n): return n > 18\n')
        first = self.commit()
        (self.root/'rule.py').write_text(padding + 'def eligible(n): return n >= 18\n')
        second = self.commit()
        recipe = dict(self.recipe, before=first, after=second, additional_before=[second])
        with patch.object(helper, 'run_check') as native:
            with self.assertRaisesRegex(ValueError, 'snapshots exceed 20 MB'):
                helper.compare(self.root, recipe)
            native.assert_not_called()
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_other_runners_reject_extras_before_execution(self):
        for runner in ('pytest', 'node'):
            with self.subTest(runner=runner), patch.object(helper, 'run_check') as native, \
                    patch.object(helper, 'run_node_check') as node:
                with self.assertRaisesRegex(ValueError, 'currently requires unittest'):
                    helper.compare(self.root, dict(self.recipe, runner=runner, additional_before=[self.after]))
                native.assert_not_called()
                node.assert_not_called()

    def test_cli_and_module_invocation_retain_each_revision_and_observation(self):
        other, recipe = self.prepare_versions()
        recipe.update(additional_before=[other], invocation='module')
        result = subprocess.run([sys.executable, '-B', str(fixture.SCRIPT),
            '--source', str(self.root), '--spec', '-'], input=json.dumps(recipe),
            text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(list(report['checks']), ['before', 'before_2', 'after'])
        for label, expected in [('before', 1), ('before_2', 1), ('after', 0)]:
            check = report['checks'][label]
            self.assertTrue(check['provenance_ready'])
            self.assertEqual(check['native_exit_code'], expected)
            self.assertIn('Ran 2 tests', check['output'])
        self.assertTrue(report['tree_guard']['unchanged'])
        self.assertTrue(report['comparison_copies_removed'])


if __name__ == '__main__':
    unittest.main()
