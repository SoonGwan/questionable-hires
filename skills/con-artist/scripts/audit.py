#!/usr/bin/env python3
"""Run one Python mutation audit in disposable copies, without editing inputs.

This is a test runner, not a security sandbox. Run only trusted local tests.
"""
import argparse
import codecs
import json
import os
from pathlib import Path
import signal
import selectors
import subprocess
import sys
import tempfile
import time


BOOTSTRAP = '''import importlib, json, pathlib, runpy, sys
spec = json.loads(sys.argv[1])
root = pathlib.Path.cwd().resolve()
sys.path.insert(0, str(root))
for name in spec['imports']:
    module = importlib.import_module(name)
    location = getattr(module, '__file__', None)
    if not location or not pathlib.Path(location).resolve().is_relative_to(root):
        raise RuntimeError('Import escaped copy: ' + name + ': ' + str(location))
    print('Verified copied import:', name, flush=True)
if spec['probe'] is not None:
    sys.argv = ['audit-probe']
    exec(compile(spec['probe'], '<audit-probe>', 'exec'), {'__name__': '__main__'})
else:
    sys.argv = [spec['runner']] + spec['tests']
    runpy.run_module(spec['runner'], run_name='__main__', alter_sys=True)
'''


def relative(name):
    path = Path(name)
    if not name or path.is_absolute() or any(p in ('.git', '..') for p in path.parts) or path == Path('.'):
        raise ValueError('Expected a project-relative file/directory: ' + str(name))
    return path


def snapshot(root, names):
    files = {}
    total = 0
    for name in names:
        path = relative(name)
        source = root / path
        for parent in (source, *source.parents):
            if parent == root:
                break
            if parent.is_symlink():
                raise ValueError('Symlinks are not independent audit inputs: ' + name)
        if not source.exists():
            raise ValueError('Missing input: ' + name)
        for item in ([source] if source.is_file() else source.rglob('*')):
            if item.is_symlink():
                raise ValueError('Symlink in selected tree: ' + str(item))
            if item.is_file():
                key = str(item.relative_to(root))
                relative(key)
                if item.stat().st_size > 20_000_000:
                    raise ValueError('Input too large for this small-audit helper: ' + key)
                if key not in files:
                    total += item.stat().st_size
                    if total > 20_000_000:
                        raise ValueError('Selected inputs exceed 20 MB; use the project audit facilities')
                    files[key] = item.read_bytes()
    return files


