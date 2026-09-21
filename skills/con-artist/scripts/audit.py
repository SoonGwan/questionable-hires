#!/usr/bin/env python3
"""Run one Python mutation audit in disposable copies, without editing inputs.

This is a test runner, not a security sandbox. Run only trusted local tests.
"""
import argparse
import codecs
import hashlib
import json
import os
from pathlib import Path
import signal
import selectors
import stat
import subprocess
import sys
import tempfile
import time

MAX_GUARD_ENTRIES = 10000
MAX_GUARD_BYTES = 20_000_000


def project_inventory(root):
    """Bounded hashes/modes including Git; link targets are never traversed."""
    inventory, pending, total = {}, [root], 0
    while pending:
        path = pending.pop()
        name = path.relative_to(root).as_posix()
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if len(inventory) >= MAX_GUARD_ENTRIES:
            raise ValueError('Project guard exceeds 10000 entries')
        if stat.S_ISLNK(info.st_mode):
            inventory[name] = ('symlink', mode, os.readlink(path))
        elif stat.S_ISDIR(info.st_mode):
            inventory[name] = ('directory', mode)
            with os.scandir(path) as entries:
                for entry in entries:
                    if len(inventory) + len(pending) >= MAX_GUARD_ENTRIES:
                        raise ValueError('Project guard exceeds 10000 entries')
                    pending.append(Path(entry.path))
        elif stat.S_ISREG(info.st_mode):
            if info.st_size > MAX_GUARD_BYTES - total:
                raise ValueError('Project guard exceeds 20 MB per inventory')
            digest = hashlib.sha256()
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(descriptor, 'rb') as stream:
                opened = os.fstat(stream.fileno())
                if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                    raise ValueError('Project guard file changed while opening')
                while True:
                    chunk = stream.read(min(65536, MAX_GUARD_BYTES - total + 1))
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_GUARD_BYTES:
                        raise ValueError('Project guard exceeds 20 MB per inventory')
                    digest.update(chunk)
            inventory[name] = ('file', mode, digest.hexdigest())
        else:
            raise ValueError('Project guard supports files, directories and symlinks only')
    return inventory, total


SETUP = '''import hashlib, importlib, json, pathlib, sys, traceback
root = pathlib.Path.cwd().resolve()
sys.path[:0] = [str(root / name) for name in spec['import_roots']] + [str(root)]
print('Copied process:', json.dumps({'python': sys.executable, 'cwd': str(root)}, separators=(',', ':')), flush=True)
def verify_setup():
    try:
        for name in spec['imports']:
            module = importlib.import_module(name)
            parts = name.split('.')
            for end in range(1, len(parts)):
                parent = '.'.join(parts[:end])
                if sys.modules.get(parent) is None:
                    raise RuntimeError('Incomplete package import: ' + name + ': missing ' + parent)
            location = getattr(module, '__file__', None)
            if not location or not pathlib.Path(location).resolve().is_relative_to(root):
                raise RuntimeError('Import escaped copy: ' + name + ': ' + str(location))
            location = pathlib.Path(location).resolve()
            print('Verified copied import:', name, json.dumps({
                'path': str(location.relative_to(root)),
                'sha256': hashlib.sha256(location.read_bytes()).hexdigest()
            }, separators=(',', ':')), flush=True)
    except BaseException:
        print('Import setup failed; not mutation evidence.', flush=True)
        traceback.print_exc()
        raise SystemExit(7)
    if spec.get('precheck'):
        try:
            exec(compile(spec['precheck'], '<audit-precheck>', 'exec'), {'__name__': '__audit_precheck__'})
        except BaseException:
            print('Precheck failed; not mutation evidence.', flush=True)
            traceback.print_exc()
            raise SystemExit(6)
        print('Precheck completed in check process.', flush=True)
'''

