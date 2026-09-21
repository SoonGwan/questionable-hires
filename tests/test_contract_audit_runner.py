import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_contract_audit_01 as runner


class ContractAuditRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        for c in runner.CONDITIONS:
            (self.output / c / 'skills').mkdir(parents=True)
        self.manifest = dict(identities=runner.identities(), cases=runner.cases(),
            schedule=[list(row) for row in runner.SCHEDULE],
            resource_digests=runner.digests(self.output), python_version=sys.version,
            completed_cells=[], stopped_after_limit=False)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            runner.execute(self.output, self.manifest)

    def test_fixed_schedule_exclusive_original_sessions(self):
        result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(runner.run, 'run_cell', return_value=result) as cell:
            self.execute()
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['baseline', 'skill', 'skill', 'skill', 'skill', 'baseline'])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(FileExistsError):
                self.execute()
            self.assertEqual(cell.call_count, 6)

    def test_changed_resource_refused_before_calls(self):
        (self.output / 'prior/skills/changed').write_text('changed')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaisesRegex(ValueError, 'Frozen'):
                self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_limit_stops_preserving_schedule(self):
        result = dict(completed=False, timed_out=False, limit_detected=True, usage={}, elapsed_seconds=1)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(runner.run, 'run_cell', return_value=result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['schedule']), 6)
        self.assertEqual(len(saved['completed_cells']), 1)
