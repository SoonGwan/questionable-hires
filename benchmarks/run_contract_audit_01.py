"""Freeze and execute six contract-transfer cells once; retain original sessions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import run
from contract_audit_cases import build_cases, preflight
from run_httpx import freeze_skill

ROOT = Path(__file__).resolve().parents[1]
REVISIONS = {'prior': '903e7c8', 'current': '19d63ec'}
SCHEDULE = [(0, 'baseline'), (0, 'prior'), (0, 'current'),
            (1, 'current'), (1, 'prior'), (1, 'baseline')]
CONDITIONS = ('baseline', 'prior', 'current')


def identities():
    names = ['run_contract_audit_01.py', 'contract_audit_cases.py', 'run.py',
             'run_httpx.py', 'CONTRACT-AUDIT-01-PROTOCOL.md']
    return {n: hashlib.sha256((ROOT / 'benchmarks' / n).read_bytes()).hexdigest() for n in names}


def cases():
    selected = build_cases()
    for case in selected:
        case['task'] += '\nUse this available interpreter: ' + str(Path(sys.executable).absolute())
    return selected


def digests(output):
    return {c: run.resource_digest(output / c / 'skills') for c in CONDITIONS}


def execute(output, manifest):
    if (manifest['identities'] != identities() or manifest['cases'] != cases()
            or manifest['resource_digests'] != digests(output)
            or manifest['schedule'] != [list(row) for row in SCHEDULE]
            or manifest['python_version'] != sys.version):
        raise ValueError('Frozen inputs/resources changed')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump({'started_at': datetime.now(timezone.utc).isoformat()}, stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        case = manifest['cases'][index]
        print('Starting ' + condition + '/' + case['id'], flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill',
            1, output / condition, 'gpt-6-astra', 'medium', 360, disabled,
            skills_root=output / condition / 'skills', persist_session=True)
        manifest['completed_cells'].append(dict(case=case['id'], condition=condition,
            **{k: result[k] for k in ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        if result['limit_detected']:
            manifest['stopped_after_limit'] = True
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
        return
    controls = preflight()
    output.mkdir(parents=True, exist_ok=False)
    (output / 'baseline/skills').mkdir(parents=True)
    for condition, revision in REVISIONS.items():
        freeze_skill(ROOT, revision, output / condition / 'skills/con-artist')
    manifest = dict(cases=cases(), identities=identities(),
        schedule=[list(row) for row in SCHEDULE], resource_revisions=REVISIONS,
        resource_digests=digests(output), native_preflight=controls, python_version=sys.version,
        model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1,
        completed_cells=[], stopped_after_limit=False,
        prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / c for c in CONDITIONS)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared six sessions; 12 native preflight runs passed; no model calls.')


if __name__ == '__main__':
    main()
