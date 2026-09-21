"""Selected-input reads must reject post-inspection replacements."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/audit.py'
PROBE = r'''
import importlib.util, os, pathlib, sys
spec = importlib.util.spec_from_file_location('audit_probe', sys.argv[1])
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
root = pathlib.Path(sys.argv[2]).resolve()
mode, kind = sys.argv[3:5]
target = root / 'selected.py'; target.write_bytes(b'value = 1\n')
permissions = target.stat().st_mode & 0o777
real_path_open, real_os_open = pathlib.Path.open, os.open
swapped = False
def swap(path):
    global swapped
    if pathlib.Path(path) == target and not swapped:
        swapped = True
        os.replace(target, root / 'held-original')
        if kind == 'fifo': os.mkfifo(target)
        elif kind == 'symlink':
            (root / 'replacement').write_bytes(b'value = 1\n')
            target.symlink_to(root / 'replacement')
        else: target.write_bytes(b'value = 1\n')
def path_open(path, *args, **kwargs):
    swap(path); return real_path_open(path, *args, **kwargs)
def os_open(path, *args, **kwargs):
    swap(path); return real_os_open(path, *args, **kwargs)
pathlib.Path.open, os.open = path_open, os_open
try:
    result = helper.snapshot(root, ['selected.py']) if mode == 'snapshot' else helper.original_matches(target, b'value = 1\n', permissions)
except (ValueError, OSError):
    assert swapped
else:
    assert swapped
    assert mode == 'matches' and result is False, 'Replacement accepted as original source'
print('replacement rejected')
'''


class AuditReadRaceTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix' and hasattr(os, 'mkfifo'), 'POSIX race controls')
    def test_selected_input_replacements_rejected(self):
        for mode in ('snapshot', 'matches'):
            for kind in ('fifo', 'file', 'symlink'):
                with self.subTest(mode=mode, kind=kind), tempfile.TemporaryDirectory() as folder:
                    result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(SCRIPT), folder, mode, kind],
                        capture_output=True, text=True, timeout=2)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('replacement rejected', result.stdout)
