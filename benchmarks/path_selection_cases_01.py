"""Authored path-selection diagnostic controls; no model execution on import."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COMMON_LOADER = '''from pathlib import Path

def read_limit(filename):
    return int(Path(filename).read_text())
'''
CACHED_LOADER = '''from functools import lru_cache
from pathlib import Path

@lru_cache(maxsize=8)
def read_limit(filename):
    return int(Path(filename).read_text())
'''
CWD_CLIENT = '''import os
from pathlib import Path
import loader

class Client:
    def __init__(self, root):
        self.root = Path(root).resolve()

    def select_root(self, root):
        self.root = Path(root).resolve()

    def load(self, filename="settings.txt"):
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            return loader.read_limit(filename)
        finally:
            os.chdir(previous)
'''
BOUND_CLIENT = '''from pathlib import Path
import loader

class Client:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self._read_root = self.root

    def select_root(self, root):
        self.root = Path(root).resolve()

    def load(self, filename="settings.txt"):
        return loader.read_limit(self._read_root / filename)
'''
TESTS = '''from pathlib import Path
import unittest
from client import Client

BASE = Path(__file__).resolve().parent

class PathTests(unittest.TestCase):
    def test_single_root(self):
        self.assertEqual(Client(BASE / "alpha").load(), 111)

    def test_other_filename(self):
        self.assertEqual(Client(BASE / "alpha").load("other.txt"), 333)

    def test_switch_root(self):
        client = Client(BASE / "alpha")
        self.assertEqual(client.load(), 111)
        client.select_root(BASE / "beta")
        self.assertEqual(client.load(), 222)
        client.select_root(BASE / "alpha")
        self.assertEqual(client.load(), 111)
'''
TASK = '''A client keeps returning the first project's settings after select_root;
a teammate suspects a cache. Diagnose the actual supplied client and loader,
without modifying any supplied file. Run all supplied native tests with
python3 -B -m unittest -v test_paths. Reproduce the incorrect result and retain
normal single-root/other-filename controls. Use a rerunnable local probe and JSON
trace to connect each requested root/filename, actual loader input, physical file
read (or absence of a read), and returned value. Cover alpha→beta→alpha with one
client and a fresh beta client; do not replace the application with a simulation.
Identify a discriminating observation and explain the supported mechanism and
smallest corrective direction; diagnosis does not authorize implementation.
Distinguish local evidence from unknown production behavior. Python 3 standard
library only; no installs, network, threads or external services. New probe/trace
files are permitted inside this project. Keep all original files unchanged.'''


def cases():
    result = []
    for name, loader, client in [('relative-cache', CACHED_LOADER, CWD_CLIENT),
                                  ('retained-binding', COMMON_LOADER, BOUND_CLIENT)]:
        result.append(dict(id='path-selection-' + name, skill='exorcist', task=TASK,
            files={'loader.py': loader, 'client.py': client, 'test_paths.py': TESTS,
                   'alpha/settings.txt': '111\n', 'beta/settings.txt': '222\n',
                   'alpha/other.txt': '333\n', 'beta/other.txt': '444\n',
                   'requirements.md': 'Every load selects its filename under the currently selected root. Root changes take effect on the next load. This is a sequential local reproduction, not a thread-safety or live-edit contract. New clients are independent.\n'},
            criteria=['All three supplied native tests run; the root-switch assertion fails with actual111 versus expected222, while normal controls pass.',
                      'Actual client/loader probe records alpha-beta-alpha and fresh beta client, loader inputs, physical reads or cache hits and returned values in rerunnable JSON evidence.',
                      'Diagnosis distinguishes the supported path/cache or retained-binding mechanism, gives a corrective direction without editing supplied files, and retains production uncertainty.']))
    return result


def preflight():
    observations = []
    for case in cases():
        with tempfile.TemporaryDirectory(prefix='qh-path-selection-', dir=ROOT) as directory:
            project = Path(directory)
            for name, content in case['files'].items():
                path = project / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            command = [sys.executable, '-B', '-m', 'unittest', '-v', 'test_paths']
            cold = subprocess.run([sys.executable, '-B', '-c', 'import client, loader'],
                                  cwd=project, capture_output=True, text=True, timeout=10)
            if cold.returncode:
                raise AssertionError(cold.stderr)
            failed = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=10)
            if failed.returncode != 1 or '111 != 222' not in failed.stderr or 'Ran 3 tests' not in failed.stderr or 'failures=1' not in failed.stderr:
                raise AssertionError(failed.stderr)
            if case['id'].endswith('relative-cache'):
                (project / 'loader.py').write_text(COMMON_LOADER)
            else:
                (project / 'client.py').write_text(BOUND_CLIENT.replace(
                    '        self.root = Path(root).resolve()\n\n    def load',
                    '        self.root = Path(root).resolve()\n        self._read_root = self.root\n\n    def load'))
            passed = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=10)
            if passed.returncode or 'Ran 3 tests' not in passed.stderr or not passed.stderr.rstrip().endswith('OK'):
                raise AssertionError(passed.stderr)
            observations.append(dict(case=case['id'], cold_import_exit=cold.returncode,
                defective=dict(exit=failed.returncode, native_output=failed.stderr.replace(str(project), '<PROJECT>')),
                healthy=dict(exit=passed.returncode, native_output=passed.stderr.replace(str(project), '<PROJECT>')),
                limitation='Author-only disposable controls; healthy edits are never supplied to models.'))
    return observations


if __name__ == '__main__':
    print(json.dumps(preflight(), indent=2))
