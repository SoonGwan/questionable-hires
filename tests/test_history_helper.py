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
    def test_focused_hunk_selection_matches_intersection_boundaries(self):
        prefix = 'commit fixture\n--- a/a.py\n+++ b/a.py\n'
        hunks = [('@@ -1,2 +1,2 @@\n one\n two\n', 1, 2),
                 ('@@ -8 +8,0 @@\n-deleted\n', 8, 0),
                 ('@@ -12 +12 @@\n-old\n+new\n', 12, 1),
                 ('@@ -20,2 +20,2 @@\n three\n four\n', 20, 2)]
        source = prefix + ''.join(h[0] for h in hunks)
        for targets in ([], [0], [1], [2], [3], [8], [12], [13], [20], [21], [22],
                        [21, 1, 12, 12, 8], list(range(1, 101))):
            with self.subTest(targets=targets):
                selected = [text for text, start, count in hunks
                            if set(targets).intersection(range(start, start + count))]
                expected = (prefix + ''.join(selected), len(hunks) - len(selected)) if selected else (source, 0)
                self.assertEqual(helper.focused_patch(source, 'a.py', targets), expected)

    def test_header_gate_preserves_data_and_rejects_malformed_headers(self):
        prefix = '--- a/a.py\n+++ b/a.py\n'
        data = '@@ -1,1 +1,1 @@\n @@ -not a header\n'
        self.assertIn('old:1 new:1  @@ -not a header',
                      helper.selected_patch_excerpt(prefix + data, 'a.py', [1]))
        for header in ('@@ -x +1 @@', '@@ +1 -1 @@', '@@\t-1 +1 @@',
                       '@@ -1 +1 @', ' @@ -1 +1 @@', '@@ -1,2 +1,1 @@'):
            with self.subTest(header=header):
                self.assertIsNone(helper.selected_patch_excerpt(
                    prefix + header + '\n value\n', 'a.py', [1]))

    def test_incremental_budget_matches_full_render_at_every_boundary(self):
        header = '@@ -1,20 +1,20 @@'
        body = [f' 한글_{i}' for i in range(1, 21)]
        source = '--- a/a.py\n+++ b/a.py\n' + header + '\n' + '\n'.join(body) + '\n'
        rows = [header] + [f'old:{i} new:{i} {line}' for i, line in enumerate(body, 1)]

        def render(indices):
            output = []
            previous = -1
            for index in sorted(indices):
                if index > previous + 1:
                    output.append('[omitted patch rows]')
                output.append(rows[index])
                previous = index
            if previous < len(rows) - 1:
                output.append('[omitted patch rows]')
            return '\n'.join(output)

        for targets in ([1], [20], [1, 20], [4, 8, 12], list(range(1, 21))):
            for budget in range(0, len('\n'.join(rows)) + 2):
                selected = set(targets)
                expected = None
                if len(render(selected)) <= budget:
                    for distance in range(1, 4):
                        for target in targets:
                            for index in (target - distance, target + distance):
                                if 0 <= index < len(rows):
                                    trial = selected | {index}
                                    if len(render(trial)) <= budget:
                                        selected = trial
                    expected = render(selected)
                self.assertEqual(helper.selected_patch_excerpt(source, 'a.py', targets, budget),
                                 expected, (targets, budget))

    def test_excerpt_overlapping_windows_and_duplicate_targets(self):
        text = ('diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n'
                '@@ -1,150 +1,150 @@\n' +
                ''.join(f' row_{i}\n' for i in range(1, 151)))
        targets = list(range(20, 120))
        excerpt = helper.selected_patch_excerpt(text, 'a.py', targets)
        self.assertEqual(excerpt, helper.selected_patch_excerpt(
            text, 'a.py', list(reversed(targets)) + targets[:10]))
        numbered = [line for line in excerpt.splitlines() if line.startswith('old:')]
        self.assertEqual(numbered, [f'old:{i} new:{i}  row_{i}' for i in range(17, 123)])
        self.assertIsNone(helper.selected_patch_excerpt(text, 'a.py', targets, budget=100))

    def test_excerpt_keeps_distant_windows_and_validates_unselected_tail(self):
        text = ('diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n'
                '@@ -1,20000 +1,20000 @@\n' +
                ''.join(f' row_{i}\n' for i in range(1, 20001)))
        excerpt = helper.selected_patch_excerpt(text, 'a.py', [1, 10000, 20000])
        for number in (1, 2, 9997, 10000, 10003, 19997, 20000):
            self.assertIn(f'old:{number} new:{number}  row_{number}', excerpt)
        self.assertNotIn(' row_5000\n', excerpt)
        self.assertIn('[omitted patch rows]', excerpt)
        self.assertLessEqual(len(excerpt), 8000)
        # A selected early window does not excuse malformed later content.
        self.assertIsNone(helper.selected_patch_excerpt(text + '+unexpected\n', 'a.py', [1]))

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

    def test_git_lines_preserve_embedded_separators_and_carriage_returns(self):
        self.git('config', 'core.autocrlf', 'false')
        for separator in ('\v', '\f', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029', '\r'):
            for ending in ('\n', '\r\n', ''):
                with self.subTest(separator=repr(separator), ending=repr(ending)):
                    first = f'const label = "before{separator}after";'
                    second = 'const done = true;'
                    source = first + '\n' + second + ending
                    (self.root / 'legacy.py').write_bytes(source.encode('utf-8'))
                    commit = self.commit('Keep Git physical rows')
                    result = helper.trace(self.root, 'legacy.py', 1, 2)
                    expected = [first, second + ('\r' if ending == '\r\n' else '')]
                    self.assertEqual([r['text'] for r in result['current_lines']], expected)
                    self.assertEqual([r['text'] for r in result['blame']], expected)
                    self.assertEqual([r['current_line'] for r in result['blame']], [1, 2])
                    raw = subprocess.check_output(
                        ['git', 'show', '--format=', '--no-color', commit, '--', 'legacy.py'],
                        cwd=self.root).decode('utf-8')
                    excerpt = helper.selected_patch_excerpt(raw, 'legacy.py', [1, 2])
                    self.assertIsNotNone(excerpt)
                    self.assertIn(first, excerpt)
                    self.assertEqual((self.root / 'legacy.py').read_bytes(), source.encode('utf-8'))
                    with self.assertRaisesRegex(ValueError, 'Line range exceeds'):
                        helper.trace(self.root, 'legacy.py', 3, 3)

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

    def test_user_diff_presentation_does_not_hide_selected_evidence(self):
        path = self.root / 'legacy.py'
        noise = ['# unrelated ' + 'x' * 100 + '\n'] * 160
        gap = [f'SEPARATOR_{index} = {index}\n' for index in range(20)]
        path.write_text(''.join(noise + gap) + 'VALUE = "before"\n')
        self.commit('Prepare presentation-independent history')
        path.write_text(''.join(s.replace('xxx', 'yyy') for s in noise) +
                        ''.join(gap) + 'VALUE = "after"\n')
        self.commit('Change both regions')
        expected = helper.trace(self.root, 'legacy.py', 181, 181)['commits']
        self.assertIn('-VALUE = "before"', expected[0]['evidence'])
        self.assertIn('+VALUE = "after"', expected[0]['evidence'])
        self.assertEqual(expected[0]['omitted_hunks'], 1)
        for key, value in (('color.ui', 'always'), ('diff.noprefix', 'true')):
            with self.subTest(setting=key):
                self.git('config', key, value)
                config_before = (self.root / '.git/config').read_bytes()
                try:
                    actual = helper.trace(self.root, 'legacy.py', 181, 181)['commits']
                    self.assertEqual(actual, expected)
                    self.assertEqual((self.root / '.git/config').read_bytes(), config_before)
                finally:
                    self.git('config', '--unset', key)

    def test_single_large_hunk_retains_selected_historical_line_within_budget(self):
        path = self.root / 'legacy.py'
        noise = ['# unrelated ' + 'x' * 100 + '\n'] * 160
        path.write_text(''.join(noise) + 'VALUE = "before"\n')
        self.commit('Prepare contiguous change')
        path.write_text(''.join(s.replace('xxx', 'yyy') for s in noise) + 'VALUE = "after"\n')
        self.commit('Contiguous rewrite')
        raw = self.git('show', '--format=fuller', '--unified=3', 'HEAD', '--', 'legacy.py')
        self.assertGreater(raw.index('+VALUE = "after"'), 12000)
        self.assertEqual(raw.count('\n@@ '), 1)
        result = helper.trace(self.root, 'legacy.py', 161, 161)
        item = result['commits'][0]
        self.assertTrue(item['truncated'])
        self.assertNotIn('+VALUE = "after"', item['evidence'])
        self.assertIn('old:- new:161 +VALUE = "after"', item['selected_patch_excerpt'])
        self.assertIn('[omitted patch rows]', item['selected_patch_excerpt'])
        self.assertLessEqual(len(item['evidence']) + len(item['selected_patch_excerpt']), 12000)
        self.assertEqual(item['omitted_hunks'], 0)

    def test_excerpt_numbers_deletions_context_and_multiple_selected_lines(self):
        text = ('+++ b/a.py\n@@ -10,3 +20,3 @@\n-old\n+new\n context\n-last\n+final\n'
                '\\ No newline at end of file\n')
        excerpt = helper.selected_patch_excerpt(text, 'a.py', [20, 22])
        self.assertIn('old:10 new:- -old', excerpt)
        self.assertIn('old:- new:20 +new', excerpt)
        self.assertIn('old:11 new:21  context', excerpt)
        self.assertIn('old:- new:22 +final', excerpt)
        self.assertIn('No newline', excerpt)

    def test_excerpt_does_not_guess_ambiguous_or_over_budget_evidence(self):
        text = '+++ b/a.py\n@@ -1 +1 @@\n-old\n+new\n'
        for source, path, lines in ((text, 'a.py', [99]), (text, 'a.py', [1, 99]),
                                    (text.replace('-1 +1', '-1,2 +1'), 'a.py', [1]),
                                    (text + text, 'a.py', [1]),
                                    ('+++ b/a.py\n@@@ -1 -1 +1 @@@\n++new\n', 'a.py', [1])):
            with self.subTest(source=source, lines=lines):
                self.assertIsNone(helper.selected_patch_excerpt(source, path, lines))
        self.assertIsNone(helper.selected_patch_excerpt(text, 'a.py', [1], budget=3))

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
