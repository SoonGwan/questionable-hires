"""Replay retained regression and two-subtest derivative on frozen native controls."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from editor_snapshot_cases import EDITOR, SUPPORT
from mother_observation_candidate import entry

OUT = ROOT / 'benchmarks/local-runs/mother-observation-native01'
OUT.mkdir(parents=True, exist_ok=False)
source = ROOT / 'benchmarks/results/all-eight-current-07/current/editor-snapshot-present--skill--1/project/test_editor.py'
original = source.read_text()
pending = '            self.assertEqual(payload, expected_saved)\n\n            acknowledge.set_result(None)'
stored = '            self.assertEqual(stored, [expected_saved])'
assert original.count(pending) == original.count(stored) == 1
candidate = original.replace(pending, '            with self.subTest(stage="pending snapshot"):\n                self.assertEqual(payload, expected_saved)\n\n            acknowledge.set_result(None)').replace(stored, '            with self.subTest(stage="stored snapshot"):\n                self.assertEqual(stored, [expected_saved])')
(OUT/'previous-test.py').write_text(original)
(OUT/'candidate-test.py').write_text(candidate)
shutil.copytree(ROOT/'skills/mother-in-law', OUT/'skill', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
path = OUT/'skill/SKILL.md'
path.write_text(entry(path.read_text()))
controls = [
    ('shallow', EDITOR, SUPPORT, (1, 2)),
    ('deep', EDITOR.replace('payload = dict(self.settings)', 'payload = deepcopy(self.settings)'), SUPPORT, (0, 0)),
    ('shallow-and-dirty', EDITOR.replace('self.saved_revision = revision', 'self.saved_revision = self.revision'), SUPPORT, (1, 3)),
    ('premature-ack', EDITOR, SUPPORT.replace('        await release\n', '        release.set_result(None)\n'), (2, 2)),
]
rows = []
for name, implementation, support, expected in controls:
    for index, (arm, test) in enumerate((('previous', original), ('candidate', candidate))):
        with tempfile.TemporaryDirectory(prefix=name+'-'+arm+'-', dir=OUT) as temporary:
            project = Path(temporary)
            inputs = {'editor.py': implementation, 'test_support.py': support, 'test_editor.py': test}
            for filename, content in inputs.items():
                (project/filename).write_text(content)
            hashes = {n: hashlib.sha256((project/n).read_bytes()).hexdigest() for n in inputs}
            timed_out = False
            try:
                p = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_editor'], cwd=project, capture_output=True, timeout=10)
                code, stdout, stderr = p.returncode, p.stdout, p.stderr
            except subprocess.TimeoutExpired as exc:
                timed_out = True
                code, stdout, stderr = None, exc.stdout or b'', exc.stderr or b''
            label = name+'-'+arm
            for stream, data in (('stdout', stdout), ('stderr', stderr)):
                (OUT/(label+'.'+stream)).write_bytes(data)
            diagnostic = stderr.decode(errors='replace')
            intact = hashes == {n: hashlib.sha256((project/n).read_bytes()).hexdigest() for n in inputs}
            files = sorted(p.name for p in project.iterdir())
            row = dict(control=name, arm=arm, exit_code=code, timed_out=timed_out,
                       native_three_methods='Ran 3 tests' in diagnostic,
                       assertion_failures=diagnostic.count('AssertionError:'),
                       errors='ERROR:' in diagnostic,
                       pending_subtest='stage=\'pending snapshot\'' in diagnostic,
                       stored_subtest='stage=\'stored snapshot\'' in diagnostic,
                       invalid_state_error='InvalidStateError' in diagnostic,
                       expected_assertion_failures=expected[index], input_hashes=hashes,
                       inputs_unchanged=intact, only_input_files=files==sorted(inputs),
                       stdout_sha256=hashlib.sha256(stdout).hexdigest(), stderr_sha256=hashlib.sha256(stderr).hexdigest())
            row['meets_control'] = (not timed_out and code==(1 if expected[index] else 0) and row['native_three_methods']
                                    and row['assertion_failures']==expected[index] and not row['errors']
                                    and not row['invalid_state_error'] and intact and row['only_input_files'])
            # A labeled failure is direct execution evidence, not an inference from test source.
            if arm=='candidate' and name in ('shallow','shallow-and-dirty'):
                row['meets_control'] &= row['pending_subtest'] and row['stored_subtest']
            row['reading_copy'] = diagnostic.replace(str(project), '<CONTROL>')
        row['owned_project_removed'] = not project.exists()
        rows.append(row)
        (OUT/'results.json').write_text(json.dumps(rows, indent=2)+'\n')
        print(json.dumps({k:row[k] for k in ('control','arm','exit_code','assertion_failures','meets_control','owned_project_removed')}), flush=True)
assert len(rows)==8 and all(x['meets_control'] and x['owned_project_removed'] for x in rows)
assert hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(original.encode()).hexdigest()
print('All eight authored native controls pass; zero model calls.')
