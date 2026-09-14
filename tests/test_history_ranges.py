import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/necromancer/scripts/trace.py'
spec = importlib.util.spec_from_file_location('history_ranges_helper', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class HistoryRangeTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.git('init', '-q', '--template=')
        self.git('config', 'user.name', 'Range Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        self.lines = [f'value_{i} = "old"\n' for i in range(1, 121)]
        self.path = self.root / 'legacy.py'
        self.path.write_text(''.join(self.lines))
        self.commit('Initial values')
        for i in (5, 40, 75):
            self.lines[i - 1] = f'value_{i} = "new"\n'
        self.path.write_text(''.join(self.lines))
        self.changed = self.commit('Update three distant values')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True).strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD')

    def test_batch_reuses_collection_without_reading_gap_or_losing_hunks(self):
        ranges = [(5, 5), (40, 40), (75, 75)]
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(helper, 'git', wraps=helper.git) as calls:
            separate = [helper.trace(self.root, 'legacy.py', start, end) for start, end in ranges]
        self.assertEqual(calls.call_count, 12)
        with patch.object(helper, 'git', wraps=helper.git) as calls:
            batched = helper.trace_ranges(self.root, 'legacy.py', ranges)
        self.assertEqual(calls.call_count, 4)
        for field in ('current_lines', 'blame'):
            self.assertEqual(batched[field], [r for result in separate for r in result[field]])
        self.assertEqual(batched['ranges'], [[5, 5], [40, 40], [75, 75]])
        self.assertEqual([c['commit'] for c in batched['commits']], [self.changed])
        self.assertEqual(batched['omitted_commits'], 0)
        for i in (5, 40, 75):
            self.assertIn(f'+value_{i} = "new"', batched['commits'][0]['evidence'])
            self.assertIn(f'-value_{i} = "old"', batched['commits'][0]['evidence'])
        self.assertNotIn('value_20', batched['commits'][0]['evidence'])
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_cli_repeated_ranges_retain_each_selection(self):
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--path', 'legacy.py',
                                  '--lines', '75:75', '--lines', '5:5', '--lines', '40:40'],
                                 cwd=self.root, capture_output=True, text=True, check=True, timeout=10)
        observed = json.loads(process.stdout)
        self.assertEqual([r['line'] for r in observed['current_lines']], [5, 40, 75])
        self.assertEqual(observed, helper.trace_ranges(self.root, 'legacy.py', [(75, 75), (5, 5), (40, 40)]))

    def test_union_limits_and_single_range_compatibility(self):
        selections = [(50, 100), [1, 50], (5, 5)]
        before = list(selections)
        self.assertEqual(helper.trace_ranges(self.root, 'legacy.py', selections),
                         helper.trace(self.root, 'legacy.py', 1, 100))
        self.assertEqual(selections, before)
        self.assertNotIn('ranges', helper.trace_ranges(self.root, 'legacy.py', [(5, 5)]))
        for invalid in (None, [], [(1, 1)] * 101, [(1, 101)], [(1, 50), (100, 150)],
                        [(0, 1)], [(2, 1)], [(True, 2)], [(1.0, 2)], [(1, 2, 3)], ['1:2']):
            with self.subTest(invalid=invalid), patch.object(helper, 'git') as git:
                with self.assertRaises(ValueError):
                    helper.trace_ranges(self.root, 'legacy.py', invalid)
                git.assert_not_called()
        with patch.object(helper, 'git') as git, self.assertRaisesRegex(ValueError, 'exceeds current file'):
            helper.trace_ranges(self.root, 'legacy.py', [(5, 5), (120, 121)])
        git.assert_not_called()
        for cap in (0, 6, True, 1.5):
            with self.subTest(cap=cap), patch.object(helper, 'git') as git:
                with self.assertRaises(ValueError):
                    helper.trace_ranges(self.root, 'legacy.py', [(5, 5)], max_commits=cap)
                git.assert_not_called()

    def test_rename_and_dirty_range_keep_attribution_distinct(self):
        self.git('mv', 'legacy.py', 'renamed.py')
        self.commit('Rename module')
        self.lines[39] = 'value_40 = "uncommitted"\n'
        (self.root / 'renamed.py').write_text(''.join(self.lines))
        result = helper.trace_ranges(self.root, 'renamed.py', [(5, 5), (40, 40), (75, 75)])
        self.assertEqual([r['commit'] for r in result['blame']], [self.changed, None, self.changed])
        self.assertEqual(result['commits'][0]['paths'], ['legacy.py'])
        self.assertIn('+value_75 = "new"', result['commits'][0]['evidence'])
        self.assertIn('renamed.py', result['working_status'])

    def test_commit_cap_is_global_and_omissions_remain_visible(self):
        commits = []
        for i in (5, 40, 75):
            self.lines[i - 1] = f'value_{i} = "separate"\n'
            self.path.write_text(''.join(self.lines))
            commits.append(self.commit('Update value ' + str(i)))
        result = helper.trace_ranges(self.root, 'legacy.py', [(5, 5), (40, 40), (75, 75)], max_commits=1)
        self.assertEqual([r['commit'] for r in result['blame']], commits)
        self.assertEqual([r['commit'] for r in result['commits']], commits[:1])
        self.assertEqual(result['omitted_commits'], 2)
