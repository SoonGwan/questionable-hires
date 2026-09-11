import importlib.util
from pathlib import Path
import subprocess
import json
import sys
import tempfile
import unittest

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

    def test_dirty_line_is_not_attributed_to_committed_intent(self):
        (self.root / 'legacy.py').write_text('def label(p):\n    return "uncommitted"\n')
        result = helper.trace(self.root, 'legacy.py', 2, 2)
        self.assertIsNone(result['blame'][0]['commit'])
        self.assertEqual(result['commits'], [])
        self.assertIn('legacy.py', result['working_status'])

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
