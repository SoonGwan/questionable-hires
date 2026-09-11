import importlib.util
from pathlib import Path
import sys
import unittest
import tempfile
import hashlib

directory = Path(__file__).resolve().parents[1] / 'benchmarks'
sys.path.insert(0, str(directory))
try:
    spec = importlib.util.spec_from_file_location('httpx_runner', directory / 'run_httpx.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
finally:
    sys.path.pop(0)


class HTTPXScheduleTests(unittest.TestCase):
    def test_snapshot_contains_helpers_and_references_from_commit(self):
        revision = runner.command(['git', 'rev-parse', 'HEAD'], runner.ROOT)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skill'
            hashes = runner.freeze_skill(runner.ROOT, revision, destination)
            for name in ('SKILL.md', 'agents/openai.yaml', 'scripts/audit.py', 'references/python-audit.md'):
                self.assertIn(name, hashes)
                self.assertEqual(hashes[name], hashlib.sha256((destination / name).read_bytes()).hexdigest())
            with self.assertRaises(FileExistsError):
                runner.freeze_skill(runner.ROOT, revision, destination)

    def test_bounded_check_does_not_schedule_other_tasks_or_arms(self):
        self.assertEqual(runner.make_schedule(['wsgi-cleanup'], ['skill', 'skill'], 1),
                         [('wsgi-cleanup', 'skill', 1)])

    def test_original_defaults_keep_twenty_seven_unique_cells(self):
        arms = ['baseline', 'control', 'skill']
        schedule = runner.make_schedule(runner.TASKS, arms, 3)
        expected = {(case, arm, repeat) for case in runner.TASKS
                    for arm in arms for repeat in range(1, 4)}
        self.assertEqual(len(schedule), 27)
        self.assertEqual(set(schedule), expected)
        self.assertEqual(schedule, runner.make_schedule(runner.TASKS, arms, 3))

    def test_invalid_repeat_rejected(self):
        with self.assertRaises(ValueError):
            runner.make_schedule(['wsgi-cleanup'], ['skill'], 0)
