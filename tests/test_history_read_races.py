"""A post-stat replacement must not block or become current-source evidence."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/necromancer/scripts/trace.py'
PROBE = r'''
import importlib.util, inspect, os, pathlib, sys
spec = importlib.util.spec_from_file_location('history_probe', sys.argv[1])
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
root = pathlib.Path(sys.argv[2]).resolve()
target = root / 'selected.py'
target.write_text('value = 1\n')
real_stat = pathlib.Path.stat
swapped = False
def racing_stat(path, *args, **kwargs):
    global swapped
    result = real_stat(path, *args, **kwargs)
    # Python 3.11 resolve() also calls stat: race only the collector's explicit
    # size/type precheck, not earlier path resolution or symlink inspection.
    if (path == target and inspect.currentframe().f_back.f_code.co_name == 'trace_ranges'
            and kwargs.get('follow_symlinks', True) and not swapped):
        swapped = True
        os.replace(target, root / 'original-held')
        if sys.argv[3] == 'fifo':
            os.mkfifo(target)
        elif sys.argv[3] == 'symlink':
            (root / 'other').write_text('replacement = 2\n')
            target.symlink_to(root / 'other')
        else:
            target.write_text('replacement = 2\n')
    return result
def unexpected_git(*args):
    raise AssertionError('Replacement reached Git collection')
collector.git = unexpected_git
pathlib.Path.stat = racing_stat
try:
    collector.trace_ranges(root, 'selected.py', [(1, 1)])
except (ValueError, OSError) as error:
    assert swapped
    print(type(error).__name__ + ': ' + str(error))
else:
    raise SystemExit('Replacement was read as the inspected source')
'''


class HistoryReadRaceTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix' and hasattr(os, 'mkfifo'), 'POSIX replacement controls')
    def test_replacements_reject_before_git_without_blocking(self):
        for kind in ('fifo', 'file', 'symlink'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
                result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(SCRIPT), scratch, kind],
                                        capture_output=True, text=True, timeout=2)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(result.stdout.startswith(('ValueError:', 'OSError:')), result.stdout)
