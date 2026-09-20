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
import run_con_artist_discovery_01 as runner


class DiscoveryRunnerTests(unittest.TestCase):
    def setUp(self):
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        scratch = stack.enter_context(tempfile.TemporaryDirectory(dir=ROOT/'benchmarks'))
        stack.enter_context(patch.object(runner, 'OUTPUT', Path(scratch)/'run'))
        stack.enter_context(patch.object(runner, 'preflight', return_value=[]))
        stack.enter_context(patch.object(runner.run, 'disabled_skills', return_value=[]))
        def git(*args):
            if len(args)!=2 or args[0]!='rev-parse' or args[1] not in {runner.RESOURCE, 'HEAD'}:
                raise AssertionError('Unexpected Git call: '+repr(args))
            return ('synthetic-unit-'+args[1]).encode()
        def snapshot(directory, candidate=False):
            path = directory/'skills/con-artist/SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text('Synthetic schedule fixture '+str(candidate))
        stack.enter_context(patch.object(runner, 'git', side_effect=git))
        stack.enter_context(patch.object(runner, 'snapshot', side_effect=snapshot))
        self.cell = stack.enter_context(patch.object(runner.run, 'run_cell'))
        self.cell.return_value = dict(completed=True, timed_out=False, limit_detected=False,
                                      usage={}, elapsed_seconds=1)

    def invoke(self, execute=False):
        with patch.object(sys, 'argv', ['runner']+(['--execute'] if execute else [])), contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def manifest(self):
        return json.loads((runner.OUTPUT/'run.json').read_text())

    def test_exact_six_slots_and_exclusive_execution(self):
        self.invoke()
        self.cell.assert_not_called()
        self.assertFalse((runner.OUTPUT/'baseline/skills').exists())
        self.invoke(True)
        expected = [('manifest-discovery-'+case, arm) for case,arm in (
            ('unknown','baseline'), ('unknown','skill'), ('unknown','skill'),
            ('known','skill'), ('known','skill'), ('known','baseline'))]
        self.assertEqual([(c.args[0]['id'],c.args[1]) for c in self.cell.call_args_list], expected)
        self.assertEqual([c.args[3].name for c in self.cell.call_args_list],
                         ['baseline','original','candidate','candidate','original','baseline'])
        self.assertTrue(all(c.kwargs['persist_session'] for c in self.cell.call_args_list))
        self.assertEqual(len(self.manifest()['completed_cells']), 6)
        with self.assertRaises(FileExistsError): self.invoke(True)
        self.assertEqual(self.cell.call_count, 6)

    def test_changed_resource_rejects_before_marker_or_model(self):
        self.invoke()
        (runner.OUTPUT/'candidate/skills/con-artist/SKILL.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'Frozen'): self.invoke(True)
        self.cell.assert_not_called()
        self.assertFalse((runner.OUTPUT/'execution-started.json').exists())

    def test_changed_schedule_rejects_before_marker_or_model(self):
        self.invoke()
        manifest = self.manifest()
        manifest['schedule'].reverse()
        (runner.OUTPUT/'run.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Frozen'): self.invoke(True)
        self.cell.assert_not_called()
        self.assertFalse((runner.OUTPUT/'execution-started.json').exists())

    def test_account_limit_retains_incomplete_cell_without_replacement(self):
        self.invoke()
        self.cell.return_value.update(completed=False, limit_detected=True)
        self.invoke(True)
        manifest = self.manifest()
        self.assertTrue(manifest['stopped_after_limit'])
        self.assertEqual(len(manifest['completed_cells']), 1)
        self.assertFalse(manifest['completed_cells'][0]['completed'])
        with self.assertRaises(FileExistsError): self.invoke(True)
        self.assertEqual(self.cell.call_count, 1)
