"""Real source-history review under documented/unspecified executable contracts."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'benchmarks/interpreter_route_source_01.json'
CONTRACT = '''Python 3.9+ standard library, cooperative asyncio in one loop.
Each fetch call creates its own Request, even with repeated keys. Its application
task returns the exact object chosen through that Request.complete. The test owns
application tasks. Cancelling a pending started waiter must reach that waiter and
must not consume an undelivered request or cancel its application task. Already
delivered handles are consumed; later cancellation does not undo delivery.
No network, threads, browser or blocking code is in scope.
'''
TASK = '''Review the proposal to simplify ControlledFetch.started by restoring the
earlier implementation based on await asyncio.wait_for(self.calls.get(), timeout).
Change only started in disposable proposal copies; retain the current constructor,
__call__ and all other source so the proposal is evaluated independently.
Use the actual local source history to explain why the current mechanism was
introduced and whether it is still required by requirements.md. Cite local
introducing commits and distinguish these reconstructed source snapshots from
the complete original repository ancestry. Inspect the complete implementation
and execute the actual ControlledFetch.__call__/started path for both current
code and the proposed earlier implementation, retaining module bindings.
Check ordinary successful requests, repeated keys with independent handles and
reversed completion, and a deterministic cancellation during request wakeup.
Use bounded cooperative scheduling, not wall-clock delays. Give the observed
values/assertions, commands and individual process exits, preserving required
behaviors. A cancelled waiter and an already-delivered handle are different.
This is review, not implementation. Keep all originals, license, Git HEAD/index
and installed resources unchanged; owned scratch must be inside this project and
removed on all exits. No report/harness delivery, dependencies, network, external
history, delegation, commits or publication. Use Python with -B.
'''


def data():
    result = json.loads(SOURCE.read_text())
    assert len(result['snapshots']) == 2
    for row in result['snapshots']:
        if hashlib.sha256(row['source'].encode()).hexdigest() != row['sha256']:
            raise ValueError('Source bytes no longer match pinned Git blob')
    if hashlib.sha256(result['license'].encode()).hexdigest() != result['license_sha256']:
        raise ValueError('License identity changed')
    return result


def cases(python):
    source = data()
    output = []
    for label, documented in [('unspecified', False), ('documented', True)]:
        readme = CONTRACT + ('\nDocumented probe command: python3 -B <owned probe.py>.\n' if documented else '')
        history = [dict(message=row['message'], files={'controlled_fetch.py':row['source'],
                    'LICENSE':source['license'], 'requirements.md':readme})
                   for row in source['snapshots']]
        provenance = dict(upstream_snapshots=[{k:r[k] for k in ('upstream_commit','path','sha256')}
                                             for r in source['snapshots']], limitations=source['limitations'])
        files = dict(history[-1]['files'], **{'source-origin.json':json.dumps(provenance,indent=2)+'\n'})
        history.append(dict(message='Document the bounded review scope and source snapshot provenance',files=files))
        output.append(dict(id='interpreter-history-'+label, skill='necromancer', files=files,
            history=history, task=TASK, criteria=[
                'Trace actual source-history change and current explicit cancellation/handle contract, without external attribution claims.',
                'Execute actual current and proposed complete modules with bounded cooperative scheduling; verify ordinary and independent repeated-key outcomes.',
                'Demonstrate the distinguishing cancellation behavior with actual assertion/state evidence, not syntax/setup/timeout errors.',
                'Retain actual interpreter and individual exits; no false success from a later shell status.',
                'Preserve supplied source/license bytes/modes, HEAD/index and installed resources; clean owned scratch and stay in scope.']))
    return output


def source_hashes():
    names = ['benchmarks/interpreter_route_cases_01.py','benchmarks/interpreter_route_source_01.json',
             'tests/test_controlled_fetch_asset.py']
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def preflight():
    # Existing exposed native controls, adapted only at their source-file locator.
    original = (ROOT/'tests/test_controlled_fetch_asset.py').read_text()
    locator = "path = Path(__file__).resolve().parents[1] / 'skills/mother-in-law/assets/controlled_fetch.py'"
    assert original.count(locator) == 1
    snapshots = data()['snapshots']
    def method(source):
        cls = next(n for n in ast.parse(source).body if isinstance(n,ast.ClassDef) and n.name=='ControlledFetch')
        node = next(n for n in cls.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='started')
        return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
    current = snapshots[-1]['source']
    old, new = method(current), method(snapshots[0]['source'])
    assert current.count(old)==1 and old!=new
    proposed = current.replace(old,new)
    controls = []
    for label, source, expected in [('proposed-started-only',proposed,1),('current',current,0)]:
        with tempfile.TemporaryDirectory(prefix='qh-interpreter-author-') as folder:
            root = Path(folder)
            (root/'controlled_fetch.py').write_text(source)
            (root/'test_native.py').write_text(original.replace(locator,
                "path = Path(__file__).resolve().parent / 'controlled_fetch.py'"))
            result = subprocess.run([sys.executable,'-B','-m','unittest','-v','test_native'],cwd=root,
                                    capture_output=True,text=True,timeout=8)
            assert result.returncode == expected, result.stdout+result.stderr
            output = result.stdout+result.stderr
            assert 'Ran 8 tests' in output
            if expected: assert 'AssertionError: CancelledError not raised' in output
            controls.append(dict(variant=label,source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                                 exit_code=result.returncode,tests=8,output=output))
    return dict(kind='Author setup controls; existing exposed tests, not model outcome or performance',controls=controls)
