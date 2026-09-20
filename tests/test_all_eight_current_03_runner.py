"""Schedule integrity without depending on historical resources in unit tests."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run_all_eight_current_03 as runner


class Current03RunnerTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        scratch = self.stack.enter_context(tempfile.TemporaryDirectory(dir=ROOT/'benchmarks'))
        self.stack.enter_context(patch.object(runner, 'OUTPUT', Path(scratch)/'run'))
        self.stack.enter_context(patch.object(runner, 'preflight', return_value={}))
        self.stack.enter_context(patch.object(runner.run, 'disabled_skills', return_value=[]))

        def snapshot(directory):
            for case in runner.cases():
                path = directory/'skills'/case['skill']/'SKILL.md'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('Synthetic schedule resource; not skill evidence.\n')

        def git(*args):
            if len(args) != 2 or args[0] != 'rev-parse' or args[1] not in {runner.RESOURCE, 'HEAD'}:
                raise AssertionError('Unexpected synthetic Git call: '+repr(args))
            return ('unit-fixture-'+args[1]).encode()

        self.stack.enter_context(patch.object(runner, 'snapshot', side_effect=snapshot))
        self.stack.enter_context(patch.object(runner, 'git', side_effect=git))
        self.cell = self.stack.enter_context(patch.object(runner.run, 'run_cell'))
        self.cell.return_value = dict(completed=True, timed_out=False, limit_detected=False,
                                      usage={}, elapsed_seconds=1)

    def invoke(self, execute=False):
        with patch.object(sys, 'argv', ['runner']+(['--execute'] if execute else [])), contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def manifest(self):
        return json.loads((runner.OUTPUT/'run.json').read_text())

    def test_balanced_exact_schedule_and_exclusive_execution(self):
        self.invoke()
        self.cell.assert_not_called()
        expected = runner.schedule(runner.cases())
        self.assertEqual(len(expected), 16)
        self.assertEqual(sum(row['condition']=='current' for row in expected[::2]), 4)
        self.invoke(True)
        self.assertEqual([(c.args[0]['id'], c.args[1]) for c in self.cell.call_args_list],
                         [(r['case'], 'baseline' if r['condition']=='baseline' else 'skill') for r in expected])
        self.assertEqual(len(self.manifest()['completed_cells']), 16)
        self.assertEqual(self.manifest()['resource_revision'], 'unit-fixture-ee5eb28')
        with self.assertRaises(FileExistsError): self.invoke(True)
        self.assertEqual(self.cell.call_count, 16)

    def test_changed_resource_rejected_before_execution_marker(self):
        self.invoke()
        (runner.OUTPUT/'current/skills/landlord/SKILL.md').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'Frozen'): self.invoke(True)
        self.cell.assert_not_called()
        self.assertFalse((runner.OUTPUT/'execution-started.json').exists())

    def test_limit_retains_one_incomplete_cell_without_replacement(self):
        self.invoke()
        self.cell.return_value.update(completed=False, limit_detected=True)
        self.invoke(True)
        manifest = self.manifest()
        self.assertTrue(manifest['stopped_after_limit'])
        self.assertEqual(len(manifest['completed_cells']), 1)
        self.assertFalse(manifest['completed_cells'][0]['completed'])
        with self.assertRaises(FileExistsError): self.invoke(True)
        self.assertEqual(self.cell.call_count, 1)
