#!/usr/bin/env python3
"""Compare committed Python implementations with frozen working-tree tests.

Trusted local tests only. This is not a security sandbox.
"""
import argparse
import codecs
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import time


BOOTSTRAP = '''import importlib, json, pathlib, runpy, sys
recipe = json.loads(sys.argv[1])
root = pathlib.Path.cwd().resolve()
sys.path.insert(0, str(root))
for name in recipe['imports']:
    module = importlib.import_module(name)
    location = getattr(module, '__file__', None)
    if not location or not pathlib.Path(location).resolve().is_relative_to(root):
        raise RuntimeError('Import escaped comparison copy: ' + name)
    print('Verified copied import:', name, flush=True)
sys.argv = [recipe['runner']] + recipe['tests']
runpy.run_module(recipe['runner'], run_name='__main__', alter_sys=True)
'''


def checked_path(name):
    if not isinstance(name, str):
        raise ValueError('Expected a project-relative file')
    path = Path(name)
    if not name or str(path) != name or path.is_absolute() or path == Path('.') or any(p in ('.git', '..') for p in path.parts):
        raise ValueError('Expected a project-relative file')
    return path


def git(root, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES'):
        env.pop(key, None)
    result = subprocess.run(['git', '--no-pager', '--literal-pathspecs', '-c', 'core.fsmonitor=false', '-C', str(root), *args],
                            env=env, capture_output=True, timeout=20)
    if result.returncode:
        raise ValueError('Git could not resolve a requested local revision or file')
    return result.stdout


def run_check(python, root, recipe, timeout):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONOPTIMIZE', None)
    process = subprocess.Popen([str(python), '-B', '-c', BOOTSTRAP, json.dumps(recipe)],
        cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, start_new_session=True)
    deadline = time.monotonic() + timeout
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    output, size, timed_out = '', 0, False
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(process.args, timeout)
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 4096)
                    text = decoder.decode(chunk, final=not chunk)
                    size += len(text)
                    output = (output + text)[-12000:]
                    if not chunk:
                        selector.unregister(key.fileobj)
            process.wait(timeout=max(0, deadline-time.monotonic()))
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
                output=output, output_truncated=size > 12000)


def compare(root, recipe, python=sys.executable, timeout=30):
    root = Path(root).resolve(strict=True)
    if os.name != 'posix' or not 0 < timeout <= 300:
        raise ValueError('Requires POSIX and a timeout in (0, 300]')
    if not isinstance(recipe, dict) or set(recipe) != {'fixed', 'vary', 'before', 'after', 'imports', 'runner', 'tests'}:
        raise ValueError('Recipe requires fixed, vary, before, after, imports, runner and tests')
    for key in ('fixed', 'vary', 'imports', 'tests'):
        if not isinstance(recipe[key], list) or not recipe[key] or not all(isinstance(v, str) and v for v in recipe[key]):
            raise ValueError(key + ' must be a nonempty string list')
    if recipe['runner'] not in ('unittest', 'pytest'):
        raise ValueError('Use unittest or installed pytest')
    names = recipe['fixed'] + recipe['vary']
    if len(set(names)) != len(names):
        raise ValueError('fixed and vary must be unique and disjoint')
    if Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != root:
        raise ValueError('source must be the repository root')
    originals, modes = {}, {}
    for name in names:
        path = root / checked_path(name)
        if any(p.is_symlink() for p in [path, *path.parents] if root in p.parents):
            raise ValueError('Symlink inputs are unsupported')
        if not path.is_file() or path.stat().st_size > 20_000_000:
            raise ValueError('Input missing or exceeds 20 MB')
        originals[name] = path.read_bytes()
        modes[name] = path.stat().st_mode & 0o777
    total = sum(map(len, originals.values()))
    if total > 20_000_000:
        raise ValueError('Inputs exceed 20 MB')
    variants, revisions = {}, {}
    for label in ('before', 'after'):
        ref = recipe[label]
        if not isinstance(ref, str) or not ref or ref.startswith('-') or '\n' in ref:
            raise ValueError('Invalid revision')
        sha = git(root, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
        revisions[label] = sha
        files = dict(originals)
        variant_modes = dict(modes)
        for name in recipe['vary']:
            # Literal pathspec prevents filenames being treated as globs.
            entry = git(root, 'ls-tree', '-z', sha, '--', name).rstrip(b'\0')
            if not entry:
                raise ValueError('Implementation missing at requested revision')
            metadata, recorded_name = entry.split(b'\t', 1)
            mode, kind, oid = metadata.split()
            if kind != b'blob' or mode not in (b'100644', b'100755') or recorded_name.decode() != name:
                raise ValueError('Implementation must be a regular Git file')
            length = int(git(root, 'cat-file', '-s', oid.decode()))
            total += length
            if total > 20_000_000:
                raise ValueError('Comparison snapshots exceed 20 MB')
            files[name] = git(root, 'cat-file', 'blob', oid.decode())
            variant_modes[name] = 0o755 if mode == b'100755' else 0o644
        variants[label] = (files, variant_modes)
    result = dict(status='observed', revisions=revisions, checks={},
                  fixed_sha256={name: hashlib.sha256(originals[name]).hexdigest() for name in recipe['fixed']},
                  limitation='Inspect assertion failures and import provenance; exit codes alone do not prove the fix.')
    try:
        with tempfile.TemporaryDirectory(prefix='.receipt-', dir=root) as scratch:
            for label, (files, file_modes) in variants.items():
                directory = Path(scratch) / label
                directory.mkdir()
                for name, content in files.items():
                    target = directory / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                    target.chmod(file_modes[name])
                check = run_check(python, directory, recipe, timeout)
                result['checks'][label] = check
                if check['timed_out']:
                    result['status'] = 'incomplete'
                    break
        return result
    finally:
        changed = [name for name, content in originals.items() if (root/name).is_symlink()
                   or not (root/name).is_file() or (root/name).read_bytes() != content]
        if changed:
            raise RuntimeError('Selected originals changed; not restored: ' + ', '.join(changed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', required=True, help='JSON file or - for stdin')
    parser.add_argument('--source', default='.')
    parser.add_argument('--python', default=sys.executable)
    parser.add_argument('--timeout', type=float, default=30)
    args = parser.parse_args()
    try:
        if args.spec == '-':
            raw = sys.stdin.read(1_000_001)
        else:
            with open(args.spec, encoding='utf-8') as stream:
                raw = stream.read(1_000_001)
        if len(raw.encode('utf-8')) > 1_000_000:
            raise ValueError('Recipe exceeds 1 MB')
        result = compare(args.source, json.loads(raw), args.python, args.timeout)
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        parser.exit(2, 'Comparison not established: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'observed' else 2


if __name__ == '__main__':
    sys.exit(main())