def execute(python, directory, spec, probe, timeout):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONOPTIMIZE', None)
    payload = dict(imports=spec['imports'], runner=spec.get('runner', 'unittest'),
                   tests=spec['tests'], probe=probe)
    process = subprocess.Popen([python, '-B', '-c', BOOTSTRAP, json.dumps(payload)],
                               cwd=directory, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               start_new_session=True)
    timed_out = False
    output, characters = '', 0
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    deadline = time.monotonic() + timeout
    def append(chunk, final=False):
        nonlocal output, characters
        decoded = decoder.decode(chunk, final=final)
        characters += len(decoded)
        output = (output + decoded)[-12000:]

    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(process.args, timeout)
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 4096)
                    if not chunk:
                        append(b'', final=True)
                        selector.unregister(key.fileobj)
                    else:
                        append(chunk)
            process.wait(timeout=max(0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        timed_out = True
    finally:
        if timed_out or process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        process.stdout.close()
        process.wait()
    return dict(exit_code=process.returncode, timed_out=timed_out,
                output=output, output_truncated=characters > 12000)


def audit(root, spec, python=sys.executable, timeout=30, *, _baseline=None):
    root = Path(root).resolve()
    if not isinstance(spec, dict):
        raise ValueError('Audit recipe must be a JSON object')
    if os.name != 'posix':
        raise ValueError('This helper currently supports POSIX process cleanup only')
    if not 0 < timeout <= 300:
        raise ValueError('timeout must be between 0 and 300 seconds per check')
    for key in ('files', 'imports', 'tests'):
        value = spec.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
            raise ValueError(key + ' must be a nonempty string list')
    if spec.get('runner', 'unittest') not in ('unittest', 'pytest'):
        raise ValueError('Use unittest or the already installed pytest')
    if 'probe' in spec and not isinstance(spec['probe'], str):
        raise ValueError('probe must be Python assertion code')
    probe_when = spec.get('probe_when', 'always')
    if probe_when not in ('always', 'survives') or ('probe_when' in spec and 'probe' not in spec):
        raise ValueError('probe_when requires a probe and must be always or survives')
    target = str(relative(spec['target']))
    old, new = spec['old'], spec['new']
    if not isinstance(old, str) or not old or not isinstance(new, str) or old == new:
        raise ValueError('Mutation must replace nonempty text with different text')
    files = snapshot(root, spec['files'])
    modes = {name: (root / name).stat().st_mode & 0o777 for name in files}
    if target not in files:
        raise ValueError('Mutation target must be among selected input files')
    original = files[target].decode('utf-8')
    if original.count(old) != 1:
        raise ValueError('Mutation text must match exactly once')
    faulty = original.replace(old, new, 1).encode('utf-8')
    identity = (files, modes, spec['imports'], spec['tests'],
                spec.get('runner', 'unittest'), str(python), timeout, dict(os.environ))
    reused = _baseline is not None and _baseline.get('identity') == identity
    results = {}
    order = [('correct', 'tests'), ('correct', 'probe'), ('mutant', 'tests'), ('mutant', 'probe')]
    if probe_when == 'survives':
        order = [('correct', 'tests'), ('mutant', 'tests'), ('correct', 'probe'), ('mutant', 'probe')]
    skipped = None
    try:
        with tempfile.TemporaryDirectory(prefix='.con-artist-', dir=root) as scratch:
            for variant, check in order:
                if check == 'probe' and ('probe' not in spec or skipped is not None):
                    continue
                if variant == 'correct' and check == 'tests' and reused:
                    results['correct_tests'] = dict(_baseline['result'])
                    continue
                # Each check starts from the same inputs, not prior test side effects.
                directory = Path(scratch) / (variant + '-' + check)
                directory.mkdir()
                for name, content in files.items():
                    dest = directory / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(faulty if variant == 'mutant' and name == target else content)
                    dest.chmod(modes[name])
                result = execute(str(python), directory, spec,
                                 spec.get('probe') if check == 'probe' else None, timeout)
                results[variant + '_' + check] = result
                if result['timed_out'] or (variant == 'correct' and result['exit_code'] != 0):
                    output = dict(status='incomplete', checks=results)
                    if reused:
                        output['correct_tests_reused'] = True
                    return output
                if variant == 'correct' and check == 'tests' and _baseline is not None:
                    _baseline.update(identity=identity, result=dict(result))
                if probe_when == 'survives' and variant == 'mutant' and check == 'tests' and result['exit_code'] != 0:
                    skipped = 'Mutant tests exited nonzero; inspect their failure before any coverage claim. Proposed probe was not validated.'
        output = dict(status='observed', checks=results,
                      limitation='Nonzero mutant exit is not automatically a killed behavioral fault; inspect the failure.')
        if skipped is not None:
            output['probe_skipped'] = skipped
        if reused:
            output['correct_tests_reused'] = True
        return output
    finally:
        changed = [name for name, content in files.items()
                   if not (root / name).is_file() or (root / name).is_symlink()
                   or (root / name).read_bytes() != content
                   or (root / name).stat().st_mode & 0o777 != modes[name]]
        if changed:
            raise RuntimeError('Selected originals changed during audit; not restored: ' + ', '.join(changed))


def audit_batch(root, spec, python=sys.executable, timeout=30):
    """Reuse a successful baseline only within this explicit local batch."""
    common_keys = {'files', 'imports', 'runner', 'tests', 'mutations'}
    fault_keys = {'target', 'old', 'new', 'probe', 'probe_when'}
    mutations = spec.get('mutations')
    if set(spec) - common_keys or not isinstance(mutations, list) or not 1 <= len(mutations) <= 8:
        raise ValueError('Batch requires shared files/imports/runner/tests and 1–8 mutations')
    for fault in mutations:
        if not isinstance(fault, dict) or set(fault) - fault_keys or not {'target', 'old', 'new'} <= set(fault):
            raise ValueError('Each mutation requires target/old/new and optional probe/probe_when')
    common = {key: value for key, value in spec.items() if key != 'mutations'}
    baseline, observations = {}, []
    baseline_index = None
    for fault in mutations:
        result = audit(root, dict(common, **fault), python, timeout, _baseline=baseline)
        if result.get('correct_tests_reused'):
            # The complete observation is already in this response. Do not send
            # the same potentially 12 KB log once per fault or imply fresh runs.
            check = result['checks']['correct_tests']
            result['checks']['correct_tests'] = dict(
                exit_code=check['exit_code'], timed_out=check['timed_out'],
                observation_ref=f'#/audits/{baseline_index}/checks/correct_tests')
        else:
            baseline_index = len(observations)
        observations.append(result)
        if result['status'] != 'observed':
            break
    return dict(status=observations[-1]['status'], audits=observations,
                limitation='Shared successful baseline is one observation, not repeated evidence; external state and flakiness are not controlled.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, required=True, help='JSON recipe file, or - for stdin; see references/python-audit.md')
    parser.add_argument('--source', type=Path, default=Path.cwd())
    parser.add_argument('--python', default=sys.executable, help='Existing project interpreter; no dependency installation')
    parser.add_argument('--timeout', type=float, default=30, help='Seconds per check, at most 300')
    args = parser.parse_args()
    try:
        recipe = sys.stdin.read() if args.spec == Path('-') else args.spec.read_text()
        spec = json.loads(recipe)
        run = audit_batch if isinstance(spec, dict) and 'mutations' in spec else audit
        result = run(args.source, spec, args.python, args.timeout)
    except (ValueError, KeyError, OSError, RuntimeError) as error:
        parser.exit(2, 'Audit not established: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'observed' else 2


if __name__ == '__main__':
    sys.exit(main())
