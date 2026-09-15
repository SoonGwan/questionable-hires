"""Frozen six-session development probe; preparation does not call a model."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

from receipt_selection_cases import cases
from run_sqlite_debit_01 import ROOT, git
import run

OUTPUT = ROOT/'benchmarks/local-runs/receipt-selection-01'
REVISIONS = {'original': '6cf9fb1', 'candidate': 'ca3da48'}
SCHEDULE = [(0, 'baseline'), (0, 'original'), (0, 'candidate'),
            (1, 'candidate'), (1, 'original'), (1, 'baseline')]


def snapshot(directory, revision):
    for entry in git('ls-tree', '-r', revision, '--', 'skills/receipt').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported skill resource')
        path = directory/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(git('cat-file', 'blob', oid))
        path.chmod(int(mode[-3:], 8))


def identities():
    paths = ['benchmarks/receipt_selection_cases.py', 'benchmarks/run_receipt_selection_01.py',
             'benchmarks/RECEIPT-SELECTION-01-PROTOCOL.md', 'benchmarks/run.py',
             'tests/test_receipt_selection_cases.py']
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in paths}


def preflight():
    # Keep the tested fixture definition identical to the committed native controls.
    for name in ('benchmarks/receipt_selection_cases.py', 'tests/test_receipt_selection_cases.py'):
        if (ROOT/name).read_bytes() != git('show', '0c4ba15:' + name):
            raise ValueError('Fixture differs from preflight source')
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
                             '-p', 'test_receipt_selection_cases.py', '-v'], cwd=ROOT,
                            capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    return dict(exit_code=result.returncode, output=result.stdout+result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    selected = cases()
    conditions = ('baseline', 'original', 'candidate')
    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest, indent=2)+'\n')
    if not args.execute:
        OUTPUT.mkdir(parents=True, exist_ok=False)
        manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
            resource_revisions={c: git('rev-parse', r).decode().strip() for c, r in REVISIONS.items()},
            prepared_at=datetime.now(timezone.utc).isoformat(), cases=selected,
            schedule=[dict(case=selected[i]['id'], condition=c) for i, c in SCHEDULE],
            model='gpt-6-astra', effort='medium', repeats=1, jobs=1, timeout_seconds=360,
            session_persistence_requested=True, identities=identities(),
            native_preflight=preflight(), completed_cells=[])
        for condition in conditions:
            directory = OUTPUT/condition
            directory.mkdir()
            if condition != 'baseline':
                snapshot(directory, REVISIONS[condition])
            (directory/'run.json').write_text(json.dumps(dict(manifest, condition=condition), indent=2)+'\n')
        original = run.resource_manifest(OUTPUT/'original/skills')
        candidate = run.resource_manifest(OUTPUT/'candidate/skills')
        changed = {n for n in original if original[n] != candidate.get(n)}
        if set(original) != set(candidate) or changed != {
                'receipt/SKILL.md', 'receipt/references/existing-fix.md'}:
            raise ValueError('Expected only tool-selection guidance changes')
        manifest['resource_digests'] = {c: run.resource_digest(OUTPUT/c/'skills') for c in conditions}
        save(manifest)
        print('Prepared six cells; native controls passed; no model calls.', flush=True)
        return
    manifest = json.loads((OUTPUT/'run.json').read_text())
    if (manifest['identities'] != identities() or manifest['cases'] != selected or
            manifest['resource_digests'] != {c: run.resource_digest(OUTPUT/c/'skills') for c in conditions}):
        raise ValueError('Prepared inputs/resources changed')
    with (OUTPUT/'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
                       launch_revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        case = selected[index]
        print('Starting ' + condition + '/' + case['id'], flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
            OUTPUT/condition, 'gpt-6-astra', 'medium', 360, disabled,
            skills_root=OUTPUT/condition/'skills', persist_session=True)
        summary = dict(case=case['id'], condition=condition, **{k: result[k] for k in
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
