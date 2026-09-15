"""Prepare once, then execute the frozen three-cell real HTTPX development probe."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from httpx_receipt_json_case import HEAD, case as make_case
from lean_entries import rewrite_entry
from run_sqlite_debit_01 import ROOT, git
import run

BASE = '13394dc2491d9d85e0957ea7855ce1e7f330af3a'
ORDER = ('lean', 'baseline', 'current')
OUTPUT = ROOT / 'benchmarks/local-runs/httpx-json-01'


def snapshot(directory, lean=False):
    for entry in git('ls-tree', '-r', BASE, '--', 'skills/receipt').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported skill resource')
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = git('cat-file', 'blob', oid)
        if lean and path.name == 'SKILL.md':
            data = rewrite_entry('receipt', data)
        path.write_bytes(data)
        path.chmod(int(mode[-3:], 8))


def validate_source(source):
    def source_git(*args):
        return subprocess.check_output(['git', *args], cwd=source, text=True).strip()
    preflight = json.loads((ROOT / 'benchmarks/httpx-receipt-json-02-preflight.json').read_text())
    if (source_git('rev-parse', 'HEAD') != HEAD or source_git('status', '--porcelain')
            or source_git('rev-parse', '--is-shallow-repository') != 'false'):
        raise ValueError('Requires pinned clean full-history source')
    names = source_git('ls-files').splitlines()
    actual = {name: dict(sha256=hashlib.sha256((source/name).read_bytes()).hexdigest(),
                         mode=(source/name).stat().st_mode & 0o777) for name in names}
    if actual != preflight['source_inventory']:
        raise ValueError('Source differs from native preflight')
    if hashlib.sha256(git('show', BASE + ':skills/receipt/scripts/compare.py')).hexdigest() != preflight['helper_sha256']:
        raise ValueError('Frozen helper differs from native preflight')


def identities():
    return {name: hashlib.sha256((ROOT/'benchmarks'/name).read_bytes()).hexdigest()
            for name in ('run_httpx_json_01.py', 'httpx_receipt_json_case.py',
                         'lean_entries.py', 'HTTPX-JSON-01-PROTOCOL.md',
                         'httpx-receipt-json-02-preflight.json', 'run.py')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help='Execute the already prepared probe exactly once')
    args = parser.parse_args()
    source, python = args.source.resolve(), args.python.absolute()
    validate_source(source)
    if not python.is_file():
        parser.error('Existing interpreter required')
    case = make_case(str(python))
    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest, indent=2)+'\n')
    if not args.execute:
        OUTPUT.mkdir(parents=True, exist_ok=False)
        manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                        resource_revision=BASE, source=str(source), case=case,
                        identities=identities(), schedule=list(ORDER),
                        model='gpt-6-astra', effort='medium', repeats=1, jobs=1,
                        timeout_seconds=360, session_persistence_requested=True,
                        prepared_at=datetime.now(timezone.utc).isoformat(), completed_cells=[])
        for condition in ORDER:
            directory = OUTPUT/condition
            directory.mkdir()
            if condition != 'baseline':
                snapshot(directory, lean=condition == 'lean')
            (directory/'run.json').write_text(json.dumps(dict(manifest, condition=condition), indent=2)+'\n')
        current = run.resource_manifest(OUTPUT/'current/skills')
        lean = run.resource_manifest(OUTPUT/'lean/skills')
        changed = [name for name in current if current[name] != lean.get(name)]
        if set(current) != set(lean) or changed != ['receipt/SKILL.md']:
            raise ValueError('Expected only the Receipt entry to differ')
        manifest['resource_digests'] = {c: run.resource_digest(OUTPUT/c/'skills') for c in ORDER}
        save(manifest)
        print('Prepared three cells; no model calls. Use --execute once after review.', flush=True)
        return
    manifest = json.loads((OUTPUT/'run.json').read_text())
    if (manifest['identities'] != identities() or manifest['case'] != case
            or manifest['source'] != str(source)
            or manifest['resource_digests'] != {c: run.resource_digest(OUTPUT/c/'skills') for c in ORDER}):
        raise ValueError('Prepared inputs/resources changed')
    # Exclusive marker prevents a second execution, including after interruption.
    # A marker is not liveness evidence: inspect the original process/streams.
    with (OUTPUT/'execution-started.json').open('x') as marker:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat()), marker)
    disabled = run.disabled_skills()
    for condition in ORDER:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
                              OUTPUT/condition, 'gpt-6-astra', 'medium', 360, disabled,
                              skills_root=OUTPUT/condition/'skills', project_source=source,
                              persist_session=True)
        summary = dict(condition=condition, **{k: result[k] for k in
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
