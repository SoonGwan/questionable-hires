"""Freeze six path-disclosure audit cells and execute them at most once."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from con_artist_discovery_case import cases, preflight
from con_artist_discovery_candidate import RESOURCE, snapshot
from run_hostage_buffer_01 import git
import run

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/'benchmarks/local-runs/con-artist-discovery-01'
CONDITIONS = ('baseline', 'original', 'candidate')
SCHEDULE = ((0,'baseline'), (0,'original'), (0,'candidate'),
            (1,'candidate'), (1,'original'), (1,'baseline'))


def identities():
    names = ('run_con_artist_discovery_01.py', 'con_artist_discovery_case.py',
             'con_artist_discovery_candidate.py', 'run_con_artist_repository_01.py',
             'run_hostage_buffer_01.py', 'run.py', 'CON-ARTIST-DISCOVERY-01-PROTOCOL.md')
    return {name:hashlib.sha256((ROOT/'benchmarks'/name).read_bytes()).hexdigest() for name in names}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    selected = cases()
    expected = dict(resource_revision=git('rev-parse', RESOURCE).decode().strip(),
        cases=selected, identities=identities(), model='gpt-6-astra', effort='medium',
        timeout_seconds=360, repeats=1, jobs=1, session_persistence_requested=True,
        schedule=[dict(case=selected[i]['id'], condition=c) for i,c in SCHEDULE])

    def digests():
        return {c:run.resource_digest(OUTPUT/c/'skills') for c in CONDITIONS}

    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest, indent=2)+'\n')

    if not args.execute:
        controls = preflight()
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT/'baseline').mkdir()
        for condition in CONDITIONS[1:]:
            snapshot(OUTPUT/condition, candidate=condition=='candidate')
        manifest = dict(expected, resource_digests=digests(), native_preflight=controls,
            completed_cells=[], stopped_after_limit=False,
            prepared_at=datetime.now(timezone.utc).isoformat())
        for condition in CONDITIONS:
            (OUTPUT/condition/'run.json').write_text(json.dumps(dict(manifest, condition=condition), indent=2)+'\n')
        save(manifest)
        print('Prepared six cells; four native controls passed; no model calls.', flush=True)
        return
    manifest = json.loads((OUTPUT/'run.json').read_text())
    if (any(manifest.get(k) != value for k,value in expected.items())
            or manifest['resource_digests'] != digests()):
        raise ValueError('Frozen inputs/resources/schedule changed')
    with (OUTPUT/'execution-started.json').open('x') as stream:
        json.dump(dict(revision=git('rev-parse','HEAD').decode().strip(),
                       started_at=datetime.now(timezone.utc).isoformat()), stream)
    disabled = run.disabled_skills()
    for index,condition in SCHEDULE:
        case = selected[index]
        print('Starting '+condition+'/'+case['id'], flush=True)
        result = run.run_cell(case, 'baseline' if condition=='baseline' else 'skill', 1,
            OUTPUT/condition, 'gpt-6-astra', 'medium', 360, disabled,
            skills_root=OUTPUT/condition/'skills', persist_session=True)
        row = dict(case=case['id'], condition=condition, **{k:result[k] for k in
            ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed_cells'].append(row)
        save(manifest)
        print(json.dumps(row), flush=True)
        if result.get('limit_detected'):
            manifest['stopped_after_limit'] = True
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    save(manifest)


if __name__ == '__main__':
    main()
