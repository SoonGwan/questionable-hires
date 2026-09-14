"""Native controls for compact sequences, not a model-adoption test."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ack_fixture', ROOT / 'benchmarks/friday_ack_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

PROBE = '''import json, pathlib, sqlite3, unittest
import application
class Sequence(unittest.TestCase):
    def test_contract(self):
        path = pathlib.Path('local.sqlite')
        def migrate(name):
            db = sqlite3.connect(path)
            try: db.executescript(pathlib.Path(name).read_text())
            finally: db.close()
        expected = {1: 10}
        counts = {'writes': 0, 'mixed_reads': 0, 'rollback_reads': 0}
        def observe(mixed):
            for key, value in expected.items():
                for version in (('old', 'new') if mixed else ('old',)):
                    self.assertEqual(application.read(path, version, key), value,
                                     (version, key, 'mixed' if mixed else 'rollback'))
                    counts['mixed_reads' if mixed else 'rollback_reads'] += 1
        migrate('001_initial.sql')
        migrate('002_up.sql')
        observe(True)
        operations = [
            ('old','insert',2,-(2**63)), ('new','insert',3,2**63-1),
            ('old','update',1,0), ('new','update',1,-1),
            ('old','update',3,2**63-1), ('new','update',2,-(2**63)),
            ('new','update',2,1), ('old','update',3,-2),
            ('old','update',1,-1), ('new','update',1,2**63-1),
            ('old','update',2,-(2**63)), ('new','update',3,2**63-1)]
        for version, operation, key, value in operations:
            ack = application.write(path, version, operation, key, value)
            self.assertEqual(ack, {'acknowledged': True, 'id': key, 'value': value})
            expected[key] = value
            counts['writes'] += 1
            observe(True)  # All current records, not a stale or affected-row-only cache.
        migrate('002_down.sql')
        observe(False)
        print(json.dumps(counts))
unittest.main(verbosity=2)
'''


class WitnessSequenceTests(unittest.TestCase):
    def execute(self, mutation):
        case = next(c for c in fixture.cases() if c['id'].endswith('control'))
        files = dict(case['files'])
        if mutation.startswith('quota_'):
            files['002_up.sql'] = '\n'.join(line for line in files['002_up.sql'].splitlines()
                                            if not line.startswith('CREATE TRIGGER ' + mutation + ' ')) + '\n'
        elif mutation == 'rollback_loss':
            files['002_down.sql'] += 'UPDATE accounts SET quota = 0;\n'
        elif mutation == 'cross_record':
            files['002_up.sql'] = files['002_up.sql'].replace(
                'SET quota_limit=NEW.quota WHERE id=NEW.id', 'SET quota_limit=NEW.quota')
        with tempfile.TemporaryDirectory(prefix='.friday-witness-', dir=ROOT / 'tests') as folder:
            project = Path(folder)
            for name, source in files.items():
                (project / name).write_text(source)
            before = {p.name: p.read_bytes() for p in project.iterdir()}
            result = subprocess.run([sys.executable, '-B', '-c', PROBE], cwd=project,
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual({name: (project / name).read_bytes() for name in before}, before)
            return result

    def test_compact_sequence_preserves_full_state_observations(self):
        result = self.execute('none')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'writes': 12, 'mixed_reads': 72, 'rollback_reads': 3})

    def test_same_sequence_detects_each_consequential_fault(self):
        for mutation in ('quota_old_update', 'quota_new_update', 'quota_old_insert',
                         'rollback_loss', 'cross_record'):
            with self.subTest(mutation=mutation):
                result = self.execute(mutation)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('AssertionError:', result.stderr)
                self.assertIn('FAILED (failures=1)', result.stderr)
                self.assertNotIn('ERROR:', result.stderr)
