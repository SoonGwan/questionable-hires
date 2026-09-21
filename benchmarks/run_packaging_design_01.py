"""Freeze and execute three original packaging design review sessions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

import run
from packaging_design_case import case, preflight, VERSION
from run_click_context_01 import environment
from run_httpx import freeze_skill

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'benchmarks/candidates/landlord-context/skills'
PRIOR = 'a545a53'
SCHEDULE = ['baseline', 'candidate', 'prior']
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360)


def identities():
    names = ['run_packaging_design_01.py', 'packaging_design_case.py', 'run.py',
             'run_httpx.py', 'run_click_context_01.py', 'PACKAGING-DESIGN-01-PROTOCOL.md']
    result = {n: hashlib.sha256((ROOT / 'benchmarks' / n).read_bytes()).hexdigest() for n in names}
    result['candidate'] = run.resource_digest(CANDIDATE)
    return result


def digests(output):
    return {c: run.resource_digest(output / c / 'skills') for c in SCHEDULE}


def execute(manifest, output, python):
    if (manifest['identities'] != identities() or manifest['case'] != case(python)
            or manifest['resource_digests'] != digests(output)
            or manifest['schedule'] != SCHEDULE or manifest['settings'] != SETTINGS
            or manifest['environment'] != environment(python)
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs/settings changed or already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump({'started_at': datetime.now(timezone.utc).isoformat()}, stream)
    disabled = run.disabled_skills()
    for condition in SCHEDULE:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(manifest['case'], 'baseline' if condition == 'baseline' else 'skill',
            1, output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills', persist_session=True)
        manifest['completed_cells'].append(dict(condition=condition, **{k: result[k] for k in
            ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
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
    output, python = args.output.resolve(), Path(sys.executable).absolute()
    if args.execute:
        execute(json.loads((output / 'run.json').read_text()), output, python)
        return
    frozen = case(python)
    controls = preflight(frozen['files'], python)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'baseline/skills').mkdir(parents=True)
    freeze_skill(ROOT, PRIOR, output / 'prior/skills/landlord', skill_name='landlord')
    shutil.copytree(CANDIDATE, output / 'candidate/skills')
    manifest = dict(case=frozen, distribution_version=VERSION, prior_revision=PRIOR,
        identities=identities(), resource_digests=digests(output), schedule=SCHEDULE,
        settings=SETTINGS, environment=environment(python), native_preflight=controls,
        completed_cells=[], stopped_after_limit=False, repeats=1, jobs=1,
        prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / c for c in SCHEDULE)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared three sessions with eight native preflight observations; no model calls.')


if __name__ == '__main__':
    main()
