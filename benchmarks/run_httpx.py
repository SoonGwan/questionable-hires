#!/usr/bin/env python3
"""Run the frozen full-checkout HTTPX audit comparison, excluding oracle context."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import subprocess

from run import ROOT, command, disabled_skills, run_cell

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'
TASKS = {
    'wsgi-cleanup': 'Audit whether tests/test_wsgi.py protects response-iterable cleanup when a client closes a response. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is missing, propose a focused test and verify it against correct and faulty behavior. Do not change the original source or tests.',
    'asgi-head': 'Audit whether tests/test_asgi.py protects HEAD response-body handling. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is missing, propose a focused test and verify it against correct and faulty behavior. Do not change the original source or tests.',
    'asgi-exceptions': 'Audit whether tests/test_asgi.py protects default application-exception propagation. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is adequate for the targeted fault, report that without demanding a stronger test. Do not change the original source or tests.',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', action='append', choices=TASKS)
    parser.add_argument('--arms', nargs='+', choices=('baseline', 'control', 'skill'), default=['baseline', 'control', 'skill'])
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--skill-revision', default='bf420fe')
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error('repeats must be positive')
    tasks = {name: TASKS[name] for name in dict.fromkeys(args.case or TASKS)}
    skill_revision = command(['git', 'rev-parse', '--verify', args.skill_revision + '^{commit}'], ROOT)
    source, python = args.source.resolve(), args.python.absolute()
    if args.output.exists():
        raise FileExistsError(args.output)
    if command(['git', 'rev-parse', 'HEAD'], source) != REVISION:
        raise ValueError('Wrong upstream revision')
    if command(['git', 'status', '--porcelain'], source):
        raise ValueError('Upstream checkout must be clean')
    # Fail before scheduling if environment no longer passes upstream tests.
    subprocess.run([str(python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                    'tests/test_wsgi.py', 'tests/test_asgi.py'], cwd=source, check=True, timeout=60)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    snapshot = output / 'skills/con-artist'
    snapshot.mkdir(parents=True)
    for name in ('SKILL.md', 'agents/openai.yaml'):
        target = snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(['git', 'show', f'{skill_revision}:skills/con-artist/{name}'], cwd=ROOT))
    schedule = [(case, arm, repeat) for repeat in range(1, args.repeats + 1) for case in tasks for arm in dict.fromkeys(args.arms)]
    random.Random(20260912).shuffle(schedule)
    manifest = dict(upstream_revision=REVISION, revision=command(['git', 'rev-parse', 'HEAD'], ROOT),
                    codex_version=command(['codex', '--version'], ROOT), model='gpt-6-astra', effort='medium',
                    seed=20260912, timeout_seconds=360, jobs=1,
                    skill_sha256=hashlib.sha256((snapshot / 'SKILL.md').read_bytes()).hexdigest(),
                    tasks=tasks, schedule=schedule, skill_revision=skill_revision, completed_cells=[], stopped_after_limit=False,
                    started_at=datetime.now(timezone.utc).isoformat(),
                    dependencies=command([str(python), '-m', 'pip', 'freeze'], source))
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    disabled = disabled_skills()
    for name, arm, repeat in schedule:
        instructions = f'\n\nUse the preinstalled interpreter {python} for all Python/pytest commands. Do not install dependencies. Keep disposable mutation copies and diagnostic artifacts inside this project, without modifying its existing files.'
        case = dict(id=name, skill='con-artist', task=TASKS[name] + instructions)
        try:
            result = run_cell(case, arm, repeat, output, 'gpt-6-astra', 'medium', 360, disabled, output / 'skills', source)
        except Exception as error:
            manifest['runner_error'] = f'{type(error).__name__}: {error}'
            (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
            raise
        manifest['completed_cells'].append(dict(case=name, arm=arm, repeat=repeat, completed=result['completed']))
        manifest['stopped_after_limit'] = result.get('limit_detected', False)
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(name, arm, repeat, 'completed' if result['completed'] else 'incomplete', flush=True)
        if manifest['stopped_after_limit']:
            raise SystemExit('Account limit: remaining scheduled cells unattempted; no retries')
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    if not all(row['completed'] for row in manifest['completed_cells']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
