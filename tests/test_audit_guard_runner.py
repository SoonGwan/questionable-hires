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
import run_audit_guard_01 as runner


class AuditGuardRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        for condition in runner.SCHEDULE:
            (self.output / condition / 'skills').mkdir(parents=True)
        self.manifest = dict(identities=runner.identities(), case=runner.case(),
            schedule=list(runner.SCHEDULE), resource_digests=runner.digests(self.output),
            python_version=sys.version, native_preflight={'sqlite_version': runner.sqlite3.sqlite_version},
            completed_cells=[], stopped_after_limit=False)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            runner.execute(self.output, self.manifest)

    def test_fixed_order_persists_original_sessions_and_refuses_restart(self):
        result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(runner.run, 'run_cell', return_value=result) as cell:
            self.execute()
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['skill', 'baseline', 'skill'])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(FileExistsError): self.execute()
            self.assertEqual(cell.call_count, 3)

    def test_frozen_task_and_resource_changes_refuse_before_calls(self):
        with patch.object(runner.run, 'run_cell') as cell:
            self.manifest['case']['task'] += ' changed'
            with self.assertRaisesRegex(ValueError, 'Frozen'): self.execute()
            self.manifest['case'] = runner.case()
            (self.output / 'current/skills/changed').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'Frozen'): self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_limit_preserves_unattempted_schedule(self):
        result = dict(completed=False, timed_out=False, limit_detected=True, usage={}, elapsed_seconds=1)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(runner.run, 'run_cell', return_value=result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['schedule']), 3)
        self.assertEqual(len(saved['completed_cells']), 1)

    def test_real_native_preflight_has_assertion_failure_and_clean_controls(self):
        result = runner.preflight()
        rows = result['observations']
        self.assertEqual([r['exit_code'] for r in rows], [0, 0, 0, 1])
        self.assertIn('AssertionError:', rows[-1]['output'])
        self.assertIn("(2, 'new')", rows[-1]['output'])
