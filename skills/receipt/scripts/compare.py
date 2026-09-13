#!/usr/bin/env python3
"""Compare committed or uncommitted Python fixes with frozen working-tree tests.

Trusted local tests only. This is not a security sandbox.
"""
import argparse
import codecs
import hashlib
import io
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import stat
import sys
import tempfile
import time

MAX_FIXED_ENTRIES = 10_000

BOOTSTRAP = '''import importlib, json, pathlib, runpy, sys, traceback
recipe = json.loads(sys.argv[1])
root = pathlib.Path.cwd().resolve()
sys.path.insert(0, str(root))
try:
    for name in recipe['imports']:
        module = importlib.import_module(name)
        location = getattr(module, '__file__', None)
        if not location or not pathlib.Path(location).resolve().is_relative_to(root):
            raise RuntimeError('Import escaped comparison copy: ' + name)
        print('Verified copied import:', name, flush=True)
except BaseException:
    traceback.print_exc()
    raise SystemExit(7)
sys.argv = [recipe['runner']] + recipe['tests']
if recipe['runner'] == 'unittest':
    import unittest
    result = unittest.main(module=None, exit=False).result
    if not result.wasSuccessful():
        raise SystemExit(1)
    if result.testsRun == len(result.skipped):
        print('No non-skipped unittest tests ran; this is not passing regression evidence.', flush=True)
        raise SystemExit(5)
    raise SystemExit(0)
runpy.run_module(recipe['runner'], run_name='__main__', alter_sys=True)
'''


def checked_path(name):
    if not isinstance(name, str):
        raise ValueError('Expected a project-relative file')
    path = Path(name)
    if not name or str(path) != name or path.is_absolute() or path == Path('.') or any(p in ('.git', '..') for p in path.parts):
        raise ValueError('Expected a project-relative file')
    return path


def fixed_files(root, selections):
    """Expand explicit working-tree support directories without following links."""
    files, visited = [], 0
    for name in selections:
        relative = checked_path(name)
        path = root / relative
        if any(p.is_symlink() for p in [path, *path.parents] if root in p.parents):
            raise ValueError('Symlink inputs are unsupported')
        pending, selected = [path], []
        while pending:
            item = pending.pop()
            visited += 1
            if visited > MAX_FIXED_ENTRIES:
                raise ValueError('Fixed selections exceed 10000 filesystem entries')
            relative = checked_path(item.relative_to(root).as_posix())
            info = item.lstat()
            if stat.S_ISLNK(info.st_mode):
                raise ValueError('Symlink inputs are unsupported')
            if stat.S_ISDIR(info.st_mode):
                populated = False
                with os.scandir(item) as entries:
                    for entry in entries:
                        populated = True
                        if visited + len(pending) >= MAX_FIXED_ENTRIES:
                            raise ValueError('Fixed selections exceed 10000 filesystem entries')
                        pending.append(Path(entry.path))
                if not populated:
                    raise ValueError('Empty fixed directories are unsupported')
            elif stat.S_ISREG(info.st_mode):
                selected.append(relative.as_posix())
            else:
                raise ValueError('Fixed inputs must be regular files or directories')
        if not selected:
            raise ValueError('Fixed directory contains no regular files')
        files.extend(sorted(selected))
    if len(files) != len(set(files)):
        raise ValueError('Fixed selections overlap')
    return files


def git(root, *args, input=None):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES'):
        env.pop(key, None)
    result = subprocess.run(['git', '--no-pager', '--literal-pathspecs', '-c', 'core.fsmonitor=false', '-C', str(root), *args],
                            env=env, input=input, capture_output=True, timeout=20)
    if result.returncode:
        raise ValueError('Git could not resolve a requested local revision or file')
    return result.stdout


def run_check(python, root, recipe, timeout):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(root),
               TMP=str(root), TEMP=str(root))
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
        pending_error = sys.exc_info()[0]
        if timed_out or process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        process.stdout.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired as error:
            if pending_error is None:
                raise RuntimeError('Child exit unconfirmed after 5-second cleanup wait; comparison not established') from error
            # Preserve the original interruption/error rather than replacing it.
    return dict(exit_code=process.returncode, timed_out=timed_out,
                output=output, output_truncated=size > 12000)


