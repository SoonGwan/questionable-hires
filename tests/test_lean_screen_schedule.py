from collections import Counter
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run_lean_screen as screen


class LeanScheduleTests(unittest.TestCase):
    def test_every_task_gets_all_three_conditions_with_balanced_positions(self):
        selected = screen.cases()
        schedule = screen.schedule(selected)
        self.assertEqual(len(schedule), 24)
        positions = {condition: Counter() for condition in screen.CONDITIONS}
        for i, case in enumerate(selected):
            block = schedule[i*3:i*3+3]
            self.assertEqual({c['case'] for c in block}, {case['id']})
            self.assertEqual({c['condition'] for c in block}, set(screen.CONDITIONS))
            for position, cell in enumerate(block):
                positions[cell['condition']][position] += 1
        for counts in positions.values():
            self.assertEqual(sorted(counts.values()), [2, 3, 3])
        self.assertEqual(schedule, screen.schedule(selected))
        with self.assertRaises(ValueError):
            screen.schedule(selected[:-1])

    def test_real_frozen_snapshots_differ_only_in_eight_entries(self):
        with tempfile.TemporaryDirectory(prefix='lean-snapshots-', dir=ROOT/'benchmarks') as temporary:
            root = Path(temporary)
            screen.snapshot(root/'current')
            screen.snapshot(root/'lean', lean=True)
            current = screen.run.resource_manifest(root/'current/skills')
            lean = screen.run.resource_manifest(root/'lean/skills')
            self.assertEqual(set(current), set(lean))
            differences = {name for name in current if current[name] != lean[name]}
            self.assertEqual(differences, {c['skill']+'/SKILL.md' for c in screen.cases()})
            for name in differences:
                before = (root/'current/skills'/name).read_bytes()
                after = (root/'lean/skills'/name).read_bytes()
                self.assertEqual(before.split(b'\n---\n', 1)[0], after.split(b'\n---\n', 1)[0])
                self.assertEqual(current[name]['mode'], lean[name]['mode'])


if __name__ == '__main__':
    unittest.main()
