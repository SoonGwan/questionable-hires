"""Native Git controls for verification-only review after an isolated comparison."""
import os
import subprocess
import unittest

import test_receipt_helper as fixture


class GitReviewTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def prepare_review(self):
        self.git('config', 'core.fsmonitor', 'false')
        self.git('config', 'core.untrackedCache', 'false')
        self.git('config', 'diff.autoRefreshIndex', 'true')
        (self.root / 'staged.txt').write_text('staged owner work\n')
        self.git('add', 'staged.txt')
        (self.root / 'untracked.txt').write_text('untracked owner work\n')
        # Same bytes, deliberately stale cached stat information; no sleep/race.
        os.utime(self.root / 'rule.py', (1_000_000_000, 1_000_000_000))

    def review(self, optional_locks):
        prefix = (['git', '--no-optional-locks', '-c', 'diff.autoRefreshIndex=false']
                  if not optional_locks else ['git'])
        env = dict(os.environ, GIT_OPTIONAL_LOCKS='1')
        return [subprocess.run(prefix + args, cwd=self.root, env=env,
                               capture_output=True, text=True, check=True).stdout
                for args in [['diff', '--check'], ['diff', '--', 'test_rule.py'],
                             ['diff', '--cached', '--', 'staged.txt'],
                             ['status', '--porcelain', '--untracked-files=all']]]

    def test_same_review_evidence_without_optional_index_refresh(self):
        self.prepare_review()
        index = self.root / '.git/index'
        original = index.read_bytes()
        tree = fixture.helper.tree_inventory(self.root)
        without_refresh = self.review(optional_locks=False)
        self.assertEqual(index.read_bytes(), original)
        self.assertEqual(fixture.helper.tree_inventory(self.root), tree)
        self.assertIn('+    def test_boundary', without_refresh[1])
        self.assertIn('+staged owner work', without_refresh[2])
        self.assertIn('A  staged.txt', without_refresh[3])
        self.assertIn(' M test_rule.py', without_refresh[3])
        self.assertIn('?? untracked.txt', without_refresh[3])
        # Deliberate adverse control: ordinary review must reproduce a write.
        self.assertEqual(self.review(optional_locks=True), without_refresh)
        self.assertNotEqual(index.read_bytes(), original)

    def test_native_comparison_and_followup_review_preserve_whole_tree(self):
        self.prepare_review()
        tree = fixture.helper.tree_inventory(self.root)
        result = fixture.helper.compare(self.root, dict(
            self.recipe, invocation='module', guard_tree=True))
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertIn('Ran 1 test', result['checks']['after']['output'])
        self.assertTrue(result['comparison_copies_removed'])
        self.review(optional_locks=False)
        self.assertEqual(fixture.helper.tree_inventory(self.root), tree)


if __name__ == '__main__':
    unittest.main()
