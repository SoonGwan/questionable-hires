"""Freeze and execute two Con Artist repository-audit comparison sessions, once."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
from con_artist_repository_case import cases, preflight
REVISIONS={'current':'ee51757'}
from run_hostage_buffer_01 import git
import run

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'benchmarks/local-runs/con-artist-repository-01'
CONDITIONS=('baseline','current')
SCHEDULE=[(0,'baseline'),(0,'current')]



def snapshot(directory,revision):
    for entry in git('ls-tree','-r',revision,'--','skills/con-artist').decode().splitlines():
        info,name=entry.split('\t',1)
        mode,kind,oid=info.split()
        if kind!='blob' or mode not in ('100644','100755'):
            raise ValueError('Unsupported resource')
        path=directory/name
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file','blob',oid))
        path.chmod(int(mode[-3:],8))

def identities():
    names=('benchmarks/run_con_artist_repository_01.py',
           'benchmarks/con_artist_repository_case.py','tests/test_con_artist_repository_case.py',
           'benchmarks/CON-ARTIST-REPOSITORY-01-PROTOCOL.md','benchmarks/run.py')
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in names}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    selected=cases()
    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
    def digests():
        return {c:run.resource_digest(OUTPUT/c/'skills') for c in CONDITIONS}
    if not args.execute:
        controls=preflight()
        OUTPUT.mkdir(parents=True,exist_ok=False)
        (OUTPUT/'baseline').mkdir()
        for condition in CONDITIONS[1:]:
            snapshot(OUTPUT/condition,REVISIONS[condition])
        manifest=dict(resource_revisions={c:git('rev-parse',r).decode().strip() for c,r in REVISIONS.items()},
            identities=identities(),cases=selected,
            schedule=[dict(case=selected[i]['id'],condition=c) for i,c in SCHEDULE],
            model='gpt-6-astra',effort='medium',timeout_seconds=360,repeats=1,jobs=1,
            resource_digests=digests(),native_preflight=controls,completed_cells=[],
            prepared_at=datetime.now(timezone.utc).isoformat(),stopped_after_limit=False)
        for condition in CONDITIONS:
            (OUTPUT/condition/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
        save(manifest)
        print('Prepared two sessions; repository native correct/fault controls passed; no model calls.',flush=True)
        return
    manifest=json.loads((OUTPUT/'run.json').read_text())
    if manifest['identities']!=identities() or manifest['cases']!=selected or manifest['resource_digests']!=digests():
        raise ValueError('Frozen inputs/resources changed')
    with (OUTPUT/'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),revision=git('rev-parse','HEAD').decode().strip()),stream)
    disabled=run.disabled_skills()
    for index,condition in SCHEDULE:
        case=selected[index]
        print('Starting '+condition+'/'+case['id'],flush=True)
        result=run.run_cell(case,'baseline' if condition=='baseline' else 'skill',1,
            OUTPUT/condition,'gpt-6-astra','medium',360,disabled,
            skills_root=OUTPUT/condition/'skills',persist_session=True)
        row=dict(case=case['id'],condition=condition,**{k:result[k] for k in
            ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed_cells'].append(row)
        save(manifest)
        print(json.dumps(row),flush=True)
        if result.get('limit_detected'):
            manifest['stopped_after_limit']=True
            break
    manifest['finished_at']=datetime.now(timezone.utc).isoformat()
    save(manifest)


if __name__=='__main__':
    main()
