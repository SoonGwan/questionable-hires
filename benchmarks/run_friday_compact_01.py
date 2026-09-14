#!/usr/bin/env python3
"""Frozen old/new Friday comparison; six serial sessions, no retries."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {'original': 'b2816cd', 'candidate': 'e063131'}
SOURCES = {
    'bundle-contract-v2-cases.json': '1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65',
    'friday-writer-cases.json': '7f61ee6e426636279085446bf5dc1f1c9c09b8b68f48f532d82eda6c80412341',
}
SCHEDULE = (
    ('rolling-schema', 'original'), ('rolling-schema', 'candidate'),
    ('quota-overlap-gap', 'candidate'), ('quota-overlap-gap', 'original'),
    ('quota-overlap-control', 'original'), ('quota-overlap-control', 'candidate'),
)


def prepare(output):
    output.mkdir(parents=True, exist_ok=False)
    resources = {}
    for condition, revision in VERSIONS.items():
        paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', revision,
                                         '--', 'skills/friday'], cwd=ROOT).decode().splitlines()
        resources[condition] = {'revision': revision, 'files': {}}
        for path in paths:
            content = subprocess.check_output(['git', 'show', revision + ':' + path], cwd=ROOT)
            relative = Path(path).relative_to('skills')
            target = output / 'snapshots' / condition / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            resources[condition]['files'][str(relative)] = hashlib.sha256(content).hexdigest()
    old, new = (resources[c]['files'] for c in ('original', 'candidate'))
    assert set(old) == set(new)
    assert [p for p in old if old[p] != new[p]] == ['friday/SKILL.md']
    for name, digest in SOURCES.items():
        content = (ROOT / 'benchmarks' / name).read_bytes()
        assert hashlib.sha256(content).hexdigest() == digest
        (output / name).write_bytes(content)
    (output / 'snapshots.json').write_text(json.dumps(resources, indent=2) + '\n')


def execute(output, invoke=subprocess.run):
    records = []
    for index, (case, condition) in enumerate(SCHEDULE, 1):
        source = 'bundle-contract-v2-cases.json' if case == 'rolling-schema' else 'friday-writer-cases.json'
        destination = output / f'{index:02d}-{case}-{condition}'
        command = [sys.executable, '-B', str(ROOT / 'benchmarks/run.py'),
                   '--output', str(destination), '--cases-file', str(output / source),
                   '--case', case, '--arms', 'skill', '--skills-root', str(output / 'snapshots' / condition),
                   '--jobs', '1', '--repeats', '1', '--timeout', '240',
                   '--model', 'gpt-6-astra', '--effort', 'medium', '--seed', '20260911']
        print(f'Starting {index}/6: {case} {condition}', flush=True)
        result = invoke(command, cwd=ROOT)
        manifest = destination / 'run.json'
        state = json.loads(manifest.read_text()) if manifest.exists() else {}
        stopped = bool(state.get('stopped_after_limit') or not state.get('finished_at'))
        records.append({'case': case, 'condition': condition, 'exit_code': result.returncode,
                        'stopped': stopped, 'output': destination.name})
        (output / 'runs.json').write_text(json.dumps(records, indent=2) + '\n')
        if stopped:
            return 2
    return int(any(r['exit_code'] for r in records))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    prepare(output)
    raise SystemExit(execute(output))