BOOTSTRAP = '''import json, sys
spec = json.loads(sys.argv[1])
''' + SETUP + '''
if spec['probe'] is None and spec['runner'] == 'pytest':
    sys.argv = [spec['runner']] + spec['tests']
    import pytest
    class CopiedSetup:
        ready = False
        def pytest_collection_finish(self, session):
            try:
                verify_setup()
            except SystemExit as error:
                pytest.exit('Audit setup incomplete', returncode=error.code)
            self.ready = True
    plugin = CopiedSetup()
    code = pytest.main(spec['tests'], plugins=[plugin])
    if not plugin.ready and code in (0, 1):
        print('Copied imports were not verified; audit is incomplete.', flush=True)
        code = 7
    raise SystemExit(code)
verify_setup()
if spec['probe'] is not None:
    sys.argv = ['audit-probe']
    exec(compile(spec['probe'], '<audit-probe>', 'exec'), {'__name__': '__main__'})
else:
    sys.argv = [spec['runner']] + spec['tests']
    if spec['runner'] == 'unittest':
        import unittest
        result = unittest.main(module=None, exit=False).result
        if not result.wasSuccessful():
            raise SystemExit(1)
        if result.testsRun == len(result.skipped):
            print('No non-skipped unittest tests ran; this is not passing audit evidence.', flush=True)
            raise SystemExit(5)
        raise SystemExit(0)
'''


def relative(name):
    path = Path(name)
    if not name or path.is_absolute() or any(p in ('.git', '..') for p in path.parts) or path == Path('.'):
        raise ValueError('Expected a project-relative file/directory: ' + str(name))
    return path


def read_selected(path, info, limit):
    """Read the inspected regular file, bounded even if it grows afterward."""
    flags = os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW
    with os.fdopen(os.open(path, flags), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino)
                or stat.S_IMODE(opened.st_mode) != stat.S_IMODE(info.st_mode)):
            raise ValueError('Selected input changed while opening')
        return stream.read(limit + 1)


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
                    remaining = 20_000_000 - total
                    inspected = item.stat()
                    if inspected.st_size > remaining:
                        raise ValueError('Selected inputs exceed 20 MB; use the project audit facilities')
                    # The file can grow after stat. Bound allocation and charge
                    # actual bytes, not the earlier size observation.
                    content = read_selected(item, inspected, remaining)
                    if len(content) > remaining:
                        raise ValueError('Selected inputs exceed 20 MB; use the project audit facilities')
                    total += len(content)
                    files[key] = content
    return files


def original_matches(path, content, mode):
    """Compare one selected input without unbounded reads of a changed file."""
    if not path.is_file() or path.is_symlink():
        return False
    status = path.stat()
    if status.st_size != len(content) or status.st_mode & 0o777 != mode:
        return False
    try:
        return read_selected(path, status, len(content)) == content
    except (OSError, ValueError):
        return False


