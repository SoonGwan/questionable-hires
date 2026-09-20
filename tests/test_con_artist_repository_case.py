from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from con_artist_repository_case import cases, preflight, source_files, IMPLEMENTATION, TEST


class ConArtistRepositoryCaseTests(unittest.TestCase):
    def test_actual_repository_tests_pass_and_reject_cross_call_cache(self):
        rows = preflight()
        self.assertEqual([r['exit_code'] for r in rows], [0, 1])
        self.assertEqual(rows[0]['test_sha256'], rows[1]['test_sha256'])
        self.assertNotEqual(rows[0]['implementation_sha256'], rows[1]['implementation_sha256'])

    def test_model_inputs_keep_original_source_and_tests_without_answer(self):
        fixture, = cases()
        sources = source_files()
        self.assertEqual(fixture['files'][IMPLEMENTATION], sources[IMPLEMENTATION])
        self.assertEqual(fixture['files'][TEST], sources[TEST])
        self.assertNotIn('_process_cache', fixture['task'])
        self.assertEqual(len(fixture['criteria']), 5)
