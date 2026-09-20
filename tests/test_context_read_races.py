"""Deterministic post-stat replacements; timeout bounds the old FIFO hang."""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/context.py'
PROBE = r'''
import importlib.util, os, pathlib, sys
spec = importlib.util.spec_from_file_location('context_probe', sys.argv[1])
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
root = pathlib.Path(sys.argv[2])
target = root / 'selected.py'
target.write_text('value = 1\n')
real_stat = pathlib.Path.stat
swapped = False
def racing_stat(path, *args, **kwargs):
    global swapped
    result = real_stat(path, *args, **kwargs)
    if path == target and kwargs.get('follow_symlinks', True) and not swapped:
        swapped = True
        os.replace(target, root / 'original-held')
        kind = sys.argv[3]
        if kind == 'fifo':
            os.mkfifo(target)
        elif kind == 'symlink':
            (root / 'other').write_text('replacement = 2\n')
            target.symlink_to(root / 'other')
        else:
            target.write_text('replacement = 2\n')
    return result
pathlib.Path.stat = racing_stat
budget = [0]
try:
    collector.read(root, pathlib.Path('selected.py'), budget)
except (ValueError, OSError) as error:
    assert swapped and budget == [0]
    print(type(error).__name__ + ': ' + str(error))
else:
    raise SystemExit('Replacement was read as the inspected file')
'''


class ContextReadRaceTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix' and hasattr(os, 'mkfifo'), 'POSIX file replacement probes')
    def test_post_stat_replacements_reject_without_blocking_or_charging_budget(self):
        for kind in ('fifo', 'file', 'symlink'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as scratch:
                result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(SCRIPT), scratch, kind],
                                        text=True, capture_output=True, timeout=2)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(result.stdout.startswith(('ValueError:', 'OSError:')), result.stdout)

    def test_regular_utf8_bytes_hash_and_budget_unchanged(self):
        spec = importlib.util.spec_from_file_location('context_regular', SCRIPT)
        collector = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(collector)
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            data = "label = '서울'\r\n".encode()
            (root / 'selected.py').write_bytes(data)
            budget = [17]
            source, digest = collector.read(root, Path('selected.py'), budget)
            self.assertEqual(source, data.decode())
            self.assertEqual(digest, hashlib.sha256(data).hexdigest())
            self.assertEqual(budget, [17 + len(data)])
