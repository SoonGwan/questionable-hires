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
import run_audit_proposal_01 as runner


class AuditProposalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        for condition in runner.CONDITIONS:
            (self.output / condition / 'skills').mkdir(parents=True)
        self.manifest = dict(identities=runner.identities(), cases=runner.cases(),
            schedule=[list(x) for x in runner.SCHEDULE], settings=dict(runner.SETTINGS),
            resource_digests=runner.digests(self.output), python_version=sys.version,
            completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False,
                           usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(runner, 'git', return_value=b'frozen'):
            runner.execute(self.output, self.manifest)

    def test_all_four_original_sessions_and_no_restart(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([(c.args[0]['id'], c.args[3].name) for c in cell.call_args_list],
                [(self.manifest['cases'][i]['id'], c) for i, c in runner.SCHEDULE])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(ValueError): self.execute()
            self.assertEqual(cell.call_count, 4)

    def test_drift_rejected_before_calls(self):
        for field, value in [('settings', {}), ('schedule', []), ('cases', []), ('identities', {})]:
            with self.subTest(field=field), patch.object(runner.run, 'run_cell') as cell:
                original = self.manifest[field]
                self.manifest[field] = value
                with self.assertRaises(ValueError): self.execute()
                self.manifest[field] = original
                cell.assert_not_called()
        (self.output / 'current/skills/changed').write_text('changed')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(ValueError): self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_exclusive_marker(self):
        (self.output / 'execution-started.json').write_text('{}')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(FileExistsError): self.execute()
            cell.assert_not_called()

    def test_limit_retains_schedule(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['schedule']), 4)
        self.assertEqual(len(saved['completed_cells']), 1)

    def test_original_task_preserved_and_separate_files(self):
        proposal, verified = runner.cases()
        original, = runner.original_cases()
        self.assertEqual(proposal['task'], original['task'])
        self.assertEqual(proposal['criteria'], original['criteria'])
        self.assertEqual(proposal['files'], verified['files'])
        verified['files']['AGENTS.md'] = 'changed'
        self.assertNotEqual(proposal['files'], verified['files'])
        self.assertEqual(len(proposal['criteria']), 5)
        self.assertEqual(len(verified['criteria']), 6)
