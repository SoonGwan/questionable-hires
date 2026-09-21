"""Freeze two native edit-audit requests and run every scheduled session once."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import run
from edit_audit_cases import cases, preflight
from run_cachetools_audit_01 import snapshot, git

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ('baseline', 'prior', 'current')
REVISIONS = {'prior': '04bf934', 'current': 'e6aa16e'}
SCHEDULE = [(0, 'prior'), (0, 'baseline'), (0, 'current'),
            (1, 'current'), (1, 'baseline'), (1, 'prior')]
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1)


def identities():
    names = ['benchmarks/run_edit_audit_01.py', 'benchmarks/edit_audit_cases.py',
             'benchmarks/run_cachetools_audit_01.py', 'benchmarks/run.py',
             'benchmarks/EDIT-AUDIT-01-PROTOCOL.md', 'tests/test_edit_audit_runner.py',
             'tests/test_edit_audit_cases.py']
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def digests(output):
    return {condition: run.resource_digest(output / condition / 'skills') for condition in CONDITIONS}


def execute(output, manifest):
    if (manifest['identities'] != identities() or manifest['cases'] != cases()
            or manifest['resource_digests'] != digests(output)
            or manifest['schedule'] != [list(item) for item in SCHEDULE]
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
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
            output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills', persist_session=True)
        manifest['completed_cells'].append(dict(case=case['id'], condition=condition,
            **{key: result[key] for key in ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
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
        snapshot(output / condition, revision)
    manifest = dict(cases=cases(), identities=identities(), schedule=[list(item) for item in SCHEDULE],
        resource_revisions={condition: git('rev-parse', revision).decode().strip()
                            for condition, revision in REVISIONS.items()},
        resource_digests=digests(output), settings=SETTINGS, python_version=sys.version,
        native_preflight=controls, completed_cells=[], stopped_after_limit=False,
        prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / condition for condition in CONDITIONS)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared two requests / six sessions; native controls passed; no model calls.')


if __name__ == '__main__':
    main()
