"""Freeze synchronous/async edits before six serial original model sessions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

import run
from hostage_conditional_cases import cases, preflight, REVISION
from run_hostage_buffer_01 import snapshot

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'benchmarks/candidates/hostage-conditional/skills'
CONDITIONS = ['prior', 'baseline', 'candidate']
SCHEDULE = [(0, 'prior'), (0, 'baseline'), (0, 'candidate'),
            (1, 'candidate'), (1, 'baseline'), (1, 'prior')]
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360,
                repeats=1, jobs=1)


def identities():
    names = ['run_hostage_conditional_01.py', 'hostage_conditional_cases.py',
             'run.py', 'run_hostage_buffer_01.py', 'HOSTAGE-CONDITIONAL-01-PROTOCOL.md']
    result = {n: hashlib.sha256((ROOT / 'benchmarks' / n).read_bytes()).hexdigest() for n in names}
    result['candidate'] = run.resource_digest(CANDIDATE)
    return result


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
        json.dump({'started_at': datetime.now(timezone.utc).isoformat()}, stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + '/' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill',
            1, output / condition, SETTINGS['model'], SETTINGS['effort'],
            SETTINGS['timeout_seconds'], disabled,
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
    frozen_cases = cases()
    controls = preflight()
    for case in frozen_cases:
        for name, body in case['files'].items():
            if name.endswith('.py'):
                compile(body, name, 'exec')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'baseline/skills').mkdir(parents=True)
    snapshot(output / 'prior', REVISION)
    shutil.copytree(CANDIDATE, output / 'candidate/skills')
    manifest = dict(cases=frozen_cases, native_preflight=controls, identities=identities(),
        schedule=[list(x) for x in SCHEDULE], resource_revision=REVISION,
        resource_digests=digests(output), settings=SETTINGS, python_version=sys.version,
        completed_cells=[], stopped_after_limit=False,
        prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / c for c in CONDITIONS)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared two edit tasks / six cells; native controls verified; no model calls.')


if __name__ == '__main__':
    main()
