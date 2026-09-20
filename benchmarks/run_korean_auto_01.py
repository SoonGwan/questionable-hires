"""Prepare and execute a frozen ten-task Korean automatic-selection screen."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

from korean_auto_cases import cases
from run_sqlite_debit_01 import ROOT, git
import run

OUTPUT = ROOT / 'benchmarks/local-runs/korean-auto-01'
RESOURCE = '2990f44'


def identities():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in (
        'benchmarks/cases.json', 'benchmarks/korean_auto_cases.py',
        'benchmarks/run_korean_auto_01.py', 'benchmarks/KOREAN-AUTO-01-PROTOCOL.md',
        'tests/test_korean_auto_cases.py', 'benchmarks/run.py')}


def preflight():
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
        '-p', 'test_korean_auto_cases.py', '-v'], cwd=ROOT, capture_output=True, text=True, timeout=30)
    if result.returncode or 'skipped' in result.stderr:
        raise ValueError(result.stdout + result.stderr)
    return dict(exit_code=0, output=result.stdout + result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    selected = cases()
    directory = OUTPUT / 'auto'
    def save(manifest):
        (OUTPUT / 'run.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    if not args.execute:
        controls = preflight()
        directory.mkdir(parents=True, exist_ok=False)
        for entry in git('ls-tree', '-r', RESOURCE, '--', 'skills').decode().splitlines():
            info, name = entry.split('\t', 1)
            mode, kind, oid = info.split()
            if kind != 'blob' or mode not in ('100644', '100755'):
                raise ValueError('Unsupported resource')
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(git('cat-file', 'blob', oid))
            path.chmod(int(mode[-3:], 8))
        manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
            resource_revision=git('rev-parse', RESOURCE).decode().strip(),
            prepared_at=datetime.now(timezone.utc).isoformat(), cases=selected,
            schedule=[c['id'] for c in selected], model='gpt-6-astra', effort='medium',
            repeats=1, jobs=1, timeout_seconds=240, identities=identities(),
            resource_digest=run.resource_digest(directory / 'skills'),
            native_preflight=controls, session_persistence_requested=True, completed_cells=[])
        (directory / 'run.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
        save(manifest)
        print('Prepared ten auto cells with all eight skills; no model calls.', flush=True)
        return
    manifest = json.loads((OUTPUT / 'run.json').read_text())
    if (manifest['identities'] != identities() or manifest['cases'] != selected or
            manifest['resource_digest'] != run.resource_digest(directory / 'skills')):
        raise ValueError('Prepared inputs/resources changed')
    with (OUTPUT / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
                       launch_revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for case in selected:
        print('Starting ' + case['id'], flush=True)
        result = run.run_cell(case, 'auto', 1, directory, 'gpt-6-astra', 'medium', 240,
                              disabled, skills_root=directory / 'skills', persist_session=True)
        summary = dict(case=case['id'], condition='auto', **{k: result[k] for k in
            ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')})
        manifest['completed_cells'].append(summary)
        save(manifest)
        print(json.dumps(summary), flush=True)
        if result.get('limit_detected'):
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    save(manifest)


if __name__ == '__main__':
    main()
