"""Fixed 24-cell all-eight development screen. No retries or source promotion."""
from datetime import datetime, timezone
import hashlib
import itertools
import json
import os
from pathlib import Path

from lean_entries import rewrite_entry
from lean_screen_cases import cases, source_hashes
from run_sqlite_debit_01 import ROOT, git
import run

BASE = '3aaef96'
CONDITIONS = ('baseline', 'current', 'lean')


def schedule(selected):
    orders = list(itertools.permutations(CONDITIONS))
    # Every permutation occurs once; the final two differ at every position.
    indices = (0, 1, 2, 3, 4, 5, 0, 3)
    if len(selected) != len(indices):
        raise ValueError('The frozen screen requires exactly eight tasks')
    return [dict(case=case['id'], condition=condition)
            for case, index in zip(selected, indices) for condition in orders[index]]


def snapshot(directory, lean=False):
    for entry in git('ls-tree', '-r', BASE, '--', 'skills').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported skill resource')
        path = directory/name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = git('cat-file', 'blob', oid)
        if lean and path.name == 'SKILL.md':
            data = rewrite_entry(path.parent.name, data)
        path.write_bytes(data)
        path.chmod(int(mode[-3:], 8))


def main():
    if 'REQUEST_RETRIES' in os.environ:
        raise ValueError('Runtime case requires unset REQUEST_RETRIES; no host setting changed')
    selected = cases()
    preflight = json.loads((ROOT/'benchmarks/lean-screen-01-preflight.json').read_text())
    if preflight['source_hashes'] != source_hashes():
        raise ValueError('Selected inputs changed since author preflight')
    output = ROOT/'benchmarks/local-runs/lean-screen-01'
    output.mkdir(parents=True, exist_ok=False)
    manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                    base_resource_revision=git('rev-parse', BASE).decode().strip(),
                    started_at=datetime.now(timezone.utc).isoformat(),
                    model='gpt-6-astra', effort='medium', jobs=1, repeats=1,
                    timeout_seconds=360, session_persistence_requested=True,
                    cases=selected, source_hashes=source_hashes(), schedule=schedule(selected),
                    protocol_sha256=hashlib.sha256((ROOT/'benchmarks/LEAN-SCREEN-01-PROTOCOL.md').read_bytes()).hexdigest(),
                    candidate_builder_sha256=hashlib.sha256((ROOT/'benchmarks/lean_entries.py').read_bytes()).hexdigest(),
                    completed_cells=[], stopped_after_limit=False)
    def save():
        (output/'run.json').write_text(json.dumps(manifest, indent=2)+'\n')
    save()
    for condition in CONDITIONS:
        directory = output/condition
        directory.mkdir()
        if condition != 'baseline':
            snapshot(directory, lean=condition == 'lean')
        (directory/'run.json').write_text(json.dumps(dict(manifest, condition=condition,
            skill_resources_sha256=None if condition == 'baseline' else
                {c['skill']: run.resource_digest(directory/'skills'/c['skill']) for c in selected}), indent=2)+'\n')
    # Entry-only experiment: all other resource bytes/modes must match exactly.
    current = run.resource_manifest(output/'current/skills')
    lean = run.resource_manifest(output/'lean/skills')
    if set(current) != set(lean):
        raise ValueError('Candidate resource inventory differs')
    for name in current:
        if not name.endswith('/SKILL.md') and current[name] != lean[name]:
            raise ValueError('Non-entry resource changed: ' + name)
    disabled = run.disabled_skills()
    by_id = {case['id']: case for case in selected}
    for cell in manifest['schedule']:
        condition, case = cell['condition'], by_id[cell['case']]
        print('Starting ' + condition + '/' + case['id'], flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
                              output/condition, 'gpt-6-astra', 'medium', 360, disabled,
                              skills_root=output/condition/'skills', persist_session=True)
        summary = dict(cell, **{k: result[k] for k in
            ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed_cells'].append(summary)
        save()
        print(json.dumps(summary), flush=True)
        if result.get('limit_detected'):
            manifest['stopped_after_limit'] = True
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    save()


if __name__ == '__main__':
    main()
