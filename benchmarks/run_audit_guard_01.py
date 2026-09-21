"""Freeze then run one three-arm audit-guard transfer, with original sessions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import sqlite3
from pathlib import Path
import sys

import run
from audit_guard_case import case, preflight
from run_httpx import freeze_skill

ROOT = Path(__file__).resolve().parents[1]
REVISIONS = {'prior': 'f157b76', 'current': 'f6f2980'}
SCHEDULE = ['prior', 'baseline', 'current']


def identities():
    return {n: hashlib.sha256((ROOT / 'benchmarks' / n).read_bytes()).hexdigest()
        for n in ('run_audit_guard_01.py', 'audit_guard_case.py', 'run.py', 'run_httpx.py', 'AUDIT-GUARD-01-PROTOCOL.md')}


def digests(output):
    return {c: run.resource_digest(output / c / 'skills') for c in SCHEDULE}


def execute(output, manifest):
    if (manifest['identities'] != identities() or manifest['case'] != case()
            or manifest['resource_digests'] != digests(output)
            or manifest['schedule'] != SCHEDULE or manifest['python_version'] != sys.version
            or manifest['native_preflight']['sqlite_version'] != sqlite3.sqlite_version):
        raise ValueError('Frozen inputs/resources changed')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump({'started_at': datetime.now(timezone.utc).isoformat()}, stream)
    disabled = run.disabled_skills()
    for condition in SCHEDULE:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(manifest['case'], 'baseline' if condition == 'baseline' else 'skill',
            1, output / condition, 'gpt-6-astra', 'medium', 360, disabled,
            skills_root=output / condition / 'skills', persist_session=True)
        manifest['completed_cells'].append(dict(condition=condition,
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
    manifest = dict(case=case(), identities=identities(), schedule=SCHEDULE, resource_revisions=REVISIONS,
        resource_digests=digests(output), native_preflight=controls, python_version=sys.version,
        model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1,
        completed_cells=[], stopped_after_limit=False, prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / c for c in SCHEDULE)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared three cells; native SQLite pass/fail controls verified; no model calls.')


if __name__ == '__main__':
    main()
