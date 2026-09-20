"""Freeze and execute six original-buffer/current-buffer/no-skill sessions once."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
from hostage_buffer_cases import cases, preflight
import run

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'benchmarks/local-runs/hostage-buffer-01'
REVISIONS={'original':'83c138b','current':'3083086'}
SCHEDULE=[(0,'baseline'),(0,'original'),(0,'current'),
          (1,'current'),(1,'original'),(1,'baseline')]


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def identities():
    names=('benchmarks/run_hostage_buffer_01.py','benchmarks/hostage_buffer_cases.py',
           'benchmarks/HOSTAGE-BUFFER-01-PROTOCOL.md','benchmarks/run.py')
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def snapshot(directory,revision):
    for entry in git('ls-tree','-r',revision,'--','skills/hostage-negotiator').decode().splitlines():
        info,name=entry.split('\t',1)
        mode,kind,oid=info.split()
        if kind!='blob' or mode not in ('100644','100755'):
            raise ValueError('Unsupported resource')
        path=directory/name
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file','blob',oid))
        path.chmod(int(mode[-3:],8))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    selected=cases()
    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
    def digests():
        return {c:run.resource_digest(OUTPUT/c/'skills') for c in ('baseline','original','current')}
    if not args.execute:
        controls=preflight()
        OUTPUT.mkdir(parents=True,exist_ok=False)
        for condition in ('baseline','original','current'):
            directory=OUTPUT/condition
            directory.mkdir()
            if condition!='baseline': snapshot(directory,REVISIONS[condition])
        manifest=dict(resource_revisions={c:git('rev-parse',r).decode().strip() for c,r in REVISIONS.items()},
            identities=identities(),cases=selected,
            schedule=[dict(case=selected[i]['id'],condition=c) for i,c in SCHEDULE],
            model='gpt-6-astra',effort='medium',timeout_seconds=360,repeats=1,jobs=1,
            resource_digests=digests(),native_preflight=controls,completed_cells=[],
            prepared_at=datetime.now(timezone.utc).isoformat(),stopped_after_limit=False)
        for condition in ('baseline','original','current'):
            (OUTPUT/condition/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
        save(manifest)
        print('Prepared six cells; native correct/fault/valid-alternative controls passed; no model calls.',flush=True)
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
