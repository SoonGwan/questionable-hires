"""Prepare, then execute six frozen Node comparison sessions once."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

import run
from receipt_node_cases import build_cases, preflight as native_preflight

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'benchmarks/local-runs/receipt-node-01'
REVISIONS = {'original': '310d483', 'current': '8fa20dd'}
CONDITIONS = ('baseline', 'original', 'current')
SCHEDULE = [(0, 'baseline'), (0, 'original'), (0, 'current'),
            (1, 'current'), (1, 'original'), (1, 'baseline')]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def snapshot(directory, revision):
    for entry in git('ls-tree', '-r', revision, '--', 'skills/receipt').decode().splitlines():
        metadata, name = entry.split('\t', 1)
        mode, kind, oid = metadata.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported resource')
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file', 'blob', oid))
        path.chmod(int(mode[-3:], 8))


def identities():
    names = ('benchmarks/run_receipt_node_01.py', 'benchmarks/receipt_node_cases.py',
             'benchmarks/RECEIPT-NODE-01-PROTOCOL.md', 'benchmarks/run.py')
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def preflight():
    if (ROOT / 'skills/receipt/scripts/compare.py').read_bytes() != git('show', REVISIONS['current'] + ':skills/receipt/scripts/compare.py'):
        raise ValueError('Preflight collector differs from the frozen current resource')
    return native_preflight(build_cases())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    selected = build_cases()
    def save(manifest):
        (OUTPUT / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    def digests():
        return {condition: run.resource_digest(OUTPUT / condition / 'skills') for condition in CONDITIONS}
    if not args.execute:
        controls = preflight()
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / 'baseline').mkdir()
        for condition, revision in REVISIONS.items():
            snapshot(OUTPUT / condition, revision)
        manifest = dict(resource_revisions={c: git('rev-parse', r).decode().strip() for c, r in REVISIONS.items()},
                        identities=identities(), cases=selected,
                        schedule=[dict(case=selected[i]['id'], condition=c) for i, c in SCHEDULE],
                        model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1,
                        resource_digests=digests(), native_preflight=controls, completed_cells=[],
                        prepared_at=datetime.now(timezone.utc).isoformat(), stopped_after_limit=False)
        for condition in CONDITIONS:
            (OUTPUT / condition / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        save(manifest)
        print('Prepared six cells; independent native and helper controls passed; no model calls.')
        return
    manifest = json.loads((OUTPUT / 'run.json').read_text())
    if manifest['identities'] != identities() or manifest['cases'] != selected or manifest['resource_digests'] != digests():
        raise ValueError('Frozen inputs/resources changed')
    with (OUTPUT / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(), revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        case = selected[index]
        print('Starting ' + condition + '/' + case['id'], flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
                              OUTPUT / condition, 'gpt-6-astra', 'medium', 360, disabled,
                              skills_root=OUTPUT / condition / 'skills', persist_session=True)
        manifest['completed_cells'].append(dict(case=case['id'], condition=condition,
            **{key: result[key] for key in ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        save(manifest)
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result.get('limit_detected'):
            manifest['stopped_after_limit'] = True
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    save(manifest)


if __name__ == '__main__':
    main()
