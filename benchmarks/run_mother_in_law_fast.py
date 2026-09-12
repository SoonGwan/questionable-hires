#!/usr/bin/env python3
"""Run or materialize the preregistered compact mother-in-law suite."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from validate_mother_in_law_fast_suite import ROOT, SUITE, validate


def selected_cases(suite, requested):
    known = {case['id']: case for case in suite['cases']}
    unknown = sorted(set(requested) - set(known))
    if unknown:
        raise ValueError('Unknown cases: ' + ', '.join(unknown))
    return [case for case in suite['cases'] if not requested or case['id'] in requested]


def materialize_generic(cases, destination):
    records = []
    for case in cases:
        if case['runner'] != 'generic':
            continue
        source = json.loads((ROOT / case['source']).read_text())
        records.append(next(record for record in source if record['id'] == case['id']))
    destination.write_text(json.dumps(records, indent=2) + '\n')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--arms', nargs='+', choices=['baseline', 'skill'],
                        default=['baseline', 'skill'])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--auth-file', type=Path,
                        help='required only when a browser case is executed')
    args = parser.parse_args()
    suite = validate(ROOT, SUITE)
    try:
        cases = selected_cases(suite, args.case)
    except ValueError as error:
        parser.error(str(error))
    if not cases:
        parser.error('At least one case is required')
    browser = [case for case in cases if case['runner'] == 'browser-container']
    if browser and not args.dry_run and not args.auth_file:
        parser.error('browser execution requires --auth-file')

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    generic_path = output / 'generic-cases.json'
    generic = materialize_generic(cases, generic_path)
    plan = dict(
        suite_version=suite['version'], skill=suite['skill'], arms=args.arms,
        cases=cases, session_count=len(cases) * len(args.arms),
        created_at=datetime.now(timezone.utc).isoformat(), dry_run=args.dry_run,
        commands=[])
    if generic:
        plan['commands'].append([
            sys.executable, '-B', str(ROOT / 'run.py'), '--cases-file',
            str(generic_path), '--output', str(output / 'generic'), '--arms',
            *args.arms, '--repeats', '1', '--jobs', '1', '--model',
            'gpt-6-astra', '--effort', 'medium'])
    if browser:
        plan['commands'].append([
            sys.executable, '-B', str(ROOT / 'run_browser_model.py'),
            '--container', '--auth-file', str(args.auth_file), '--output',
            str(output / 'browser'), '--arms', *args.arms])
    plan_path = output / 'plan.json'
    plan_path.write_text(json.dumps(plan, indent=2) + '\n')
    print(f"planned {len(cases)} cases / {plan['session_count']} sessions")
    if args.dry_run:
        return 0
    for command in plan['commands']:
        completed = subprocess.run(command, cwd=ROOT.parent)
        if completed.returncode:
            return completed.returncode
    plan['finished_at'] = datetime.now(timezone.utc).isoformat()
    plan_path.write_text(json.dumps(plan, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
