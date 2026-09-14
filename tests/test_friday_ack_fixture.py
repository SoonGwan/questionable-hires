import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ack_cases', ROOT / 'benchmarks/friday_ack_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

PROBE = '''import json, pathlib, sqlite3, unittest
import application
class Contract(unittest.TestCase):
    def test_acknowledged_values(self):
        path = pathlib.Path('local.sqlite')
        db = sqlite3.connect(path)
        for name in ('001_initial.sql', '002_up.sql'):
            db.executescript(pathlib.Path(name).read_text())
        db.close()
        observed = []
        for version, operation, key, value, other in (
            ('old', 'update', 1, 20, 'new'), ('new', 'update', 1, 30, 'old'),
            ('old', 'insert', 2, 40, 'new'), ('new', 'insert', 3, 50, 'old')):
            self.assertEqual(application.write(path, version, operation, key, value),
                             {'acknowledged': True, 'id': key, 'value': value})
            self.assertEqual(application.read(path, version, key), value)
            observed.append(application.read(path, other, key))
        with self.assertRaises(sqlite3.IntegrityError):
            application.write(path, 'new', 'insert', 3, 999)
        self.assertEqual(application.read(path, 'new', 3), 50)
        db = sqlite3.connect(path)
        db.executescript(pathlib.Path('002_down.sql').read_text())
        db.close()
        observed += [application.read(path, 'old', key) for key in (1, 2, 3)]
        self.assertEqual(observed, EXPECTED)
        print(json.dumps(observed))
unittest.main(verbosity=2)
'''


class AckFixtureTests(unittest.TestCase):
    def run_probe(self, case, mutation=False):
        with tempfile.TemporaryDirectory(prefix='.friday-ack-', dir=ROOT / 'tests') as folder:
            project = Path(folder)
            for name, contents in case['files'].items():
                if mutation and name == 'application.py':
                    contents = contents.replace('with db:', 'if True:')
                (project / name).write_text(contents)
            before = {p.name: p.read_bytes() for p in project.iterdir()}
            expected = ([10, 20, None, 50, 20, 40, 50] if case['id'].endswith('gap')
                        else [20, 30, 40, 50, 30, 40, 50])
            process = subprocess.run([sys.executable, '-B', '-c',
                                      'EXPECTED = ' + repr(expected) + '\n' + PROBE],
                                     cwd=project, capture_output=True, text=True, timeout=10)
            self.assertEqual({name: (project / name).read_bytes() for name in before}, before)
            self.assertTrue((project / 'local.sqlite').is_file())
            return process, expected

    def test_real_caller_commits_and_independent_reads_distinguish_gap_control(self):
        for case in fixture.cases():
            with self.subTest(case=case['id']):
                process, expected = self.run_probe(case)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertIn('Ran 1 test', process.stderr)
                self.assertEqual(json.loads(process.stdout), expected)

    def test_missing_commit_fails_native_value_assertion(self):
        case = next(c for c in fixture.cases() if c['id'].endswith('control'))
        process, _ = self.run_probe(case, mutation=True)
        self.assertEqual(process.returncode, 1, process.stderr)
        self.assertIn('AssertionError: 10 != 20', process.stderr)
        self.assertIn('FAILED (failures=1)', process.stderr)
        self.assertNotIn('ERROR:', process.stderr)
