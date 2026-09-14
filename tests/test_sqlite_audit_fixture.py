import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sqlite_audit_cases', ROOT / 'benchmarks/con_artist_sqlite_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class SQLiteAuditFixtureTests(unittest.TestCase):
    def test_frozen_files_match_generator(self):
        self.assertEqual(json.loads((ROOT / 'benchmarks/con-artist-sqlite-cases.json').read_text()), fixture.cases())

    def test_native_receipts_survive_but_new_connection_rows_detect_lost_commit(self):
        observations = fixture.preflight()
        self.assertEqual([(o['faulty'], o['module'], o['exit_code']) for o in observations], [
            (False, 'test_receipts', 0), (False, 'test_durable', 0),
            (True, 'test_receipts', 0), (True, 'test_durable', 1)])
        self.assertTrue(all(o['scratch_removed'] for o in observations))
