#!/usr/bin/env python3
"""Run one Python mutation audit in disposable copies, without editing inputs.

This is a test runner, not a security sandbox. Run only trusted local tests.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile


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
                               stderr=subprocess.STDOUT, text=True, start_new_session=True)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate()
    return dict(exit_code=process.returncode, timed_out=timed_out,
                output=output[-12000:], output_truncated=len(output) > 12000)


def audit(root, spec, python=sys.executable, timeout=30):
    root = Path(root).resolve()
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
    target = str(relative(spec['target']))
    old, new = spec['old'], spec['new']
    if not isinstance(old, str) or not old or not isinstance(new, str) or old == new:
        raise ValueError('Mutation must replace nonempty text with different text')
    files = snapshot(root, spec['files'])
    if target not in files:
        raise ValueError('Mutation target must be among selected input files')
    original = files[target].decode('utf-8')
    if original.count(old) != 1:
        raise ValueError('Mutation text must match exactly once')
    faulty = original.replace(old, new, 1).encode('utf-8')
    results = {}
    try:
        with tempfile.TemporaryDirectory(prefix='.con-artist-', dir=root) as scratch:
            for variant in ('correct', 'mutant'):
                for check in ('tests', 'probe'):
                    if check == 'probe' and 'probe' not in spec:
                        continue
                    # Each check starts from the same inputs, not prior test side effects.
                    directory = Path(scratch) / (variant + '-' + check)
                    directory.mkdir()
                    for name, content in files.items():
                        dest = directory / name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(faulty if variant == 'mutant' and name == target else content)
                    result = execute(str(python), directory, spec,
                                     spec.get('probe') if check == 'probe' else None, timeout)
                    results[variant + '_' + check] = result
                    if result['timed_out'] or (variant == 'correct' and result['exit_code'] != 0):
                        return dict(status='incomplete', checks=results)
        return dict(status='observed', checks=results,
                    limitation='Nonzero mutant exit is not automatically a killed behavioral fault; inspect the failure.')
    finally:
        changed = [name for name, content in files.items()
                   if not (root / name).is_file() or (root / name).is_symlink()
                   or (root / name).read_bytes() != content]
        if changed:
            raise RuntimeError('Selected originals changed during audit; not restored: ' + ', '.join(changed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, required=True, help='JSON audit recipe; see references/python-audit.md')
    parser.add_argument('--source', type=Path, default=Path.cwd())
    parser.add_argument('--python', default=sys.executable, help='Existing project interpreter; no dependency installation')
    parser.add_argument('--timeout', type=float, default=30, help='Seconds per check, at most 300')
    args = parser.parse_args()
    try:
        result = audit(args.source, json.loads(args.spec.read_text()), args.python, args.timeout)
    except (ValueError, KeyError, OSError, RuntimeError) as error:
        parser.exit(2, 'Audit not established: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'observed' else 2


if __name__ == '__main__':
    sys.exit(main())
