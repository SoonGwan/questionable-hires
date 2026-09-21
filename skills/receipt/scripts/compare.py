#!/usr/bin/env python3
"""Compare committed or uncommitted fixes with frozen working-tree tests.

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
MAX_GUARD_BYTES = 20_000_000

NODE_OBSERVER = '''import { registerHooks } from 'node:module';
import { createHash } from 'node:crypto';
const selected = new Set(JSON.parse(process.env.RECEIPT_NODE_MODULE_URLS));
registerHooks({load(url, context, nextLoad) {
  const result = nextLoad(url, context);
  if (selected.has(url)) {
    const hash = result.source == null ? null : createHash('sha256').update(result.source).digest('hex');
    console.error('Receipt copied load: ' + JSON.stringify({url, pid: process.pid, sha256: hash}));
  }
  return result;
}});
'''

MODULE_BINDINGS = '''def verify_module_bindings(recipe, root):
    for selector, relative in recipe.get('module_bindings', {}).items():
        name, attributes = selector.split(':')
        module = importlib.import_module(name)
        for attribute in attributes.split('.'):
            if not isinstance(module, types.ModuleType):
                raise RuntimeError('Expected module binding: ' + selector)
            module = vars(module).get(attribute)
        if not isinstance(module, types.ModuleType):
            raise RuntimeError('Expected module binding: ' + selector)
        location = vars(module).get('__file__')
        expected = (root / relative).resolve(strict=True)
        if (not expected.is_relative_to(root) or not location
                or pathlib.Path(location).resolve(strict=True) != expected):
            raise RuntimeError('Module binding path mismatch: ' + selector)
        print('Verified copied module binding:', selector, json.dumps({
            'path': str(expected), 'pid': os.getpid()
        }), flush=True)
'''


BOOTSTRAP = '''import importlib, json, os, pathlib, sys, traceback, types
''' + MODULE_BINDINGS + '''
recipe = json.loads(sys.argv[1])
root = pathlib.Path.cwd().resolve()
sys.path[:0] = [str(root / name) for name in recipe.get('import_roots', [])] + [str(root)]
def verify_imports():
    for name in recipe['imports']:
        module = importlib.import_module(name)
        location = getattr(module, '__file__', None)
        if not location or not pathlib.Path(location).resolve().is_relative_to(root):
            raise RuntimeError('Import escaped comparison copy: ' + name)
        print('Verified copied import:', name, json.dumps({
            'path': str(pathlib.Path(location).resolve()), 'pid': os.getpid()
        }), flush=True)
    verify_module_bindings(recipe, root)
sys.argv = [recipe['runner']] + recipe['tests']
if recipe['runner'] == 'pytest':
    import pytest
    class CopiedImports:
        ready = False
        def pytest_collection_finish(self, session):
            # Let native collection/configuration load tests with assertion
            # rewriting before checking the same process's module identities.
            try:
                verify_imports()
            except BaseException:
                traceback.print_exc()
                pytest.exit('Comparison import verification failed', returncode=7)
            self.ready = True
    probe = CopiedImports()
    code = pytest.main(recipe['tests'], plugins=[probe])
    if not probe.ready and code in (0, 1):
        print('Copied imports were not verified; comparison is incomplete.', flush=True)
        code = 7
    raise SystemExit(code)
try:
    verify_imports()
except BaseException:
    traceback.print_exc()
    raise SystemExit(7)
if recipe['runner'] == 'unittest':
    import unittest
    result = unittest.main(module=None, exit=False).result
    if not result.wasSuccessful():
        raise SystemExit(1)
    if result.testsRun == len(result.skipped):
        print('No non-skipped unittest tests ran; this is not passing regression evidence.', flush=True)
        raise SystemExit(5)
    raise SystemExit(0)
'''


NATIVE_STARTUP = '''import importlib, json, os, pathlib, site, sys, traceback, types
''' + MODULE_BINDINGS + '''
def _receipt_startup():
    global probe, root
    probe = pathlib.Path(__file__).resolve().parent
    root = probe.parent
    paths = [str(root / name) for name in recipe.get('import_roots', [])] + [str(root)]
    sys.path[:] = paths + [path for path in sys.path if path != str(probe) and path not in paths]
    # Child processes inherit copy lookup, not this one-process startup probe.
    os.environ['PYTHONPATH'] = os.pathsep.join(paths)
    try:
        # Remove only our temporary lookup/identity, then import the real hooks.
        # Keep the adapter identity when no real sitecustomize exists: Python's
        # in-progress outer import still requires that sys.modules entry.
        adapter = sys.modules.pop('sitecustomize')
        try:
            importlib.import_module('sitecustomize')
        except ImportError as error:
            if error.name != 'sitecustomize':
                raise
            sys.modules['sitecustomize'] = adapter
        if site.ENABLE_USER_SITE:
            try:
                importlib.import_module('usercustomize')
            except ImportError as error:
                if error.name != 'usercustomize':
                    raise
        # Python's following usercustomize import reuses the cached real module.
        # A Python-based launcher must not satisfy the native probe, but still
        # receives the original hooks instead of silently shadowing them.
        if sys.argv[:1] != ['-m']:
            return
        for name in recipe['imports']:
            module = importlib.import_module(name)
            location = getattr(module, '__file__', None)
            if not location or not pathlib.Path(location).resolve().is_relative_to(root):
                raise RuntimeError('Import escaped comparison copy: ' + name)
            print('Verified copied import:', name, json.dumps({
                'path': str(pathlib.Path(location).resolve()), 'pid': os.getpid()
            }), flush=True)
        verify_module_bindings(recipe, root)
        (probe / 'ready').write_bytes(b'ready')
    except BaseException:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(7)
_receipt_startup()
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
    args = [str(python), '-B', '-c', BOOTSTRAP, json.dumps(recipe)]
    marker = None
    if recipe.get('invocation', 'bootstrap') == 'module':
        for directory in [root, *(root / name for name in recipe.get('import_roots', []))]:
            if any((directory / name).exists() for name in
                   ('sitecustomize', 'sitecustomize.py', 'sitecustomize.pyc',
                    'usercustomize', 'usercustomize.py', 'usercustomize.pyc')):
                raise ValueError('Native invocation does not replace project startup customization')
        probe = Path(tempfile.mkdtemp(prefix='.receipt-startup-', dir=root))
        (probe / 'sitecustomize.py').write_text('recipe = ' + repr(recipe) + '\n' + NATIVE_STARTUP)
        marker = probe / 'ready'
        env['PYTHONPATH'] = os.pathsep.join([str(probe), *(str(root / name) for name in recipe.get('import_roots', [])), str(root)])
        args = [str(python), '-B', '-m', recipe['runner'], *recipe['tests']]
    result = capture_check(args, root, env, timeout)
    if marker is not None:
        ready = marker.is_file() and not marker.is_symlink() and read_limited(marker, 5) == b'ready'
        result.update(command=args, invocation='module', provenance_ready=ready,
                      native_exit_code=result['exit_code'])
        if not ready and not result['timed_out']:
            result['exit_code'] = 7
    return result


def capture_check(args, root, env, timeout):
    """Shared bounded foreground execution; callers interpret native evidence."""
    process = subprocess.Popen(args,
        cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, start_new_session=True)
    deadline = time.monotonic() + timeout
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    output, size, timed_out = '', 0, False
    group_stopped = False
    def stop_group():
        nonlocal group_stopped
        if not group_stopped:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            group_stopped = True
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                if process.poll() is not None:
                    # Native runner finished; idle descendants must not turn
                    # its captured failure into a wrapper timeout.
                    stop_group()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(process.args, timeout)
                for key, _ in selector.select(min(remaining, 0.05)):
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
        stop_group()
        process.stdout.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired as error:
            if pending_error is None:
                raise RuntimeError('Child exit unconfirmed after 5-second cleanup wait; comparison not established') from error
            # Preserve the original interruption/error rather than replacing it.
    result = dict(exit_code=process.returncode, timed_out=timed_out,
                  output=output, output_truncated=size > 12000)
    return result


def run_node_check(node, root, recipe, timeout):
    # Do not pre-import application code: observe the native test's own loads.
    probe = Path(tempfile.mkdtemp(prefix='.receipt-node-', dir=root))
    hook = probe / 'observe.mjs'
    hook.write_text(NODE_OBSERVER, encoding='utf-8')
    expected = {(root / name).as_uri(): hashlib.sha256((root / name).read_bytes()).hexdigest()
                for name in recipe['imports']}
    env = dict(os.environ, TMPDIR=str(root), TMP=str(root), TEMP=str(root),
               RECEIPT_NODE_MODULE_URLS=json.dumps(list(expected)))
    args = [str(node), '--test', '--test-reporter=tap', '--import', str(hook),
            *(str(root / name) for name in recipe['tests'])]
    result = capture_check(args, root, env, timeout)
    loads, malformed = [], False
    for line in result['output'].splitlines():
        prefix = 'Receipt copied load: '
        if prefix not in line:
            continue
        try:
            record = json.loads(line.split(prefix, 1)[1])
            if (not isinstance(record, dict) or record.get('url') not in expected
                    or record.get('sha256') != expected[record['url']]
                    or type(record.get('pid')) is not int or record['pid'] <= 0):
                malformed = True
            else:
                loads.append(record)
        except (ValueError, TypeError):
            malformed = True
    ready = (not malformed and not result['output_truncated']
             and {record['url'] for record in loads} == set(expected))
    result.update(command=args, invocation='node-test', native_exit_code=result['exit_code'],
                  provenance_ready=ready, copied_loads=loads,
                  provenance_limitation='Loader results only; not successful evaluation, dispatch or test coverage.')
    if not ready and not result['timed_out']:
        result['exit_code'] = 7
    return result


def read_limited(path, limit):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('Selected input must be a regular file')
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino, opened.st_mode)
                != (info.st_dev, info.st_ino, info.st_mode)):
            raise ValueError('Selected input changed while opening')
        return stream.read(limit + 1)


def tree_inventory(root):
    """Bounded read-only inventory; record links, never their target contents."""
    inventory, pending, total = {}, [root], 0
    while pending:
        path = pending.pop()
        name = path.relative_to(root).as_posix()
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if len(inventory) >= MAX_FIXED_ENTRIES:
            raise ValueError('Tree guard exceeds 10000 entries')
        if stat.S_ISLNK(info.st_mode):
            inventory[name] = ('symlink', mode, os.readlink(path))
        elif stat.S_ISDIR(info.st_mode):
            inventory[name] = ('directory', mode)
            with os.scandir(path) as entries:
                for entry in entries:
                    if len(inventory) + len(pending) >= MAX_FIXED_ENTRIES:
                        raise ValueError('Tree guard exceeds 10000 entries')
                    pending.append(Path(entry.path))
        elif stat.S_ISREG(info.st_mode):
            if info.st_size > MAX_GUARD_BYTES - total:
                raise ValueError('Tree guard exceeds 20 MB per inventory')
            digest = hashlib.sha256()
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(descriptor, 'rb') as stream:
                opened = os.fstat(stream.fileno())
                if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                    raise ValueError('Tree guard file changed while opening')
                while True:
                    chunk = stream.read(min(65536, MAX_GUARD_BYTES - total + 1))
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_GUARD_BYTES:
                        raise ValueError('Tree guard exceeds 20 MB per inventory')
                    digest.update(chunk)
            inventory[name] = ('file', mode, digest.hexdigest())
        else:
            raise ValueError('Tree guard supports only files, directories and symlinks')
    return inventory, total


def compare(root, recipe, python=sys.executable, timeout=30, *, node='node'):
    root = Path(root).resolve(strict=True)
    if os.name != 'posix' or not 0 < timeout <= 300:
        raise ValueError('Requires POSIX and a timeout in (0, 300]')
    required = {'fixed', 'vary', 'before', 'after', 'imports', 'runner', 'tests'}
    if not isinstance(recipe, dict) or not required <= set(recipe) or set(recipe) - required - {'watch', 'import_roots', 'guard_tree', 'invocation', 'module_bindings'}:
        raise ValueError('Recipe requires fixed, vary, before, after, imports, runner and tests')
    if type(recipe.get('guard_tree', False)) is not bool:
        raise ValueError('guard_tree must be a boolean')
    if 'watch' in recipe and (not isinstance(recipe['watch'], list)
                            or not all(isinstance(v, str) and v for v in recipe['watch'])):
        raise ValueError('watch must be a list of project-relative selections')
    for key in ('fixed', 'vary', 'imports', 'tests'):
        if not isinstance(recipe[key], list) or not recipe[key] or not all(isinstance(v, str) and v for v in recipe[key]):
            raise ValueError(key + ' must be a nonempty string list')
    if recipe['runner'] not in ('unittest', 'pytest', 'node'):
        raise ValueError('Use unittest, installed pytest or native node')
    if recipe['runner'] == 'node':
        if any(key in recipe for key in ('invocation', 'import_roots', 'module_bindings')):
            raise ValueError('Node does not support Python invocation/import options')
        if any(os.environ.get(key) for key in ('NODE_OPTIONS', 'NODE_PATH', 'NODE_COMPILE_CACHE')):
            raise ValueError('Node custom startup/search/cache settings require project-native comparison')
    if recipe.get('invocation', 'bootstrap') not in ('bootstrap', 'module'):
        raise ValueError('invocation must be bootstrap or module')
    if recipe.get('invocation') == 'module' and recipe['runner'] != 'unittest':
        raise ValueError('Native module invocation currently supports unittest only')
    recipe = dict(recipe, fixed=fixed_files(root, recipe['fixed']))
    watched = fixed_files(root, recipe.get('watch', []))
    names = recipe['fixed'] + recipe['vary']
    if recipe['runner'] == 'node':
        for key in ('imports', 'tests'):
            if len(set(recipe[key])) != len(recipe[key]):
                raise ValueError('Node ' + key + ' must be unique selected file paths')
            for name in recipe[key]:
                path = checked_path(name)
                selected = recipe['fixed'] if key == 'tests' else names
                if name not in selected or path.suffix not in ('.js', '.cjs', '.mjs'):
                    raise ValueError('Node ' + key + ' requires selected JS files, not flags/globs/module names')
    bindings = recipe.get('module_bindings', {})
    if not isinstance(bindings, dict) or len(bindings) > 100:
        raise ValueError('module_bindings must map at most 100 module:attribute selectors to selected paths')
    for selector, relative in bindings.items():
        if not isinstance(selector, str) or selector.count(':') != 1:
            raise ValueError('Expected a module:attribute binding selector')
        module, attribute = selector.split(':')
        if (module not in recipe['imports'] or not all(part.isidentifier() for part in module.split('.'))
                or not all(part.isidentifier() for part in attribute.split('.'))):
            raise ValueError('Module binding requires a declared import and dotted attribute identifiers')
        checked_path(relative)
        if relative not in names:
            raise ValueError('Module binding path must be a fixed or varying selected file')
    if len(set(names + watched)) != len(names + watched):
        raise ValueError('fixed, vary and watch must be unique and disjoint')
    import_roots = recipe.get('import_roots', [])
    if not isinstance(import_roots, list) or not all(isinstance(name, str) for name in import_roots):
        raise ValueError('import_roots must be a list of selected project-relative directories')
    roots = []
    for name in import_roots:
        relative = checked_path(name)
        if (relative in roots or not (root / relative).is_dir()
                or any(p.is_symlink() for p in [root / relative, *(root / relative).parents]
                       if root in p.parents)
                or not any(relative in Path(selected).parents for selected in names)):
            raise ValueError('Import root must be a distinct directory containing selected files: ' + name)
        roots.append(relative)
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
    result = dict(status='observed', revisions=revisions, checks={}, import_roots=list(import_roots),
                  fixed_sha256={name: hashlib.sha256(originals[name]).hexdigest() for name in recipe['fixed']},
                  limitation='Inspect assertion failures and import provenance; exit codes alone do not prove the fix.')
    if revisions['after'] is None:
        result['working_tree_after'] = dict(
            sha256={name: hashlib.sha256(originals[name]).hexdigest() for name in recipe['vary']},
            modes={name: modes[name] for name in recipe['vary']})
    guarded = tree_inventory(root) if recipe.get('guard_tree', False) else None
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
                check = (run_node_check(node, directory, recipe, timeout) if recipe['runner'] == 'node'
                         else run_check(python, directory, recipe, timeout))
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
        if guarded is not None:
            current, _ = tree_inventory(root)
            previous, byte_count = guarded
            differences = sorted(name for name in previous.keys() | current.keys()
                                 if previous.get(name) != current.get(name))
            if differences:
                raise RuntimeError('Project tree changed; not restored (' + str(len(differences))
                                   + ' paths): ' + ', '.join(differences[:20]))
            encoded = json.dumps(previous, sort_keys=True, separators=(',', ':')).encode()
            result['tree_guard'] = dict(unchanged=True, entries=len(previous),
                file_bytes=byte_count, inventory_sha256=hashlib.sha256(encoded).hexdigest(),
                scope='source root including Git metadata; symlink targets not read')
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
guard_tree (optional boolean): inventory all source entries including Git around
the comparison; no link traversal. 10000 entries/20 MB read per inventory. Opt in
only when whole-project preservation is requested and all source reads are allowed.
before: commit expression. after: commit expression or {"working_tree":true}.
Working-tree after freezes current bytes/modes once, not the index or a commit.
imports: modules that must load inside each copy. runner: unittest, pytest or node.
Node mode: imports are selected .js/.cjs/.mjs paths; tests are fixed JS paths,
not flags/globs. Runs node --test --test-reporter=tap with an observation preload.
Requires synchronous registerHooks; verified on Node 24.16.0. Custom NODE_OPTIONS,
NODE_PATH or NODE_COMPILE_CACHE and Python invocation/import options are rejected.
Node copied_loads record source hashes/PIDs, not evaluation or coverage; truncated
or missing provenance is incomplete. Use --node to select the project executable.
module_bindings (optional): {"test_loader:component":"plugin.py"} verifies a
module-valued attribute's exact selected path in the same test process. The base
module must be declared in imports. Not function identity or later dispatch proof.
Verified copied import lines include JSON path/pid from that native process at
import time; they do not prove later monkey-patching cannot change behavior.
invocation (optional): module runs Python -B -m unittest with these tests using
a temporary same-process startup probe; bootstrap is the existing default.
Module mode keeps native unittest exits; empty discovery can return 0 or 5
depending on Python, so inspect counts/skips. Missing provenance reserves check 7, CLI 2.
import_roots (optional): ordered selected directories, e.g. ["src"], prepended
inside each copy before its root. No package installation or inherited PYTHONPATH.
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
    parser.add_argument('--node', default='node', help='Node executable for runner=node (default: node)')
    parser.add_argument('--pretty', action='store_true',
                        help='Indent JSON for human reading; default is compact lossless JSON')
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
        result = compare(args.source, json.loads(raw), args.python, args.timeout, node=args.node)
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        parser.exit(2, 'Comparison not established: ' + str(error) + '\n')
    print(json.dumps(result, indent=2) if args.pretty else json.dumps(result, separators=(',', ':')))
    return 0 if result['status'] == 'observed' else 2


if __name__ == '__main__':
    sys.exit(main())
