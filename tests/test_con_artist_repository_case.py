from pathlib import Path
import sys
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from con_artist_repository_case import cases, preflight, source_files, IMPLEMENTATION, TEST
import con_artist_repository_case as fixture_module
from con_artist_fixture_support import native_controls, retained_sources


class ConArtistRepositoryCaseTests(unittest.TestCase):
    def test_actual_repository_tests_pass_and_reject_cross_call_cache(self):
        with native_controls(fixture_module):
            rows = preflight()
        self.assertEqual([r['exit_code'] for r in rows], [0, 1])
        self.assertEqual(rows[0]['test_sha256'], rows[1]['test_sha256'])
        self.assertNotEqual(rows[0]['implementation_sha256'], rows[1]['implementation_sha256'])

    def test_model_inputs_keep_original_source_and_tests_without_answer(self):
        with native_controls(fixture_module):
            fixture, = cases()
        sources = retained_sources()
        self.assertEqual(fixture['files'][IMPLEMENTATION], sources[IMPLEMENTATION])
        self.assertEqual(fixture['files'][TEST], sources[TEST])
        self.assertNotIn('_process_cache', fixture['task'])
        self.assertEqual(len(fixture['criteria']), 5)

    def test_retained_bytes_match_pinned_project_history_when_available(self):
        if not (ROOT / '.git').exists():
            self.skipTest('Source archive: no project-owned history; native controls still execute')
        identity = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT,
                                  capture_output=True, text=True, timeout=10)
        self.assertEqual(identity.returncode, 0, identity.stderr)
        self.assertEqual(Path(identity.stdout.strip()).resolve(), ROOT.resolve())
        revision = subprocess.run(['git', 'cat-file', '-e', fixture_module.REVISION + '^{commit}'],
                                  cwd=ROOT, capture_output=True, timeout=10)
        if revision.returncode:
            self.skipTest('Pinned commit absent; native retained-byte controls still execute')
        self.assertEqual(source_files(), retained_sources())
