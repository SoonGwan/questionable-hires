import importlib.util
from pathlib import Path
import subprocess
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('history_helper', ROOT / 'skills/necromancer/scripts/trace.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class HistoryHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q', '--template=')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        (self.root / 'legacy.py').write_text('def label(p):\n    return p["display"]\n')
        self.commit('Initial label')
        (self.root / 'legacy.py').write_text('def label(p):\n    return p.get("display") or p["name"]\n')
        self.changed = self.commit('Preserve partner compatibility')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True).strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD')

    def test_collects_current_line_and_introducing_patch_without_writes(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = helper.trace(self.root, 'legacy.py', 2, 2)
        self.assertEqual(result['history'], 'available')
        self.assertEqual(result['blame'][0]['commit'], self.changed)
        self.assertIn('Preserve partner compatibility', result['commits'][0]['evidence'])
        self.assertIn('+    return p.get', result['commits'][0]['evidence'])
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_cli_emits_parseable_evidence_for_only_selected_behavior(self):
        completed = subprocess.run(
            [sys.executable, '-B', str(ROOT / 'skills/necromancer/scripts/trace.py'),
             '--path', 'legacy.py', '--lines', '2:2'],
            cwd=self.root, text=True, capture_output=True, check=True)
        result = json.loads(completed.stdout)
        self.assertEqual(completed.stderr, '')
        self.assertEqual([item['commit'] for item in result['commits']], [self.changed])
        self.assertEqual([item['line'] for item in result['current_lines']], [2])

    def test_repository_facts_share_one_git_process(self):
        with patch.object(helper, 'git', wraps=helper.git) as calls:
            result = helper.trace(self.root, 'legacy.py', 2, 2)
        self.assertEqual(calls.call_count, 4)
        self.assertFalse(result['shallow'])
        self.assertEqual(result['blame'][0]['commit'], self.changed)
        self.assertIn('Preserve partner compatibility', result['commits'][0]['evidence'])

    def test_incomplete_repository_identity_is_not_guessed(self):
        response = subprocess.CompletedProcess([], 0, str(self.root) + '\n', '')
        with patch.object(helper, 'git', return_value=response):
            with self.assertRaisesRegex(ValueError, 'Incomplete repository identity'):
                helper.trace(self.root, 'legacy.py', 2, 2)

    def test_dirty_line_is_not_attributed_to_committed_intent(self):
        (self.root / 'legacy.py').write_text('def label(p):\n    return "uncommitted"\n')
        result = helper.trace(self.root, 'legacy.py', 2, 2)
        self.assertIsNone(result['blame'][0]['commit'])
        self.assertEqual(result['commits'], [])
        self.assertIn('legacy.py', result['working_status'])

    def test_unrelated_large_hunk_does_not_hide_selected_change(self):
        path = self.root / 'legacy.py'
        noise = ['# unrelated ' + 'x' * 100 + '\n'] * 160
        gap = [f'SEPARATOR_{index} = {index}\n' for index in range(20)]
        path.write_text(''.join(noise + gap) + 'VALUE = "before"\n')
        self.commit('Prepare separated changes')
        path.write_text(''.join([s.replace('xxx', 'yyy') for s in noise] + gap) + 'VALUE = "after"\n')
        commit = self.commit('Two independent edits')
        raw = self.git('show', '--format=fuller', '--unified=3', commit, '--', 'legacy.py')
        self.assertGreater(raw.index('+VALUE = "after"'), 12000)
        result = helper.trace(self.root, 'legacy.py', 181, 181)
        evidence = result['commits'][0]
        self.assertIn('+VALUE = "after"', evidence['evidence'])
        self.assertIn('-VALUE = "before"', evidence['evidence'])
        self.assertIn('Two independent edits', evidence['evidence'])
        self.assertEqual(evidence['omitted_hunks'], 1)
        self.assertFalse(evidence['truncated'])
        self.assertLess(len(evidence['evidence']), 1500)

    def test_focused_patch_falls_back_when_no_hunk_matches(self):
        text = '+++ b/a.py\n@@ -1 +1 @@\n-old\n+new\n'
        self.assertEqual(helper.focused_patch(text, 'a.py', [99]), (text, 0))
        combined = '+++ b/a.py\n@@@ -1 -1 +1 @@@\n++new\n'
        self.assertEqual(helper.focused_patch(combined, 'a.py', [1]), (combined, 0))

    def test_focused_patch_keeps_multiple_selected_hunks(self):
        text = ('commit evidence\n+++ b/a.py\n@@ -1 +1 @@\n-a\n+b\n'
                '@@ -20 +20 @@\n-c\n+d\n@@ -40 +40 @@\n-e\n+f\n')
        result, omitted = helper.focused_patch(text, 'a.py', [1, 40])
        self.assertEqual(omitted, 1)
        self.assertIn('+b', result)
        self.assertIn('+f', result)
        self.assertNotIn('+d', result)

    def test_rename_uses_historical_filename_for_patch(self):
        self.git('mv', 'legacy.py', 'renamed module.py')
        self.commit('Rename module')
        result = helper.trace(self.root, 'renamed module.py', 2, 2)
        self.assertEqual(result['blame'][0]['historical_path'], 'legacy.py')
        self.assertIn('Preserve partner compatibility', result['commits'][0]['evidence'])

    def test_untracked_file_has_current_text_but_no_invented_history(self):
        (self.root / 'new.py').write_text('VALUE = 1\n')
        result = helper.trace(self.root, 'new.py', 1, 1)
        self.assertEqual(result['history'], 'unavailable')
        self.assertEqual(result['current_lines'][0]['text'], 'VALUE = 1')

    def test_non_git_folder_returns_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'code.py').write_text('VALUE = 1\n')
            self.assertEqual(helper.trace(root, 'code.py', 1, 1)['history'], 'unavailable')

    def test_shallow_boundary_is_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / 'clone'
            subprocess.run(['git', 'clone', '-q', '--depth=1', self.root.as_uri(), str(clone)], check=True)
            result = helper.trace(clone, 'legacy.py', 2, 2)
            self.assertTrue(result['shallow'])
            self.assertTrue(result['blame'][0]['boundary'])
            self.assertIn('parent history is missing', result['commits'][0]['patch_unavailable'])
            self.assertIn('Preserve partner compatibility', result['commits'][0]['evidence'])
            self.assertNotIn('diff --git', result['commits'][0]['evidence'])
            self.assertIn('return p.get', result['current_lines'][0]['text'])

    def test_genuine_root_commit_keeps_patch(self):
        result = helper.trace(self.root, 'legacy.py', 1, 1)
        self.assertFalse(result['shallow'])
        self.assertTrue(result['blame'][0]['boundary'])
        self.assertNotIn('patch_unavailable', result['commits'][0])
        self.assertIn('diff --git', result['commits'][0]['evidence'])

    def test_omitted_commits_and_invalid_ranges_are_explicit(self):
        result = helper.trace(self.root, 'legacy.py', 1, 2, max_commits=1)
        self.assertEqual(len(result['commits']), 1)
        self.assertEqual(result['omitted_commits'], 1)
        for start, end in ((0, 1), (2, 1), (1, 101), (1, 3)):
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                helper.trace(self.root, 'legacy.py', start, end)

    def test_path_escape_and_symlink_rejected(self):
        (self.root / 'alias.py').symlink_to(self.root / 'legacy.py')
        for name in ('../legacy.py', '/tmp/legacy.py', '.git/config', 'alias.py'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                helper.trace(self.root, name, 1, 1)