def execute(python, directory, spec, probe, timeout):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONOPTIMIZE', None)
    payload = dict(imports=spec['imports'], runner=spec.get('runner', 'unittest'),
                   tests=spec['tests'], probe=probe, precheck=spec.get('precheck'),
                   import_roots=spec.get('import_roots', []))
    command = [python, '-B', '-c', BOOTSTRAP, json.dumps(payload)]
    marker = None
    if spec.get('invocation', 'bootstrap') == 'module':
        paths = [directory / name for name in payload['import_roots']] + [directory]
        for path in paths:
            if any((path / name).exists() for name in
                   ('sitecustomize', 'sitecustomize.py', 'sitecustomize.pyc',
                    'usercustomize', 'usercustomize.py', 'usercustomize.pyc')):
                raise ValueError('Module invocation does not replace project startup customization')
        adapter = Path(tempfile.mkdtemp(prefix='.audit-startup-', dir=directory))
        marker = adapter / 'result.json'
        startup = (Path(__file__).resolve().parent.parent / 'assets/unittest_startup.py').read_text()
        (adapter / 'sitecustomize.py').write_text(
            'spec = ' + repr(payload) + '\nsetup_source = ' + repr(SETUP) + '\n' + startup)
        env['PYTHONPATH'] = os.pathsep.join([str(adapter), *map(str, paths)])
        command = [python, '-B', '-m', 'unittest', *spec['tests']]
    process = subprocess.Popen(command,
                               cwd=directory, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               start_new_session=True)
    timed_out = False
    output, characters = '', 0
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    deadline = time.monotonic() + timeout
    group_stopped = False
    def stop_group():
        nonlocal group_stopped
        if not group_stopped:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            group_stopped = True
    def append(chunk, final=False):
        nonlocal output, characters
        decoded = decoder.decode(chunk, final=final)
        characters += len(decoded)
        output = (output + decoded)[-12000:]

    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                if process.poll() is not None:
                    # The foreground runner has finished; an inherited pipe
                    # must not turn its result into a deadline failure.
                    stop_group()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(process.args, timeout)
                for key, _ in selector.select(min(remaining, 0.05)):
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
        pending_error = sys.exc_info()[0]
        stop_group()
        process.stdout.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired as error:
            if pending_error is None:
                raise RuntimeError('Child exit unconfirmed after 5-second cleanup wait; audit not established') from error
            # Preserve an existing interruption/error; do not start another check.
    result = dict(exit_code=process.returncode, timed_out=timed_out,
                  output=output, output_truncated=characters > 12000)
    if marker is not None:
        evidence = None
        try:
            info = marker.lstat()
            evidence = json.loads(read_selected(marker, info, 2048))
            if (set(evidence) != {'tests', 'skipped', 'successful'}
                    or type(evidence['tests']) is not int or type(evidence['skipped']) is not int
                    or type(evidence['successful']) is not bool
                    or not 0 <= evidence['skipped'] <= evidence['tests']):
                evidence = None
        except (OSError, ValueError, TypeError):
            evidence = None
        result.update(command=command, invocation='module',
                      native_exit_code=process.returncode, suite_observation=evidence)
        if not timed_out:
            if evidence is None:
                result['exit_code'] = 7
            elif evidence['successful'] != (process.returncode == 0):
                result['exit_code'] = 7
                result['incomplete_reason'] = 'Native exit status disagrees with completed unittest result; inspect shutdown/runner behavior.'
            elif evidence['successful'] and evidence['tests'] == evidence['skipped']:
                result['exit_code'] = 5
    return result


