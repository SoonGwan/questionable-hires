import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import test_benchmark_runner as fixture

runner = fixture.runner


class IndexCaptureTests(unittest.TestCase):
    def test_native_child_index_is_retained_before_collector_changes_it(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root / 'results'
            output.mkdir()
            expected = root / 'child-index.bin'
            actual_popen = runner.subprocess.Popen
            def launch(args, **kwargs):
                if args[0] != 'codex':
                    return actual_popen(args, **kwargs)
                workspace = Path(args[args.index('-C') + 1])
                source = ('import pathlib, subprocess, json\n'
                    'root = pathlib.Path(' + repr(str(workspace)) + ')\n'
                    '(root/"source.py").write_text("VALUE = 2\\n")\n'
                    'subprocess.run(["git", "add", "source.py"], cwd=root, check=True)\n'
                    '(root/"new.txt").write_text("untracked content")\n'
                    'pathlib.Path(' + repr(str(expected)) + ').write_bytes((root/".git/index").read_bytes())\n'
                    'print(json.dumps({"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}))\n')
                return actual_popen([sys.executable, '-B', '-c', source], **kwargs)
            with patch.object(runner.subprocess, 'Popen', side_effect=launch):
                meta = runner.run_cell(dict(id='index', skill='receipt', task='Fixture',
                    files={'source.py': 'VALUE = 1\n'}), 'baseline', 1, output,
                    'gpt-6-astra', 'medium', 10, [], workspace_root=root / 'workspaces')
            cell = output / 'index--baseline--1'
            captured = meta['pre_collection_index']
            initial = meta['pre_model_index']
            self.assertEqual(initial['status'], 'retained')
            self.assertNotEqual(initial['sha256'], captured['sha256'])
            self.assertEqual(meta['index_comparison']['status'], 'observed')
            self.assertIs(meta['index_comparison']['bytes_and_mode_unchanged'], False)
            self.assertEqual(json.loads((cell/'git-index.before-model.json').read_text()), initial)
            self.assertEqual(captured['status'], 'retained')
            self.assertEqual((cell / captured['file']).read_bytes(), expected.read_bytes())
            self.assertEqual(captured['sha256'], hashlib.sha256(expected.read_bytes()).hexdigest())
            self.assertEqual(json.loads((cell/'git-index.before-collection.json').read_text()), captured)
            self.assertNotEqual((Path(meta['workspace'])/'.git/index').read_bytes(), expected.read_bytes())
            self.assertIn('+untracked content', (cell/'changes.diff').read_text())
            self.assertIn('+VALUE = 2', (cell/'changes.diff').read_text())
            export_spec = importlib.util.spec_from_file_location('index_export', runner.ROOT/'benchmarks/export.py')
            exporter = importlib.util.module_from_spec(export_spec)
            export_spec.loader.exec_module(exporter)
            (output/'run.json').write_text('{}')
            exporter.export(output, root/'export')
            exported = root/'export/index--baseline--1'
            exported_meta = json.loads((exported/'metadata.json').read_text())
            self.assertEqual(exported_meta['pre_collection_index'], captured)
            self.assertFalse((exported/captured['file']).exists())
            self.assertEqual(exported_meta['pre_model_index'], initial)
            self.assertFalse((exported/initial['file']).exists())

    def test_read_only_child_keeps_initial_index_identity(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root/'results'
            output.mkdir()
            actual_popen = runner.subprocess.Popen
            def launch(args, **kwargs):
                if args[0] != 'codex':
                    return actual_popen(args, **kwargs)
                return actual_popen([sys.executable, '-B', '-c',
                    'import json; print(json.dumps({"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}))'], **kwargs)
            with patch.object(runner.subprocess, 'Popen', side_effect=launch):
                meta = runner.run_cell(dict(id='read-only', skill='receipt', task='Fixture',
                    files={'source.py':'VALUE=1\n'}), 'baseline', 1, output,
                    'gpt-6-astra','medium',10,[],workspace_root=root/'workspaces')
            self.assertIs(meta['index_comparison']['bytes_and_mode_unchanged'], True)
            cell = output/'read-only--baseline--1'
            self.assertEqual((cell/meta['pre_model_index']['file']).read_bytes(),
                             (cell/meta['pre_collection_index']['file']).read_bytes())

    def test_bad_native_index_survives_subsequent_collector_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root/'results'
            output.mkdir()
            actual_popen = runner.subprocess.Popen
            def launch(args, **kwargs):
                if args[0] != 'codex':
                    return actual_popen(args, **kwargs)
                workspace = Path(args[args.index('-C') + 1])
                source = ('import pathlib; pathlib.Path(' + repr(str(workspace/'.git/index')) +
                          ').write_bytes(b"invalid fixture index"); print("original child output")')
                return actual_popen([sys.executable, '-B', '-c', source], **kwargs)
            with patch.object(runner.subprocess, 'Popen', side_effect=launch):
                with self.assertRaises(runner.subprocess.CalledProcessError):
                    runner.run_cell(dict(id='bad-index', skill='receipt', task='Fixture',
                        files={'source.py': 'VALUE=1\n'}), 'baseline', 1, output,
                        'gpt-6-astra', 'medium', 10, [], workspace_root=root/'workspaces')
            cell = output/'bad-index--baseline--1'
            self.assertEqual((cell/'git-index.before-collection.bin').read_bytes(), b'invalid fixture index')
            self.assertEqual(json.loads((cell/'git-index.before-collection.json').read_text())['status'], 'retained')
            self.assertEqual((cell/'stdout.original.jsonl').read_text(), 'original child output\n')
            self.assertFalse((cell/'metadata.json').exists())
            self.assertEqual(json.loads((cell/'git-index.before-model.json').read_text())['status'], 'retained')
            self.assertNotEqual((cell/'git-index.before-model.bin').read_bytes(), b'invalid fixture index')

    def test_unavailable_capture_is_unknown_not_an_unchanged_index(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root/'results'
            output.mkdir()
            actual_popen = runner.subprocess.Popen
            def launch(args, **kwargs):
                if args[0] != 'codex':
                    return actual_popen(args, **kwargs)
                return actual_popen([sys.executable, '-B', '-c', 'print("synthetic child")'], **kwargs)
            with patch.object(runner.subprocess, 'Popen', side_effect=launch), \
                 patch.object(runner, 'preserve_collector_index',
                              return_value=dict(status='unavailable', reason='synthetic unreadable control')):
                meta = runner.run_cell(dict(id='unknown-index', skill='receipt', task='Fixture',
                    files={'source.py':'VALUE=1\n'}), 'baseline', 1, output,
                    'gpt-6-astra','medium',10,[],workspace_root=root/'workspaces')
            self.assertEqual(meta['index_comparison']['status'], 'unknown')
            self.assertIsNone(meta['index_comparison']['bytes_and_mode_unchanged'])
            cell = output/'unknown-index--baseline--1'
            self.assertEqual(list(cell.glob('git-index.*.bin')), [])

    def test_local_snapshot_is_bounded_and_never_follows_links(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            workspace, cell = root/'project', root/'cell'
            (workspace/'.git').mkdir(parents=True)
            cell.mkdir()
            index = workspace/'.git/index'
            index.write_bytes(b'12345')
            with patch.object(runner, 'INDEX_CAPTURE_LIMIT', 4), patch.object(runner.os, 'open') as opened:
                self.assertEqual(runner.preserve_collector_index(workspace, cell)['status'], 'unavailable')
                opened.assert_not_called()
            index.unlink()
            index.symlink_to(root/'outside')
            with patch.object(runner.os, 'open') as opened:
                self.assertEqual(runner.preserve_collector_index(workspace, cell)['status'], 'unavailable')
                opened.assert_not_called()
            index.unlink()
            os.mkfifo(index)
            self.assertEqual(runner.preserve_collector_index(workspace, cell)['status'], 'unavailable')
            self.assertEqual(list(cell.iterdir()), [])

    def test_growth_is_rejected_without_partial_artifact(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            workspace, cell = root/'project', root/'cell'
            (workspace/'.git').mkdir(parents=True)
            cell.mkdir()
            index = workspace/'.git/index'
            index.write_bytes(b'12')
            actual_open = os.open
            def grow(path, *args):
                index.write_bytes(b'12345')
                return actual_open(path, *args)
            with patch.object(runner, 'INDEX_CAPTURE_LIMIT', 4), patch.object(runner.os, 'open', side_effect=grow):
                result = runner.preserve_collector_index(workspace, cell)
            self.assertEqual(result['status'], 'unavailable')
            self.assertIn('grew', result['reason'])
            self.assertEqual(list(cell.iterdir()), [])

    def test_invalid_git_layout_does_not_broaden_capture_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            workspace, cell = root/'project', root/'cell'
            workspace.mkdir()
            cell.mkdir()
            (workspace/'.git').write_text('gitdir: ../outside\n')
            with patch.object(runner.os, 'open') as opened:
                result = runner.preserve_collector_index(workspace, cell)
            self.assertEqual(result['status'], 'unavailable')
            opened.assert_not_called()


if __name__ == '__main__':
    unittest.main()
