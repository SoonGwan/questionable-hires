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
import run_con_artist_read_01 as runner
from con_artist_read_candidate import OLD, NEW
import con_artist_read_candidate as candidate_module
from runner_snapshot_support import controlled_revision_labels, require_history


class ConArtistReadRunnerTests(unittest.TestCase):
    @contextlib.contextmanager
    def synthetic_resources(self):
        def snapshot(directory, revision):
            self.assertEqual(revision, candidate_module.RESOURCE)
            root = Path(directory) / 'skills/con-artist'
            root.mkdir(parents=True)
            (root / 'SKILL.md').write_text('Synthetic instruction fixture.\n' + OLD + '\n')
            (root / 'support.txt').write_bytes(b'unchanged synthetic support\n')
        with controlled_revision_labels(runner), patch.object(candidate_module, 'original_snapshot', side_effect=snapshot):
            yield

    def invoke(self, execute=False):
        with patch.object(sys, 'argv', ['runner'] + (['--execute'] if execute else [])), contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_native_controls_reach_real_assertions(self):
        rows = runner.preflight()
        self.assertEqual([row['exit_code'] for row in rows], [0, 0, 0, 1])
        self.assertIn('AssertionError: Lists differ:', rows[-1]['output'])
        self.assertTrue(all(row['scratch_removed'] for row in rows))

    def test_only_entrypoint_changes_and_exclusive_order(self):
        with self.synthetic_resources(), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), patch.object(runner, 'preflight', return_value=[]), patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(runner.run, 'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            roots = [runner.OUTPUT / condition / 'skills' for condition in runner.CONDITIONS]
            original, candidate = [{str(p.relative_to(root)): p.read_bytes()
                                    for p in root.rglob('*') if p.is_file()} for root in roots]
            self.assertEqual(set(original), set(candidate))
            changed = [name for name in original if original[name] != candidate[name]]
            self.assertEqual(changed, ['con-artist/SKILL.md'])
            self.assertEqual(candidate[changed[0]].decode(), original[changed[0]].decode().replace(OLD, NEW))
            cell.return_value = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
            self.invoke(True)
            manifest = json.loads((runner.OUTPUT / 'run.json').read_text())
            self.assertEqual([row['condition'] for row in manifest['completed_cells']], ['original', 'candidate'])
            self.assertEqual([call.args[1] for call in cell.call_args_list], ['skill', 'skill'])
            with self.assertRaises(FileExistsError):
                self.invoke(True)
            self.assertEqual(cell.call_count, 2)

    def test_changed_resource_prevents_execution(self):
        with self.synthetic_resources(), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), patch.object(runner, 'preflight', return_value=[]), patch.object(runner.run, 'run_cell') as cell:
            self.invoke()
            entry = runner.OUTPUT / 'candidate/skills/con-artist/SKILL.md'
            entry.write_text(entry.read_text() + '\nchanged\n')
            with self.assertRaisesRegex(ValueError, 'Frozen'):
                self.invoke(True)
            cell.assert_not_called()
            self.assertFalse((runner.OUTPUT / 'execution-started.json').exists())

    def test_reviser_rejects_missing_duplicate_and_revised_anchor(self):
        for body in ('unknown', OLD + OLD, NEW):
            with self.subTest(body=body), self.assertRaises(ValueError):
                candidate_module.revise(body)

    def test_pinned_resources_only_change_entrypoint_bytes(self):
        require_history(self, ROOT, runner.REVISIONS.values())
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            manifests = []
            for changed in (False, True):
                root = Path(scratch) / str(changed)
                candidate_module.snapshot(root, candidate=changed)
                manifests.append(runner.run.resource_manifest(root / 'skills'))
            original, candidate = manifests
            self.assertEqual(set(original), set(candidate))
            self.assertEqual({p for p in original if original[p] != candidate[p]}, {'con-artist/SKILL.md'})
            original_entry = Path(scratch) / 'False/skills/con-artist/SKILL.md'
            candidate_entry = Path(scratch) / 'True/skills/con-artist/SKILL.md'
            self.assertEqual(candidate_entry.read_text(), original_entry.read_text().replace(OLD, NEW))
