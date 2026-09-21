"""Descriptor-level race controls; owned files only, with an outer hang deadline."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/receipt/scripts/compare.py'
PROBE = r'''
import importlib.util, json, os, pathlib, sys
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('receipt', sys.argv[1])
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
root = pathlib.Path(sys.argv[2])
kind = sys.argv[3]
selected = root / 'selected'
selected.write_bytes(b'original')
other = root / 'other'
other.write_bytes(b'original')
original_path_open, original_os_open = pathlib.Path.open, os.open
replaced = False
def swap(path):
    global replaced
    if pathlib.Path(path) != selected or replaced:
        return
    replaced = True
    selected.rename(root / 'old')
    if kind == 'fifo': os.mkfifo(selected)
    elif kind == 'symlink': selected.symlink_to(other)
    else: other.rename(selected)
def path_open(path, *args, **kwargs):
    swap(path)
    return original_path_open(path, *args, **kwargs)
def os_open(path, *args, **kwargs):
    swap(path)
    return original_os_open(path, *args, **kwargs)
with patch.object(pathlib.Path, 'open', path_open), patch.object(os, 'open', os_open):
    try:
        value = helper.read_limited(selected, 8)
        result = dict(status='accepted', value=value.decode())
    except (ValueError, OSError) as error:
        result = dict(status='rejected', error=type(error).__name__)
assert replaced
print(json.dumps(result))
'''


class ReceiptSelectedReadTests(unittest.TestCase):
    def test_replacements_rejected_without_waiting_on_fifo(self):
        for kind in ('fifo', 'symlink', 'regular'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                result = subprocess.run([sys.executable, '-B', '-c', PROBE,
                    str(SCRIPT), temporary, kind], capture_output=True, text=True, timeout=3)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], 'rejected')