def audit(root, spec, python=sys.executable, timeout=30, *, _baseline=None, _probe_baseline=None,
          _selection_baselines=None):
    root = Path(root).resolve()
    if not isinstance(spec, dict):
        raise ValueError('Audit recipe must be a JSON object')
    allowed = {'files', 'imports', 'runner', 'tests', 'target', 'old', 'new',
               'probe', 'probe_when', 'probe_files', 'probe_replacements', 'probe_tests', 'precheck', 'import_roots', 'guard_project', 'invocation'}
    unknown = set(spec) - allowed
    if unknown:
        raise ValueError('Unknown audit fields: ' + ', '.join(sorted(map(str, unknown))) +
                         '. Use CLI --timeout/--python for execution settings.')
    if os.name != 'posix':
        raise ValueError('This helper currently supports POSIX process cleanup only')
    if not isinstance(spec.get('guard_project', False), bool):
        raise ValueError('guard_project must be a boolean')
    if not 0 < timeout <= 300:
        raise ValueError('timeout must be between 0 and 300 seconds per check')
    for key in ('files', 'imports', 'tests'):
        value = spec.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
            raise ValueError(key + ' must be a nonempty string list')
    if spec.get('runner', 'unittest') not in ('unittest', 'pytest'):
        raise ValueError('Use unittest or the already installed pytest')
    if spec.get('invocation', 'bootstrap') not in ('bootstrap', 'module'):
        raise ValueError('invocation must be bootstrap or module')
    if spec.get('invocation') == 'module' and (spec.get('runner', 'unittest') != 'unittest' or 'probe' in spec):
        raise ValueError('Module invocation requires unittest and native probe files, not inline probes')
    if 'probe' in spec and not isinstance(spec['probe'], str):
        raise ValueError('probe must be Python assertion code')
    if 'precheck' in spec and not isinstance(spec['precheck'], str):
        raise ValueError('precheck must be Python assertion code')
    file_probe = any(key in spec for key in ('probe_files', 'probe_replacements', 'probe_tests'))
    if file_probe:
        if 'probe' in spec:
            raise ValueError('Use probe or native probe files/replacements, not both')
        if (not any(key in spec for key in ('probe_files', 'probe_replacements'))
                or any(key in spec and (not isinstance(spec[key], dict) or not spec[key])
                       for key in ('probe_files', 'probe_replacements'))
                or not isinstance(spec.get('probe_tests'), list) or not spec['probe_tests']
                or not all(isinstance(x, str) and x for x in spec['probe_tests'])):
            raise ValueError('Nonempty probe_files/probe_replacements and probe_tests are required together')
    has_probe = 'probe' in spec or file_probe
    probe_when = spec.get('probe_when', 'always')
    if probe_when not in ('always', 'survives') or ('probe_when' in spec and not has_probe):
        raise ValueError('probe_when requires a probe and must be always or survives')
    target = str(relative(spec['target']))
    old, new = spec['old'], spec['new']
    if not isinstance(old, str) or not old or not isinstance(new, str) or old == new:
        raise ValueError('Mutation must replace nonempty text with different text')
    files = snapshot(root, spec['files'])
    import_roots = spec.get('import_roots', [])
    if not isinstance(import_roots, list) or not all(isinstance(name, str) for name in import_roots):
        raise ValueError('import_roots must be a list of selected project-relative directories')
    normalized_roots = []
    for name in import_roots:
        path = relative(name)
        if (not (root / path).is_dir() or (root / path).is_symlink()
                or not any(path in Path(key).parents for key in files)
                or path in normalized_roots):
            raise ValueError('Import root must be a distinct directory containing selected files: ' + name)
        normalized_roots.append(path)
    probe_files = {}
    total = sum(len(content) for content in files.values())
    for name, content in spec.get('probe_files', {}).items():
        if not isinstance(name, str) or not isinstance(content, str):
            raise ValueError('probe_files must map relative paths to text')
        path = relative(name)
        key = str(path)
        if (root / path).exists() or (root / path).is_symlink():
            raise ValueError('Probe files must use new project paths: ' + key)
        for other in (*files, *probe_files):
            other_path = Path(other)
            if path == other_path or path in other_path.parents or other_path in path.parents:
                raise ValueError('Probe file path collision: ' + key)
        encoded = content.encode('utf-8')
        total += len(encoded)
        if total > 20_000_000:
            raise ValueError('Selected inputs and probe files exceed 20 MB')
        probe_files[key] = encoded
    probe_replacements = {}
    for name, content in spec.get('probe_replacements', {}).items():
        if not isinstance(name, str) or not isinstance(content, str):
            raise ValueError('probe_replacements must map selected relative paths to text')
        key = str(relative(name))
        if key not in files or key == target or key in probe_replacements:
            raise ValueError('Probe replacement requires a distinct selected non-target file: ' + key)
        encoded = content.encode('utf-8')
        total += len(encoded)
        if total > 20_000_000:
            raise ValueError('Selected inputs and probe contents exceed 20 MB')
        probe_replacements[key] = encoded
    modes = {name: (root / name).stat().st_mode & 0o777 for name in files}
    if target not in files:
        raise ValueError('Mutation target must be among selected input files')
    original = files[target].decode('utf-8')
    if original.count(old) != 1:
        raise ValueError('Mutation text must match exactly once')
    faulty = original.replace(old, new, 1).encode('utf-8')
    guarded = project_inventory(root) if spec.get('guard_project', False) else None
    identity = (files, modes, spec['imports'], spec['tests'], spec.get('precheck'), import_roots,
                spec.get('runner', 'unittest'), str(python), timeout, dict(os.environ), guarded,
                spec.get('invocation', 'bootstrap'))
    reused = _baseline is not None and _baseline.get('identity') == identity
    selected_baseline = None
    if _selection_baselines is not None:
        # One shared source snapshot, not one copy per test selection. All other
        # identity components still invalidate every cached normal observation.
        context = identity[:3] + identity[4:]
        if _selection_baselines.get('context') != context:
            _selection_baselines.update(context=context, checks={})
        selection = tuple(spec['tests'])
        selected_baseline = _selection_baselines['checks'].get(selection)
        reused = selected_baseline is not None
    probe_identity = (identity, spec.get('probe'), probe_files, spec.get('probe_tests'), probe_replacements)
    probe_reused = False
    results = {}
    order = [('correct', 'tests'), ('correct', 'probe'), ('mutant', 'tests'), ('mutant', 'probe')]
    if probe_when == 'survives':
        order = [('correct', 'tests'), ('mutant', 'tests'), ('correct', 'probe'), ('mutant', 'probe')]
    skipped = None
    output = None
    try:
        with tempfile.TemporaryDirectory(prefix='.con-artist-', dir=root) as scratch:
            for variant, check in order:
                if check == 'probe' and (not has_probe or skipped is not None):
                    continue
                if variant == 'correct' and check == 'tests' and reused:
                    results['correct_tests'] = dict((selected_baseline or _baseline)['result'])
                    continue
                if variant == 'correct' and check == 'probe' and _probe_baseline is not None \
                        and _probe_baseline.get('identity') == probe_identity:
                    results['correct_probe'] = dict(_probe_baseline['result'])
                    probe_reused = True
                    continue
                # Each check starts from the same inputs, not prior test side effects.
                directory = Path(scratch) / (variant + '-' + check)
                directory.mkdir()
                created_parents = {directory}
                for name, content in files.items():
                    if check == 'probe':
                        content = probe_replacements.get(name, content)
                    dest = directory / name
                    if dest.parent not in created_parents:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        created_parents.add(dest.parent)
                    dest.write_bytes(faulty if variant == 'mutant' and name == target else content)
                    dest.chmod(modes[name])
                phase_spec = spec
                if check == 'probe' and file_probe:
                    for name, content in probe_files.items():
                        dest = directory / name
                        if dest.parent not in created_parents:
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            created_parents.add(dest.parent)
                        with dest.open('xb') as stream:
                            stream.write(content)
                    phase_spec = dict(spec, tests=spec['probe_tests'])
                result = execute(str(python), directory, phase_spec,
                                 spec.get('probe') if check == 'probe' else None, timeout)
                results[variant + '_' + check] = result
                if (result['timed_out'] or result['exit_code'] in (5, 7)
                        or (variant == 'correct' and result['exit_code'] != 0)
                        or (spec.get('precheck') and result['exit_code'] == 6)):
                    output = dict(status='incomplete', checks=results)
                    if reused:
                        output['correct_tests_reused'] = True
                    if probe_reused:
                        output['correct_probe_reused'] = True
                    return output
                if variant == 'correct' and check == 'tests' and _baseline is not None:
                    _baseline.update(identity=identity, result=dict(result))
                if variant == 'correct' and check == 'tests' and _selection_baselines is not None:
                    _selection_baselines['checks'][selection] = dict(
                        result=dict(result), observation_index=_selection_baselines['index'])
                if variant == 'correct' and check == 'probe' and _probe_baseline is not None:
                    _probe_baseline.update(identity=probe_identity, result=dict(result))
                if probe_when == 'survives' and variant == 'mutant' and check == 'tests' and result['exit_code'] != 0:
                    skipped = 'Mutant tests exited nonzero; inspect their failure before any coverage claim. Proposed probe was not validated.'
        output = dict(status='observed', checks=results,
                      limitation='Nonzero mutant exit is not automatically a killed behavioral fault; inspect the failure.')
        if skipped is not None:
            output['probe_skipped'] = skipped
        if reused:
            output['correct_tests_reused'] = True
        if probe_reused:
            output['correct_probe_reused'] = True
        return output
    finally:
        changed = [name for name, content in files.items()
                   if not original_matches(root / name, content, modes[name])]
        if changed:
            raise RuntimeError('Selected originals changed during audit; not restored: ' + ', '.join(changed))
        if guarded is not None:
            current, _ = project_inventory(root)
            previous, _ = guarded
            differences = sorted(name for name in previous.keys() | current.keys()
                                 if previous.get(name) != current.get(name))
            if differences:
                raise RuntimeError('Project tree changed during audit; not restored (' + str(len(differences))
                                   + ' paths): ' + ', '.join(differences[:20]))
        if output is not None:
            # Both normal and early returns leave the context manager before
            # reaching this finally block. Never report removal from intent alone.
            if Path(scratch).exists() or Path(scratch).is_symlink():
                raise RuntimeError('Owned audit scratch removal unconfirmed: ' + scratch)
            output['integrity'] = dict(
                selected_files=len(files),
                selected_original_bytes_and_modes_unchanged=True,
                owned_scratch_removed=True)
            if guarded is not None:
                output['integrity']['project_guard'] = dict(
                    unchanged=True, entries=len(guarded[0]), file_bytes=guarded[1],
                    scope='source root including Git metadata; symlink targets not read')


