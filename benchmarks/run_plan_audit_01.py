"""Freeze proposal-only and verified-assertion requests; execute six cells once."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import run
from plan_audit_cases import cases, preflight
from run_cachetools_audit_01 import snapshot, git

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ('baseline', 'prior', 'current')
REVISIONS = {'prior': '740948e', 'current': 'a3dee3b'}
SCHEDULE = [(0, 'baseline'), (0, 'prior'), (0, 'current'),
            (1, 'current'), (1, 'prior'), (1, 'baseline')]
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360,
                repeats=1, jobs=1)


def identities():
    names = ['benchmarks/run_plan_audit_01.py', 'benchmarks/plan_audit_cases.py',
             'benchmarks/run_cachetools_audit_01.py', 'benchmarks/run.py',
             'benchmarks/PLAN-AUDIT-01-PROTOCOL.md', 'tests/test_plan_audit_runner.py']
    return {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in names}


def digests(output):
    return {c: run.resource_digest(output / c / 'skills') for c in CONDITIONS}


def execute(output, manifest):
    if (manifest['identities'] != identities() or manifest['cases'] != cases()
            or manifest['resource_digests'] != digests(output)
            or manifest['schedule'] != [list(x) for x in SCHEDULE]
            or manifest['settings'] != SETTINGS or manifest['python_version'] != sys.version
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs/resources/settings changed or already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
                       revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + '/' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1, output / condition,
            SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'], disabled,
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
    for condition in REVISIONS:
        snapshot(output / condition, REVISIONS[condition])
    manifest = dict(cases=cases(), identities=identities(),
        schedule=[list(x) for x in SCHEDULE],
        resource_revisions={c: git('rev-parse', r).decode().strip() for c, r in REVISIONS.items()},
        resource_digests=digests(output), settings=SETTINGS, python_version=sys.version,
        native_preflight=controls, completed_cells=[], stopped_after_limit=False,
        prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / c for c in CONDITIONS)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared two requests / six sessions; native controls passed; no model calls.')


if __name__ == '__main__':
    main()
