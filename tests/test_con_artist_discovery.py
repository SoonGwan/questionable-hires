from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import con_artist_discovery_case as case
import con_artist_discovery_candidate as candidate


class DiscoveryTests(unittest.TestCase):
    def test_real_positive_and_faulty_controls(self):
        rows = case.preflight()
        self.assertEqual([r['exit_code'] for r in rows], [0, 0, 0, 1])
        self.assertTrue(all(r['source_preserved'] and r['scratch_removed'] for r in rows))

    def test_only_path_disclosure_changes_task(self):
        unknown, known = case.cases()
        self.assertEqual(unknown['files'], known['files'])
        self.assertEqual(unknown['criteria'], known['criteria'])
        self.assertTrue(known['task'].startswith(unknown['task']+' Relevant paths: '))
        self.assertNotEqual(unknown['id'], known['id'])

    def test_revision_is_single_scoped_replacement_and_rejects_reapplication(self):
        original = (ROOT/'skills/con-artist/SKILL.md').read_text()
        revised = candidate.revise(original)
        self.assertEqual(revised.replace(candidate.NEW, candidate.OLD), original)
        for bad in (revised, original+candidate.OLD, original.replace(candidate.OLD,'')):
            with self.assertRaises(ValueError):
                candidate.revise(bad)

    def test_candidate_snapshot_preserves_every_support_file_and_mode(self):
        def local_snapshot(directory, revision):
            self.assertEqual(revision, candidate.RESOURCE)
            shutil.copytree(ROOT/'skills/con-artist', directory/'skills/con-artist')
        with tempfile.TemporaryDirectory() as scratch, patch.object(candidate, 'original_snapshot', side_effect=local_snapshot):
            original, revised = Path(scratch)/'original', Path(scratch)/'candidate'
            candidate.snapshot(original)
            candidate.snapshot(revised, candidate=True)
            def manifest(root):
                return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mode & 0o777)
                        for p in root.rglob('*') if p.is_file()}
            before, after = manifest(original), manifest(revised)
            self.assertEqual(before.keys(), after.keys())
            entry = 'skills/con-artist/SKILL.md'
            self.assertEqual([name for name in before if before[name] != after[name]], [entry])
            self.assertEqual(before[entry][1], after[entry][1])