def audit_batch(root, spec, python=sys.executable, timeout=30):
    """Reuse a successful baseline only within this explicit local batch."""
    common_keys = {'files', 'imports', 'runner', 'tests', 'mutations', 'precheck', 'import_roots', 'guard_project', 'invocation'}
    fault_keys = {'target', 'old', 'new', 'tests', 'probe', 'probe_when', 'probe_files', 'probe_replacements', 'probe_tests'}
    mutations = spec.get('mutations')
    misplaced = (set(spec) - common_keys) & fault_keys
    if misplaced:
        raise ValueError('Batch fault/probe fields belong in each mutations[] entry, not the batch root: '
                         + ', '.join(sorted(misplaced)))
    if set(spec) - common_keys or not isinstance(mutations, list) or not 1 <= len(mutations) <= 8:
        raise ValueError('Batch requires shared files/imports/runner/tests and 1–8 mutations')
    for fault in mutations:
        if not isinstance(fault, dict) or set(fault) - fault_keys or not {'target', 'old', 'new'} <= set(fault):
            raise ValueError('Each mutation requires target/old/new and optional tests/probe settings')
    common = {key: value for key, value in spec.items() if key != 'mutations'}
    selection_baselines, probe_baseline, observations = {}, {}, []
    baseline_indices = {}
    for fault in mutations:
        try:
            selection_baselines['index'] = len(observations)
            recipe = dict(common, **fault)
            result = audit(root, recipe, python, timeout,
                           _selection_baselines=selection_baselines, _probe_baseline=probe_baseline)
        except (ValueError, KeyError, OSError) as error:
            if not observations:
                raise
            # Retain earlier evidence, but never count the failed or later faults.
            # RuntimeError (integrity/unconfirmed cleanup) and interruptions still
            # propagate as before, rather than being treated as ordinary input errors.
            result = dict(status='incomplete', checks={},
                          error=type(error).__name__ + ': ' + str(error),
                          limitation='This audit did not return its checks; empty checks do not prove that no execution occurred. Earlier audit observations are retained. Do not retry until the error and any process state are understood.')
        for name in ('correct_tests', 'correct_probe'):
            if name not in result['checks']:
                continue
            if result.get(name + '_reused'):
                # Point directly to the execution, not another reused reference.
                check = result['checks'][name]
                index = (selection_baselines['checks'][tuple(recipe['tests'])]['observation_index']
                         if name == 'correct_tests' else baseline_indices[name])
                result['checks'][name] = dict(
                    exit_code=check['exit_code'], timed_out=check['timed_out'],
                    observation_ref=f'#/audits/{index}/checks/{name}')
            else:
                baseline_indices[name] = len(observations)
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
    parser.add_argument('--pretty', action='store_true', help='Indent JSON for manual reading; default retains identical values in compact JSON')
    args = parser.parse_args()
    try:
        recipe = sys.stdin.read() if args.spec == Path('-') else args.spec.read_text()
        spec = json.loads(recipe)
        run = audit_batch if isinstance(spec, dict) and 'mutations' in spec else audit
        result = run(args.source, spec, args.python, args.timeout)
    except (ValueError, KeyError, OSError, RuntimeError) as error:
        parser.exit(2, 'Audit not established: ' + str(error) + '\n')
    print(json.dumps(result, indent=2) if args.pretty else json.dumps(result, separators=(',', ':')))
    return 0 if result['status'] == 'observed' else 2


if __name__ == '__main__':
    sys.exit(main())