def read_limited(path, limit):
    with path.open('rb') as stream:
        return stream.read(limit + 1)


def compare(root, recipe, python=sys.executable, timeout=30):
    root = Path(root).resolve(strict=True)
    if os.name != 'posix' or not 0 < timeout <= 300:
        raise ValueError('Requires POSIX and a timeout in (0, 300]')
    required = {'fixed', 'vary', 'before', 'after', 'imports', 'runner', 'tests'}
    if not isinstance(recipe, dict) or not required <= set(recipe) or set(recipe) - required - {'watch'}:
        raise ValueError('Recipe requires fixed, vary, before, after, imports, runner and tests')
    if 'watch' in recipe and (not isinstance(recipe['watch'], list)
                            or not all(isinstance(v, str) and v for v in recipe['watch'])):
        raise ValueError('watch must be a list of project-relative selections')
    for key in ('fixed', 'vary', 'imports', 'tests'):
        if not isinstance(recipe[key], list) or not recipe[key] or not all(isinstance(v, str) and v for v in recipe[key]):
            raise ValueError(key + ' must be a nonempty string list')
    if recipe['runner'] not in ('unittest', 'pytest'):
        raise ValueError('Use unittest or installed pytest')
    recipe = dict(recipe, fixed=fixed_files(root, recipe['fixed']))
    watched = fixed_files(root, recipe.get('watch', []))
    names = recipe['fixed'] + recipe['vary']
    if len(set(names + watched)) != len(names + watched):
        raise ValueError('fixed, vary and watch must be unique and disjoint')
    if Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != root:
        raise ValueError('source must be the repository root')
    originals, modes = {}, {}
    total = 0
    for name in names + watched:
        path = root / checked_path(name)
        if any(p.is_symlink() for p in [path, *path.parents] if root in p.parents):
            raise ValueError('Symlink inputs are unsupported')
        if not path.is_file():
            raise ValueError('Input missing or exceeds 20 MB')
        length = path.stat().st_size
        if length > 20_000_000:
            raise ValueError('Input missing or exceeds 20 MB')
        if total + length > 20_000_000:
            raise ValueError('Inputs exceed 20 MB')
        originals[name] = read_limited(path, 20_000_000 - total)
        total += len(originals[name])
        if total > 20_000_000:
            raise ValueError('Inputs exceed 20 MB')
        modes[name] = path.stat().st_mode & 0o777
    variants, revisions = {}, {}
    varying_names = set(recipe['vary'])
    blobs = {}  # Immutable object content; never reuse mutable working inputs.
    for label in ('before', 'after'):
        ref = recipe[label]
        if (label == 'after' and isinstance(ref, dict) and set(ref) == {'working_tree'}
                and ref['working_tree'] is True):
            revisions[label] = None
            variants[label] = ({name: originals[name] for name in names},
                               {name: modes[name] for name in names})
            continue
        if not isinstance(ref, str) or not ref or ref.startswith('-') or '\n' in ref:
            raise ValueError('Invalid revision')
        sha = git(root, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
        revisions[label] = sha
        files = {name: originals[name] for name in names}
        variant_modes = {name: modes[name] for name in names}
        # One literal-path tree query per revision, not one process per file.
        tree = git(root, 'ls-tree', '-l', '-z', sha, '--', *recipe['vary'])
        entries = {}
        for entry in tree.split(b'\0'):
            if not entry:
                continue
            metadata, recorded_name = entry.split(b'\t', 1)
            name = recorded_name.decode()
            if name in entries or name not in varying_names:
                raise ValueError('Ambiguous historical file selection')
            entries[name] = metadata.split()
        missing = {}
        for name in recipe['vary']:
            if name not in entries:
                raise ValueError('Implementation missing at requested revision')
            mode, kind, oid, size = entries[name]
            if kind != b'blob' or mode not in (b'100644', b'100755'):
                raise ValueError('Implementation must be a regular Git file')
            length = int(size)
            total += length
            if total > 20_000_000:
                raise ValueError('Comparison snapshots exceed 20 MB')
            if oid not in blobs:
                missing[oid] = length
        if missing:
            # Request only size-checked immutable objects, not paths or revisions.
            stream = io.BytesIO(git(root, 'cat-file', '--batch',
                                   input=b''.join(oid + b'\n' for oid in missing)))
            for oid, length in missing.items():
                if stream.readline().split() != [oid, b'blob', str(length).encode()]:
                    raise ValueError('Unexpected historical blob header')
                content = stream.read(length)
                if len(content) != length or stream.read(1) != b'\n':
                    raise ValueError('Incomplete historical blob')
                blobs[oid] = content
            if stream.read(1):
                raise ValueError('Unexpected historical blob data')
        for name in recipe['vary']:
            mode, kind, oid, size = entries[name]
            files[name] = blobs[oid]
            variant_modes[name] = 0o755 if mode == b'100755' else 0o644
        variants[label] = (files, variant_modes)
    result = dict(status='observed', revisions=revisions, checks={},
                  fixed_sha256={name: hashlib.sha256(originals[name]).hexdigest() for name in recipe['fixed']},
                  limitation='Inspect assertion failures and import provenance; exit codes alone do not prove the fix.')
    if revisions['after'] is None:
        result['working_tree_after'] = dict(
            sha256={name: hashlib.sha256(originals[name]).hexdigest() for name in recipe['vary']},
            modes={name: modes[name] for name in recipe['vary']})
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
                if check['timed_out'] or check['exit_code'] == 7:
                    result['status'] = 'incomplete'
                    break
    finally:
        changed = [name for name, content in originals.items() if (root/name).is_symlink()
                   or not (root/name).is_file() or read_limited(root/name, len(content)) != content
                   or (root/name).stat().st_mode & 0o777 != modes[name]]
        if changed:
            raise RuntimeError('Selected originals changed; not restored: ' + ', '.join(changed))
    result['originals'] = dict(unchanged=True,
        sha256={name: hashlib.sha256(content).hexdigest() for name, content in originals.items()},
        modes=modes, watch_only=watched)
    result['comparison_copies_removed'] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Recipe example (adapt paths, revisions and tests to the project):
{"fixed":["test_rule.py"],"vary":["rule.py"],"before":"HEAD^","after":"HEAD","imports":["rule"],"runner":"unittest","tests":["-v","test_rule"]}

fixed: current tests/data/config/dependencies; files or explicit directories.
vary: implementation files. Paths are project-relative and disjoint.
watch (optional): originals to check but not copy or execute; files/directories.
before: commit expression. after: commit expression or {"working_tree":true}.
Working-tree after freezes current bytes/modes once, not the index or a commit.
imports: modules that must load inside each copy. runner: unittest or pytest.
Use --spec - to send JSON on stdin; no recipe file is required.
Directory inputs include hidden files; select only needed, authorized support.
No root, symlink, Git-internal, empty-directory or overlapping selections.
Limits: Python 3.9+/POSIX, 20 MB snapshot, 10000 entries, 12000 output characters.
Exit 0 means observations collected, not a verified fix: inspect each check's
assertion output, exit_code, timed_out, output_truncated and import provenance.
Exit 2 means comparison not established. Copies are cleaned; selected originals
are checked, not restored. No sandbox or complete side-effect containment.
Check exit 7 reserves incomplete import/setup evidence; no next comparison runs.
Child temp defaults use each copy; do not redirect the helper's global TMPDIR.
''')
    parser.add_argument('--spec', required=True, help='JSON file or - for stdin')
    parser.add_argument('--source', default='.', help='Git project root (default: current directory)')
    parser.add_argument('--python', default=sys.executable, help='Check interpreter (default: this Python)')
    parser.add_argument('--timeout', type=float, default=30,
                        help='Seconds per check, >0 and <=300 (default: 30); cleanup may wait 5 more')
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
