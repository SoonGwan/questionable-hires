"""Authored filesystem-publication audit; path disclosure is the only task variant."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

ENGINE = '''import json
from pathlib import Path


def install(destination, payload):
    destination = Path(destination)
    staged = destination.with_name(destination.name + '.pending')
    try:
        staged.write_bytes((json.dumps(payload, ensure_ascii=False, sort_keys=True) + '\\n').encode('utf-8'))
        staged.replace(destination)
        return {'published': payload['version']}
    finally:
        staged.unlink(missing_ok=True)
'''
BRIDGE = '''from engine import install as _install


def refresh(path, payload):
    return _install(path, payload)
'''
TESTS = '''import tempfile
from pathlib import Path
import unittest
from bridge import refresh as publish

ROOT = Path(__file__).resolve().parents[1]


class SuccessTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(scratch.cleanup)
        self.target = Path(scratch.name) / 'active.json'
        self.target.write_bytes(b'previous manifest\\n')

    def test_success(self):
        self.assertEqual(publish(self.target, {'version': 2, 'routes': ['/']}), {'published': 2})

    def test_unicode_success(self):
        self.assertEqual(publish(self.target, {'version': 3, 'routes': ['/서울', '/café']}), {'published': 3})
'''
STRONG = '''
    def test_actual_published_bytes(self):
        payload = {'version': 3, 'routes': ['/서울', '/café']}
        self.assertEqual(publish(self.target, payload), {'published': 3})
        actual = self.target.read_bytes()
        expected = ('{"routes": ["/서울", "/café"], "version": 3}\\n').encode('utf-8')
        print('AUTHOR_PUBLICATION_BYTES', repr(actual), repr(expected), flush=True)
        self.assertFalse(self.target.with_name('active.json.pending').exists())
        self.assertEqual(actual, expected)
'''
ANCHOR = '        staged.replace(destination)\n'


def files():
    return {
        'engine.py': ENGINE, 'bridge.py': BRIDGE, 'checks/test_engine.py': TESTS,
        'AGENTS.md': 'Audit only. Native runner: python3 -B -m unittest discover -s checks -v. '
            'No dependencies/services, delegation, publication, or production/test repair. '
            'Use only disposable copies inside this project for deliberate faults and stronger checks. '
            'Keep original bytes/modes, including notes.txt. Remove owned scratch after execution. '
            'No permanent harness/report is requested.\n',
        'requirements.md': 'Publishing a generated routing manifest returns the published version. '
            'Before returning success, replace the destination with the complete UTF-8 JSON payload: '
            'sort_keys=True, ensure_ascii=False, standard json.dumps separators, and a final LF. '
            'Remove the sibling .pending file on completion. Acknowledgment alone is not publication. '
            'This audit concerns omitted final replacement, not crash durability or concurrent writers.\n',
        'notes.txt': 'Owner draft: preserve exactly.\n',
    }


def cases():
    task = ('Audit whether the existing success tests detect a missing final replacement '
        'when publishing the routing manifest. Trace the actual tested entrypoint and writer '
        'binding in the same process as the checks. Run the existing native tests on correct '
        'code and an isolated fault that omits final replacement but preserves acknowledgment '
        'and pending-file cleanup. If they survive, run the same stronger native assertion '
        'on both versions: reopen the destination after the actual call and compare complete '
        'bytes for a Unicode payload against the documented format, with an existing destination '
        'seeded to different bytes. Confirm pending-file cleanup. Explain actual assertions and '
        'exits, distinguishing missing publication from setup errors. Follow AGENTS.md; preserve '
        'originals and remove disposable copies. Do not apply a production or test edit.')
    criteria = [
        'Both original native success tests execute on correct and isolated omitted-replacement code.',
        'The deliberate fault omits only final replacement, retaining acknowledgment and cleanup.',
        'Same-process evidence links the tested entrypoint and writer to the copied implementation.',
        'Stronger native assertion uses the actual call and reopened full Unicode bytes with distinct preexisting content; correct passes and faulty fails for publication, not setup.',
        'Cleanup is checked; original bytes/modes/owner notes remain intact and owned copies are removed.',
    ]
    return [dict(id='manifest-discovery-'+variant, skill='con-artist', files=files(),
                 task=task+suffix, criteria=list(criteria)) for variant, suffix in (
        ('unknown', ''),
        ('known', ' Relevant paths: checks/test_engine.py, bridge.py, engine.py, requirements.md.'))]


def preflight():
    if ENGINE.count(ANCHOR) != 1:
        raise ValueError('Unexpected publication anchor')
    rows = []
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(dir=root/'benchmarks') as scratch:
        for stronger in (False, True):
            for faulty in (False, True):
                work = Path(scratch)/f'{stronger}-{faulty}'
                selected = files()
                if stronger:
                    selected['checks/test_engine.py'] += STRONG
                if faulty:
                    selected['engine.py'] = ENGINE.replace(ANCHOR, '        pass  # omit final replacement\n')
                for name, body in selected.items():
                    path = work/name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(body)
                before = {p.relative_to(work).as_posix():(p.read_bytes(), p.stat().st_mode & 0o777)
                          for p in work.rglob('*') if p.is_file()}
                probe = '''import pathlib, sys, unittest
import engine, bridge
sys.path.insert(0, 'checks')
import test_engine
root = pathlib.Path.cwd()
assert pathlib.Path(engine.__file__).resolve() == root / 'engine.py'
assert pathlib.Path(bridge.__file__).resolve() == root / 'bridge.py'
assert pathlib.Path(test_engine.__file__).resolve() == root / 'checks/test_engine.py'
assert test_engine.publish is bridge.refresh
assert test_engine.publish.__globals__['_install'] is engine.install
print('AUTHOR_BINDINGS_VERIFIED', flush=True)
created = []
def observe(event, args):
    if event == 'tempfile.mkdtemp':
        created.append(pathlib.Path(args[0]))
sys.addaudithook(observe)
program = unittest.main(module=test_engine, argv=['unittest', '-v'], exit=False)
assert created and all(path.parent == root and not path.exists() for path in created)
print('AUTHOR_SCRATCH_VERIFIED', len(created), flush=True)
sys.exit(0 if program.result.wasSuccessful() else 1)
'''
                proc = subprocess.run([sys.executable, '-B', '-c', probe], cwd=work,
                                      capture_output=True, text=True, timeout=10)
                output = proc.stdout + proc.stderr
                expected = int(stronger and faulty)
                assert proc.returncode == expected, output
                assert f'Ran {3 if stronger else 2} tests' in output and 'ERROR:' not in output, output
                assert 'AUTHOR_BINDINGS_VERIFIED' in output, output
                assert f'AUTHOR_SCRATCH_VERIFIED {3 if stronger else 2}' in output, output
                if expected:
                    assert 'FAIL: test_actual_published_bytes' in output and 'previous manifest' in output, output
                    assert 'AssertionError:' in output and 'version' in output, output
                after = {p.relative_to(work).as_posix():(p.read_bytes(), p.stat().st_mode & 0o777)
                         for p in work.rglob('*') if p.is_file()}
                assert after == before
                assert set(work.iterdir()) == {work/name for name in ('engine.py','bridge.py','checks','AGENTS.md','requirements.md','notes.txt')}
                rows.append(dict(stronger=stronger, faulty=faulty, exit_code=proc.returncode,
                    output=output.replace(str(work), '<COPY>'),
                    source_sha256={name:hashlib.sha256(raw).hexdigest() for name,(raw,mode) in before.items()},
                    source_preserved=True, scratch_removed=True))
    return rows
