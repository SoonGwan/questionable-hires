"""Native preflight of binary rollback behavior; controls are not model inputs."""
import ast
import json
from pathlib import Path
import sqlite3
import unittest


CASES = Path(__file__).resolve().parents[1] / 'benchmarks/friday-binary-rollback-cases.json'


class BinaryRollbackFixtureTests(unittest.TestCase):
    def exercise(self, correct_down):
        case, = json.loads(CASES.read_text())
        files = case['files']
        queries = {}
        for label in ('old', 'new'):
            assignment, = ast.parse(files[label + '_reader.py']).body
            self.assertEqual(assignment.targets[0].id, 'QUERY')
            queries[label] = ast.literal_eval(assignment.value)
        db = sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.executescript(files['001_initial.sql'])
        self.assertEqual(db.execute(queries['old']).fetchall(),
                         [(1, b'\x00\xff\x80'), (2, b'\x01\xfe'), (3, b'')])
        db.executescript(files['002_up.sql'])
        self.assertEqual(db.execute(queries['new']).fetchall(),
                         [(1, '00FF80'), (2, '01FE'), (3, '')])
        db.executescript(files['verification_writes.sql'])
        current = db.execute(queries['new']).fetchall()
        self.assertEqual(current, [(1, 'FF0080'), (2, '01FE'), (3, ''), (4, '0001FF')])
        expected = [(key, bytes.fromhex(value)) for key, value in current]
        down = files['002_down.sql']
        if correct_down:
            # Author-only semantic control, never supplied as a model hint/fix.
            db.create_function('decode_hex', 1, bytes.fromhex)
            down = down.replace('CAST(payload_hex AS BLOB)', 'decode_hex(payload_hex)')
        db.executescript(down)
        return db.execute(queries['old']).fetchall(), expected

    def test_supplied_down_returns_wrong_bytes_despite_successful_reader(self):
        observed, expected = self.exercise(False)
        self.assertEqual(observed, [(1, b'FF0080'), (2, b'01FE'), (3, b''), (4, b'0001FF')])
        self.assertEqual([key for (key, actual), (_, wanted) in zip(observed, expected) if actual != wanted],
                         [1, 2, 4])
        with self.assertRaises(AssertionError) as failure:
            self.assertEqual(observed, expected)
        # Actual/expected bytes, not a harness/import exception, are visible.
        self.assertIn('FF0080', str(failure.exception))
        self.assertIn('\\xff', str(failure.exception))
        self.assertEqual(observed[2], expected[2])  # Empty binary remains a valid control.

    def test_decoding_control_preserves_current_binary_values(self):
        observed, expected = self.exercise(True)
        self.assertEqual(observed, expected)
        self.assertEqual(observed[0], (1, b'\xff\x00\x80'))  # Updated, not original data.
        self.assertEqual(observed[3], (4, b'\x00\x01\xff'))
