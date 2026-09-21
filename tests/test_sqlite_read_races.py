"""Native file replacement probes; process bounds contain the pre-fix FIFO hang."""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/friday/scripts/sqlite_matrix.py'
PROBE = r'''
import importlib.util, os, pathlib, sys
spec = importlib.util.spec_from_file_location('matrix_probe', sys.argv[1])
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
root = pathlib.Path(sys.argv[2]).resolve()
mode, kind = sys.argv[3:5]
target = root / ('reader.py' if mode == 'reader' else 'schema.sql')
original = "QUERY = 'SELECT 1'\n" if mode == 'reader' else 'CREATE TABLE t(v);'
replacement = "QUERY = 'SELECT 99'\n" if mode == 'reader' else 'CREATE TABLE replacement(v);'
target.write_text(original)
real_path_open, real_os_open = pathlib.Path.open, os.open
swapped = False
def swap(path):
    global swapped
    if pathlib.Path(path) == target and not swapped:
        swapped = True
        os.replace(target, root / 'held-original')
        if kind == 'fifo': os.mkfifo(target)
        elif kind == 'symlink':
            (root / 'replacement').write_text(replacement)
            target.symlink_to(root / 'replacement')
        else: target.write_text(replacement)
def path_open(path, *args, **kwargs):
    swap(path)
    return real_path_open(path, *args, **kwargs)
def os_open(path, *args, **kwargs):
    swap(path)
    return real_os_open(path, *args, **kwargs)
pathlib.Path.open, os.open = path_open, os_open
connections = []
real_connect = helper.sqlite3.connect
def connect(*args, **kwargs):
    connections.append(args)
    return real_connect(*args, **kwargs)
helper.sqlite3.connect = connect
recipe = {'phases': [{'name': 'check', 'files': [] if mode == 'reader' else ['schema.sql']}],
          'checks': {'read': {'python_file': 'reader.py', 'constant': 'QUERY'} if mode == 'reader' else 'SELECT 1'}}
try:
    helper.matrix(recipe, root)
except (ValueError, OSError) as error:
    assert swapped and not connections, (swapped, connections)
    assert (root / 'held-original').read_text() == original
    print(type(error).__name__ + ': rejected before SQL')
else:
    assert swapped, 'Replacement hook did not exercise the source read'
    raise SystemExit('Replacement was accepted as the inspected source')
'''


class SQLiteReadRaceTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix' and hasattr(os, 'mkfifo'), 'POSIX replacement probes')
    def test_source_replacements_rejected_before_sql_without_waiting_for_fifo(self):
        for mode in ('reader', 'sql'):
            for kind in ('fifo', 'file', 'symlink'):
                with self.subTest(mode=mode, kind=kind), tempfile.TemporaryDirectory() as folder:
                    result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(SCRIPT), folder, mode, kind],
                        text=True, capture_output=True, timeout=2)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('rejected before SQL', result.stdout)

    def test_stable_reader_preserves_original_byte_hash_and_sql_result(self):
        spec = importlib.util.spec_from_file_location('matrix_regular', SCRIPT)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            raw = "QUERY = \"SELECT '서울' AS value\"\r\n".encode('utf-8')
            (root / 'reader.py').write_bytes(raw)
            (root / 'schema.sql').write_bytes(b'CREATE TABLE t(v);\r\n')
            result = helper.matrix({'phases': [{'name': 'one', 'files': ['schema.sql']}],
                'checks': {'q': {'python_file': 'reader.py', 'constant': 'QUERY'}}}, root)
            self.assertTrue(result['complete'])
            self.assertEqual(result['reader_sources']['q']['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(result['phases'][0]['checks']['q']['rows'], [('서울',)])
            self.assertEqual((root / 'reader.py').read_bytes(), raw)
