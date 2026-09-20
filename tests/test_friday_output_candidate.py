import copy
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import friday_output_candidate as candidate


class FridayOutputCandidateTests(unittest.TestCase):
    def test_only_api_example_changes_and_wrong_input_rejects(self):
        guide = (ROOT / 'skills/friday/references/sqlite-matrix.md').read_text()
        revised = candidate.revise(guide)
        self.assertEqual(revised.replace(candidate.CANDIDATE, candidate.ORIGINAL), guide)
        for invalid in ('', candidate.ORIGINAL * 2, revised):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                candidate.revise(invalid)

    def test_native_assertions_do_not_depend_on_serializing_full_result(self):
        helper = runpy.run_path(str(ROOT / 'skills/friday/scripts/sqlite_matrix.py'))
        recipe = {
            'phases': [{'name': 'initial', 'sql':
                        "CREATE TABLE entries(id INTEGER, payload BLOB); "
                        "INSERT INTO entries VALUES (1, x'00ff');"},
                       {'name': 'update', 'sql':
                        "UPDATE entries SET payload=x'80' WHERE id=1;"}],
            'checks': {'reader': 'SELECT id, payload FROM entries ORDER BY id'},
        }
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            result = helper['matrix'](recipe, Path(scratch))
        retained = copy.deepcopy(result)
        for phase, value in ((0, b'\x00\xff'), (1, b'\x80')):
            helper['assert_rows'](result, phase, 'reader', columns=['id', 'payload'],
                                  rows=[(1, value)])
        with self.assertRaises(AssertionError) as failure:
            helper['assert_rows'](result, 1, 'reader', columns=['id', 'payload'],
                                  rows=[(1, b'\x00\xff')])
        message = str(failure.exception)
        for detail in ('update', 'reader', 'expected', 'observed', "b'\\x00\\xff'", "b'\\x80'"):
            self.assertIn(detail, message)
        self.assertEqual(result, retained)
