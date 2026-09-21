"""Frozen sixteen-cell eight-role regression, with no retries or resumption."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import run
import lean_screen_cases as fixture
import preflight_lean_screen as controls

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = {'current': '0d12dd9'}
CONDITIONS = ('baseline', 'current')
SCHEDULE = [(i, c) for i in range(8) for c in (CONDITIONS if i % 2 == 0 else tuple(reversed(CONDITIONS)))]
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360, jobs=1, repeats=1)


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], timeout=20)


def cases():
    selected = fixture.cases()
    if len(selected) != 8 or len({c['skill'] for c in selected}) != 8:
        raise ValueError('Expected eight distinct role tasks')
    return selected


def identities():
    names = ('benchmarks/run_all_eight_current_04.py',
             'benchmarks/ALL-EIGHT-CURRENT-04-PROTOCOL.md',
             'benchmarks/preflight_lean_screen.py', 'benchmarks/run.py',
             'benchmarks/editor_snapshot_cases.py', 'benchmarks/preflight_view_contract.py',
             'tests/test_all_eight_current_04.py',
             'tests/test_history_invoice_fixture.py', 'tests/test_receipt_ledger_fixture.py',
             'tests/test_landlord_check_scope_fixture.py', 'tests/test_exorcist_runtime_fixture.py',
             'tests/test_hostage_refresh_fixture.py', 'tests/test_sqlite_audit_fixture.py')
    return dict(fixture_sources=fixture.source_hashes(),
                execution_sources={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names})


def snapshot(directory, revision):
    for line in git('ls-tree', '-r', revision, '--', 'skills').decode().splitlines():
        info, name = line.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported resource')
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file', 'blob', oid))
        path.chmod(int(mode[-3:], 8))
    for case in cases():
        if not (directory / 'skills' / case['skill'] / 'SKILL.md').is_file():
            raise ValueError('Pinned skill is missing: ' + case['skill'])


def frozen(output):
    if 'REQUEST_RETRIES' in os.environ:
        raise ValueError('Unexpected REQUEST_RETRIES; host configuration unchanged')
    return dict(identities=identities(), cases=cases(), schedule=[list(row) for row in SCHEDULE],
                settings=dict(SETTINGS), python=sys.executable, python_version=sys.version,
                resource_digests={c: run.resource_digest(output / c / 'skills') for c in CONDITIONS})


def prepare(output):
    if output.exists():
        raise FileExistsError(output)
    cases()
    preflight = controls.check()
    output.mkdir(parents=True, exist_ok=False)
    for condition in CONDITIONS:
        (output / condition / 'skills').mkdir(parents=True)
    for condition, revision in RESOURCES.items():
        snapshot(output / condition, revision)
    manifest = dict(frozen(output), resource_revisions={c: git('rev-parse', r).decode().strip()
                                                     for c, r in RESOURCES.items()},
                    completed_cells=[], stopped_after_limit=False,
                    prepared_at=datetime.now(timezone.utc).isoformat())
    (output / 'preflight.json').write_text(json.dumps(preflight, indent=2, default=lambda value: {'blob_hex': value.hex()}) + '\n')
    for directory in (output, *(output / c for c in CONDITIONS)):
        (directory / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
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
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + ' / ' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
            output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills',
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
        print('Prepared eight exposed tasks / sixteen sessions; no model calls.')
