from contextlib import contextmanager
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run_httpx_json_01 as probe
from runner_snapshot_support import require_history


@contextmanager
def controlled_receipt():
    files = {
        'SKILL.md': ('100644', b'---\nname: receipt\ndescription: Synthetic fixture\n---\n\nSynthetic entry.\n'),
        'scripts/compare.py': ('100755', b'# Synthetic support, not executed\n'),
        'agents/openai.yaml': ('100644', b'interface: {}\n'),
    }
    revision = 'unit-fixture-httpx-receipt'
    objects = {str(i): raw for i, (_, raw) in enumerate(files.values())}
    listing = '\n'.join(f'{mode} blob {i}\tskills/receipt/{name}'
                        for i, (name, (mode, _)) in enumerate(files.items()))

    def git(*args):
        if args == ('ls-tree', '-r', revision, '--', 'skills/receipt'):
            return listing.encode()
        if len(args) == 3 and args[:2] == ('cat-file', 'blob') and args[2] in objects:
            return objects[args[2]]
        if args == ('rev-parse', 'HEAD'):
            return b'unit-fixture-launch'
        raise AssertionError('Unexpected synthetic Git request: ' + repr(args))

    with patch.object(probe, 'BASE', revision), patch.object(probe, 'git', side_effect=git):
        yield


class HttpxJsonProbeTests(unittest.TestCase):
    def test_real_snapshots_change_only_entry_and_keep_metadata(self):
        require_history(self, ROOT, [probe.BASE])
        self.check_snapshots()

    def test_synthetic_snapshots_preserve_support_and_metadata(self):
        with controlled_receipt():
            self.check_snapshots()

    def check_snapshots(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            probe.snapshot(root/'current')
            probe.snapshot(root/'lean', lean=True)
            current = probe.run.resource_manifest(root/'current/skills')
            lean = probe.run.resource_manifest(root/'lean/skills')
            self.assertEqual(set(current), set(lean))
            self.assertEqual([n for n in current if current[n] != lean[n]], ['receipt/SKILL.md'])
            entries = [(root/c/'skills/receipt/SKILL.md').read_text() for c in ('current', 'lean')]
            self.assertEqual(entries[0].split('\n---\n')[0], entries[1].split('\n---\n')[0])

    def test_prepare_never_calls_model_execute_once_preserves_all_cells(self):
        with controlled_receipt(), tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'probe'
            argv = ['probe', '--source', temporary, '--python', sys.executable]
            fake = dict(completed=True, timed_out=False, limit_detected=False,
                        usage=dict(input_tokens=1, output_tokens=1), elapsed_seconds=1)
            with patch.object(probe, 'OUTPUT', output), \
                    patch.object(probe, 'validate_source'), \
                    patch.object(probe.run, 'disabled_skills', return_value=[]), \
                    patch.object(probe.run, 'run_cell', return_value=fake) as execute:
                with patch.object(sys, 'argv', argv):
                    probe.main()
                execute.assert_not_called()
                self.assertFalse((output/'execution-started.json').exists())
                with patch.object(sys, 'argv', argv + ['--execute']):
                    probe.main()
                    with self.assertRaises(FileExistsError):
                        probe.main()
                self.assertEqual(execute.call_count, 3)
                manifest = json.loads((output/'run.json').read_text())
                self.assertEqual(manifest['resource_revision'], 'unit-fixture-httpx-receipt')
                self.assertEqual([c['condition'] for c in manifest['completed_cells']], list(probe.ORDER))
                self.assertEqual([c.args[1] for c in execute.call_args_list], ['skill', 'baseline', 'skill'])
                for call in execute.call_args_list:
                    self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
                    self.assertTrue(call.kwargs['persist_session'])

    def test_tampered_snapshot_rejects_before_execution_marker(self):
        with controlled_receipt(), tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'probe'
            argv = ['probe', '--source', temporary, '--python', sys.executable]
            with patch.object(probe, 'OUTPUT', output), patch.object(probe, 'validate_source'), \
                    patch.object(probe.run, 'run_cell') as execute:
                with patch.object(sys, 'argv', argv):
                    probe.main()
                (output/'lean/skills/receipt/scripts/compare.py').write_text('changed')
                with patch.object(sys, 'argv', argv + ['--execute']):
                    with self.assertRaisesRegex(ValueError, 'inputs/resources changed'):
                        probe.main()
                execute.assert_not_called()
                self.assertFalse((output/'execution-started.json').exists())
