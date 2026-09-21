"""Freeze and execute the six predeclared ancestry-scope cells, without retries."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import ancestry_scope_case as fixture
import run

ROOT = fixture.ROOT
CONDITIONS = ('prior', 'baseline', 'current')
RESOURCES = {'prior': '31a68d5', 'current': '99301e9'}
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=240, repeats=1, jobs=1)
SCHEDULE = [(0, c) for c in CONDITIONS] + [(1, c) for c in reversed(CONDITIONS)]


def repository_git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], timeout=20)


def source_identity(source):
    if fixture.git(source, 'status', '--porcelain'):
        raise ValueError('Fixture source changed')
    if fixture.git(source, 'rev-parse', '--is-shallow-repository') != 'false':
        raise ValueError('Fixture must retain full history')
    files = {}
    for name in fixture.git(source, 'ls-files').splitlines():
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Unexpected fixture path')
        files[name] = dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           mode=path.stat().st_mode & 0o777)
    return dict(head=fixture.git(source, 'rev-parse', 'HEAD'),
                refs=fixture.git(source, 'show-ref'),
                ancestors=fixture.git(source, 'rev-list', 'HEAD'), files=files)


def identities():
    names = ('benchmarks/run_ancestry_scope_01.py', 'benchmarks/ancestry_scope_case.py',
             'benchmarks/run.py', 'benchmarks/ANCESTRY-SCOPE-01-PROTOCOL.md',
             'tests/test_ancestry_scope_case.py', 'tests/test_ancestry_scope_runner.py')
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def frozen(output):
    return dict(identities=identities(), source_identity=source_identity(output / 'source'),
                cases=fixture.cases(), schedule=[list(row) for row in SCHEDULE],
                settings=SETTINGS, python_version=sys.version, python=sys.executable,
                resource_digests={c: run.resource_digest(output / c / 'skills') for c in CONDITIONS})


def prepare(output):
    output.mkdir(parents=True, exist_ok=False)
    fixture_ids = fixture.build(output / 'source')
    for condition in CONDITIONS:
        (output / condition / 'skills').mkdir(parents=True)
    for condition, revision in RESOURCES.items():
        for entry in repository_git('ls-tree', '-r', revision, '--', 'skills/necromancer').decode().splitlines():
            info, name = entry.split('\t', 1)
            mode, kind, oid = info.split()
            if kind != 'blob' or mode not in ('100644', '100755'):
                raise ValueError('Unexpected skill resource')
            path = output / condition / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(repository_git('cat-file', 'blob', oid))
            path.chmod(int(mode[-3:], 8))
    manifest = dict(frozen(output), fixture_ids=fixture_ids,
        resource_revisions={c: repository_git('rev-parse', r).decode().strip() for c, r in RESOURCES.items()},
        completed_cells=[], stopped_after_limit=False, prepared_at=datetime.now(timezone.utc).isoformat())
    for directory in (output, *(output / c for c in CONDITIONS)):
        (directory / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def execute(output, manifest):
    if (any(manifest.get(k) != v for k, v in frozen(output).items())
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs changed or execution already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
                       revision=repository_git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for case_index, condition in SCHEDULE:
        # Never silently continue a schedule whose source/resources changed mid-run.
        if any(manifest.get(k) != v for k, v in frozen(output).items()):
            raise ValueError('Frozen inputs changed between cells; do not restart')
        case = manifest['cases'][case_index]
        print('Starting ' + case['id'] + ' / ' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
            output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills', project_source=output / 'source',
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        execute(output, json.loads((output / 'run.json').read_text()))
    else:
        prepare(output)
        print('Prepared two requests / six sessions; no model calls.')


if __name__ == '__main__':
    main()
