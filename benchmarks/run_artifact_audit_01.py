"""Prepare then execute one frozen three-cell audit probe; never retry cells."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

from artifact_audit_case import case
from run_sqlite_debit_01 import ROOT, git
import run

OUTPUT = ROOT / 'benchmarks/local-runs/artifact-audit-01'
REVISIONS = {'original': '9c0c458', 'candidate': '7c96592'}
SCHEDULE = ('original', 'baseline', 'candidate')


def identities():
    names = ('benchmarks/artifact_audit_case.py', 'tests/test_artifact_audit_case.py',
             'benchmarks/run_artifact_audit_01.py', 'benchmarks/ARTIFACT-AUDIT-01-PROTOCOL.md',
             'benchmarks/run.py')
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def preflight():
    import pytest
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
                             '-p', 'test_artifact_audit_case.py', '-v'], cwd=ROOT,
                            capture_output=True, text=True, timeout=30)
    if result.returncode or 'skipped' in result.stderr:
        raise ValueError(result.stdout + result.stderr)
    return dict(exit_code=result.returncode, output=result.stdout + result.stderr,
                python=sys.executable, python_version=sys.version, pytest=pytest.__version__)


def snapshot(directory, revision):
    for entry in git('ls-tree', '-r', revision, '--', 'skills/con-artist').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported skill resource')
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(git('cat-file', 'blob', oid))
        path.chmod(int(mode[-3:], 8))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    selected = case(sys.executable)
    def save(manifest):
        (OUTPUT / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    if not args.execute:
        controls = preflight()
        OUTPUT.mkdir(parents=True, exist_ok=False)
        manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
            resource_revisions={c: git('rev-parse', r).decode().strip() for c, r in REVISIONS.items()},
            prepared_at=datetime.now(timezone.utc).isoformat(), cases=[selected], schedule=SCHEDULE,
            model='gpt-6-astra', effort='medium', repeats=1, jobs=1, timeout_seconds=360,
            session_persistence_requested=True, identities=identities(),
            native_preflight=controls, completed_cells=[])
        for condition in SCHEDULE:
            directory = OUTPUT / condition
            directory.mkdir()
            if condition in REVISIONS:
                snapshot(directory, REVISIONS[condition])
            (directory / 'run.json').write_text(json.dumps(dict(manifest, condition=condition), indent=2)+'\n')
        original = run.resource_manifest(OUTPUT / 'original/skills')
        candidate = run.resource_manifest(OUTPUT / 'candidate/skills')
        changed = {name for name in original if original[name] != candidate.get(name)}
        if set(original) != set(candidate) or changed != {
                'con-artist/scripts/audit.py', 'con-artist/references/python-audit.md',
                'con-artist/references/python-audit-probes.md'}:
            raise ValueError('Unexpected resource changes')
        manifest['resource_digests'] = {c: run.resource_digest(OUTPUT / c / 'skills') for c in SCHEDULE}
        save(manifest)
        print('Prepared three cells with passing native controls; no model calls.', flush=True)
        return
    manifest = json.loads((OUTPUT / 'run.json').read_text())
    if (manifest['identities'] != identities() or manifest['cases'] != [selected] or
            manifest['resource_digests'] != {c: run.resource_digest(OUTPUT / c / 'skills') for c in SCHEDULE}):
        raise ValueError('Prepared inputs/resources changed')
    with (OUTPUT / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
                       launch_revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for condition in SCHEDULE:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(selected, 'baseline' if condition == 'baseline' else 'skill', 1,
            OUTPUT / condition, 'gpt-6-astra', 'medium', 360, disabled,
            skills_root=OUTPUT / condition / 'skills', persist_session=True)
        summary = dict(case=selected['id'], condition=condition, **{k: result[k] for k in
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
