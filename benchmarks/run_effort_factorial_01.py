"""Frozen two-task effort/skill screen; no retries or resumed partial schedule."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import con_artist_sqlite_cases as sqlite_fixture
import hostage_refresh_cases as refresh_fixture
import run

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = '35bba0a'
CONDITIONS = ('low-baseline', 'low-current', 'medium-baseline', 'medium-current')
SCHEDULE = [(0, c) for c in ('low-baseline', 'low-current', 'medium-current', 'medium-baseline')] + [
    (1, c) for c in ('medium-baseline', 'medium-current', 'low-current', 'low-baseline')]
SETTINGS = dict(model='gpt-6-astra', timeout_seconds=360, jobs=1, repeats=1)


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], timeout=20)


def cases():
    selections = (('con-artist-sqlite-cases.json', 'sqlite-commit-audit'),
                  ('hostage-refresh-cases.json', 'refresh-owner-a'))
    selected = []
    for filename, identity in selections:
        matches = [c for c in json.loads((ROOT / 'benchmarks' / filename).read_text()) if c['id'] == identity]
        if len(matches) != 1:
            raise ValueError('Unexpected case selection')
        selected.append(matches[0])
    return selected


def identities():
    names = ('benchmarks/run_effort_factorial_01.py', 'benchmarks/EFFORT-FACTORIAL-01-PROTOCOL.md',
             'benchmarks/run.py', 'benchmarks/con_artist_sqlite_cases.py',
             'benchmarks/hostage_refresh_cases.py', 'benchmarks/con-artist-sqlite-cases.json',
             'benchmarks/hostage-refresh-cases.json', 'tests/test_effort_factorial_runner.py',
             'tests/test_sqlite_audit_fixture.py', 'tests/test_hostage_refresh_fixture.py')
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def preflight():
    selected = cases()
    if selected != [sqlite_fixture.cases()[0], refresh_fixture.cases()[0]]:
        raise ValueError('Case JSON differs from actual fixture builder')
    imports = []
    for case, module in zip(selected, ('ingest.endpoint', 'preview')):
        with tempfile.TemporaryDirectory(prefix='effort-import-', dir=ROOT / 'benchmarks') as directory:
            project = Path(directory)
            for name, body in case['files'].items():
                target = project / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body)
            result = subprocess.run([sys.executable, '-B', '-c',
                                     'import importlib; importlib.import_module(' + repr(module) + ')'],
                                    cwd=project, capture_output=True, text=True, timeout=10)
            if result.returncode:
                raise ValueError('Fresh public import failed: ' + result.stderr)
            imports.append(dict(case=case['id'], module=module, exit_code=result.returncode))
    return dict(sqlite=sqlite_fixture.preflight(), refresh=refresh_fixture.preflight(),
                fresh_imports=imports, limitation='Author controls, not model execution.')


def snapshot(directory):
    for entry in git('ls-tree', '-r', RESOURCE, '--', 'skills/con-artist',
                     'skills/hostage-negotiator').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported skill resource')
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(git('cat-file', 'blob', oid))
        target.chmod(int(mode[-3:], 8))
    if any(not (directory / 'skills' / c['skill'] / 'SKILL.md').is_file() for c in cases()):
        raise ValueError('Pinned skills missing')


def frozen(output):
    if 'REQUEST_RETRIES' in os.environ:
        raise ValueError('Unexpected REQUEST_RETRIES; host configuration unchanged')
    return dict(identities=identities(), cases=cases(), schedule=[list(row) for row in SCHEDULE],
                settings=SETTINGS, python=sys.executable, python_version=sys.version,
                resource_digest=run.resource_digest(output / 'resources' / 'skills'))


def prepare(output):
    if output.exists():
        raise FileExistsError(output)
    controls = preflight()
    output.mkdir(parents=True, exist_ok=False)
    snapshot(output / 'resources')
    manifest = dict(frozen(output), resource_revision=git('rev-parse', RESOURCE).decode().strip(),
                    completed_cells=[], stopped_after_limit=False,
                    prepared_at=datetime.now(timezone.utc).isoformat())
    (output / 'preflight.json').write_text(json.dumps(controls, indent=2) + '\n')
    for condition in CONDITIONS:
        directory = output / condition
        directory.mkdir()
        (directory / 'run.json').write_text(json.dumps(dict(manifest, condition=condition), indent=2) + '\n')
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def execute(output, manifest):
    if (any(manifest.get(k) != v for k, v in frozen(output).items())
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs changed or execution already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                       started_at=datetime.now(timezone.utc).isoformat()), stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        if any(manifest.get(k) != v for k, v in frozen(output).items()):
            raise ValueError('Frozen inputs changed between cells; do not restart')
        effort, arm = condition.split('-')
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + ' / ' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if arm == 'baseline' else 'skill', 1,
                              output / condition, SETTINGS['model'], effort, SETTINGS['timeout_seconds'],
                              disabled, skills_root=output / 'resources' / 'skills',
                              workspace_root=output / 'workspaces' / condition, persist_session=True)
        manifest['completed_cells'].append(dict(case_id=case['id'], condition=condition,
            **{k: result[k] for k in ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        manifest['stopped_after_limit'] = bool(result['limit_detected'])
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result['limit_detected']:
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        execute(output, json.loads((output / 'run.json').read_text()))
    else:
        prepare(output)
        print('Prepared two tasks / eight sessions; no model calls.')
