"""Isolated entry packaging and guarded four-cell schedule, without Git history."""
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_receipt_bridge_route_01 as runner


class ReceiptBridgeRouteTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner.base.subprocess, 'check_output', return_value='synthetic CLI version'))
        stack.enter_context(patch.object(runner.base, 'git', return_value=b'synthetic-resource'))
        stack.enter_context(patch.object(runner.base.controls, 'check', return_value=[]))
        def snapshot(directory, revision):
            shutil.copytree(ROOT / 'skills/receipt', directory / 'skills/receipt', dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        stack.enter_context(patch.object(runner, 'original_snapshot', side_effect=snapshot))
        stack.enter_context(patch.object(runner.base.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.base.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_balanced_complete_schedule_and_no_restart(self):
        manifest = runner.base.prepare(self.output)
        stale = json.loads((self.output / 'run.json').read_text())
        runner.driver.execute(self.output, manifest)
        self.assertEqual([(c['case_id'], c['condition']) for c in manifest['completed_cells']],
                         [('windows-single', 'cli'), ('windows-single', 'bridge'),
                          ('windows-multiple', 'bridge'), ('windows-multiple', 'cli')])
        self.assertEqual(self.cell.call_count, 4)
        for call in self.cell.call_args_list:
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises((ValueError, FileExistsError)):
            runner.driver.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 4)

    def test_resource_drift_stops_before_any_call(self):
        manifest = runner.base.prepare(self.output)
        entry = self.output / 'bridge/skills/receipt/SKILL.md'
        entry.write_text(entry.read_text() + '\nchanged')
        with self.assertRaisesRegex(ValueError, 'Frozen'):
            runner.driver.execute(self.output, manifest)
        self.cell.assert_not_called()

    def test_incomplete_attempt_stops_and_cannot_resume(self):
        manifest = runner.base.prepare(self.output)
        self.cell.return_value = dict(completed=False, timed_out=True, limit_detected=False, usage={}, elapsed_seconds=1)
        runner.driver.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        self.assertTrue(manifest['stopped_after_uncompleted'])
        with self.assertRaises(ValueError):
            runner.driver.execute(self.output, manifest)

    def test_only_entry_body_changes_and_metadata_links_survive(self):
        runner.base.prepare(self.output)
        roots = [self.output / arm / 'skills/receipt' for arm in ('cli', 'bridge')]
        manifests = [runner.base.run.resource_manifest(root) for root in roots]
        self.assertEqual(set(manifests[0]), set(manifests[1]))
        self.assertEqual([name for name in manifests[0] if manifests[0][name] != manifests[1][name]], ['SKILL.md'])
        before, after = [(root / 'SKILL.md').read_text() for root in roots]
        self.assertEqual(before.split('\n---\n')[0], after.split('\n---\n')[0])
        self.assertEqual(runner.entry(after), after)
        for path in ('scripts/compare.py', 'references/existing-fix.md', 'references/node-comparison.md'):
            self.assertTrue((roots[1] / path).is_file())

    def test_launch_adapter_preserves_normal_rules(self):
        seen = []
        def launch(workspace, argv):
            seen.append(argv)
            return argv
        def cell(*args, **kwargs):
            return kwargs['launcher'](self.output, ['codex', 'exec', '--ignore-rules', '--json'])
        with patch.object(runner, 'original_cell', side_effect=cell):
            result = runner.run_cell(launcher=launch)
        self.assertEqual(result, ['codex', 'exec', '--json'])
        self.assertEqual(seen, [result])


if __name__ == '__main__':
    unittest.main()
