import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('transfer', Path(__file__).resolve().parents[1] / 'benchmarks/run_transfer.py')
transfer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transfer)


class TransferScheduleTests(unittest.TestCase):
    def run_mock(self, limited=False):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'experiment'
            def execute(command, **kwargs):
                destination = Path(command[command.index('--output') + 1])
                destination.mkdir()
                (destination / 'run.json').write_text(json.dumps(dict(finished_at='done', stopped_after_limit=limited)))
                return subprocess.CompletedProcess(command, 1 if limited else 0)
            with patch.object(sys, 'argv', ['run_transfer.py', '--output', str(output)]), patch.object(transfer.subprocess, 'check_output', return_value=b'frozen'), patch.object(transfer.subprocess, 'run', side_effect=execute) as run:
                with self.assertRaises(SystemExit):
                    transfer.main()
            records = json.loads((output / 'blocks.json').read_text())
            return records, run.call_args_list

    def test_rotated_conditions_and_fixed_execution_settings(self):
        records, calls = self.run_mock()
        self.assertEqual([r['condition'] for r in records], [condition for order in transfer.ORDERS for condition in order])
        self.assertEqual(len(calls), 9)
        for record, call in zip(records, calls):
            command = call.args[0]
            self.assertEqual(command[command.index('--jobs') + 1], '1')
            self.assertEqual(command[command.index('--seed') + 1], str(20260911 + record['block']))
            self.assertEqual('--skills-root' in command, record['condition'] != 'baseline')

    def test_limit_stops_outer_schedule_without_retry(self):
        records, calls = self.run_mock(limited=True)
        self.assertEqual(len(calls), 1)
        self.assertTrue(records[0]['stopped_after_limit'])


if __name__ == '__main__':
    unittest.main()
