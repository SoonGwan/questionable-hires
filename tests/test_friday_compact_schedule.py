import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('compact', ROOT / 'benchmarks/run_friday_compact_01.py')
compact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compact)


class FridayCompactScheduleTests(unittest.TestCase):
    def test_frozen_snapshots_differ_only_in_entry_and_preserve_tasks(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'run'
            compact.prepare(output)
            for source in compact.SOURCES:
                self.assertEqual((output / source).read_bytes(), (ROOT / 'benchmarks' / source).read_bytes())
            with self.assertRaises(FileExistsError):
                compact.prepare(output)

    def run_fake(self, *, limit=False, missing=False, incomplete=False):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            commands = []
            def invoke(command, **kwargs):
                commands.append(command)
                destination = Path(command[command.index('--output') + 1])
                destination.mkdir()
                if not missing:
                    (destination / 'run.json').write_text(json.dumps({'finished_at': 'done', 'stopped_after_limit': limit}))
                return subprocess.CompletedProcess(command, int(limit or incomplete))
            status = compact.execute(output, invoke)
            return status, commands, json.loads((output / 'runs.json').read_text())

    def test_all_six_fixed_settings_and_no_retry_of_terminal_failure(self):
        status, commands, records = self.run_fake(incomplete=True)
        self.assertEqual(status, 1)
        self.assertEqual([(r['case'], r['condition']) for r in records], list(compact.SCHEDULE))
        for command in commands:
            for flag, value in [('--jobs', '1'), ('--repeats', '1'), ('--timeout', '240'), ('--arms', 'skill')]:
                self.assertEqual(command[command.index(flag) + 1], value)

    def test_limit_or_missing_manifest_stops_schedule(self):
        for option in ({'limit': True}, {'missing': True}):
            with self.subTest(option=option):
                status, commands, records = self.run_fake(**option)
                self.assertEqual(status, 2)
                self.assertEqual(len(commands), 1)
                self.assertTrue(records[0]['stopped'])
