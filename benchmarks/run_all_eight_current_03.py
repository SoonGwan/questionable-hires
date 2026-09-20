"""Frozen current-bundle regression/efficiency screen on eight exposed tasks."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from lean_screen_cases import cases, source_hashes
from preflight_lean_screen import check as preflight
from run_sqlite_debit_01 import ROOT,git
import run

RESOURCE='ee5eb28'
OUTPUT=ROOT/'benchmarks/local-runs/all-eight-current-03'


def schedule(selected):
    if len(selected)!=8 or len({c['skill'] for c in selected})!=8:
        raise ValueError('Expected eight distinct role tasks')
    return [dict(case=c['id'],condition=condition) for index,c in enumerate(selected)
            for condition in (('baseline','current') if index%2==0 else ('current','baseline'))]


def identities():
    names=('benchmarks/run_all_eight_current_03.py','benchmarks/ALL-EIGHT-CURRENT-03-PROTOCOL.md',
           'benchmarks/preflight_lean_screen.py','benchmarks/run.py')
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def snapshot(directory):
    for entry in git('ls-tree','-r',RESOURCE,'--','skills').decode().splitlines():
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
    if 'REQUEST_RETRIES' in os.environ:
        raise ValueError('Runtime task requires absent REQUEST_RETRIES; host setting unchanged')
    selected=cases()
    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
    def digests():
        return {c:run.resource_digest(OUTPUT/c/'skills') for c in ('baseline','current')}
    if not args.execute:
        controls=preflight()
        OUTPUT.mkdir(parents=True,exist_ok=False)
        for condition in ('baseline','current'):
            directory=OUTPUT/condition
            directory.mkdir()
            if condition=='current':
                snapshot(directory)
        manifest=dict(resource_revision=git('rev-parse',RESOURCE).decode().strip(),
            cases=selected,source_hashes=source_hashes(),identities=identities(),schedule=schedule(selected),
            resource_digests=digests(),model='gpt-6-astra',effort='medium',jobs=1,repeats=1,
            timeout_seconds=360,session_persistence_requested=True,completed_cells=[],
            prepared_at=datetime.now(timezone.utc).isoformat(),stopped_after_limit=False)
        (OUTPUT/'preflight.json').write_text(json.dumps(controls,indent=2,default=lambda value:{'blob_hex':value.hex()})+'\n')
        for condition in ('baseline','current'):
            (OUTPUT/condition/'run.json').write_text(json.dumps(dict(manifest,condition=condition),indent=2)+'\n')
        save(manifest)
        print('Prepared 16 sessions; eight native fixture controls verified; no model calls.',flush=True)
        return
    manifest=json.loads((OUTPUT/'run.json').read_text())
    if (manifest['cases']!=selected or manifest['source_hashes']!=source_hashes()
            or manifest['identities']!=identities() or manifest['resource_digests']!=digests()):
        raise ValueError('Frozen inputs/resources changed')
    with (OUTPUT/'execution-started.json').open('x') as stream:
        json.dump(dict(revision=git('rev-parse','HEAD').decode().strip(),started_at=datetime.now(timezone.utc).isoformat()),stream)
    by_id={c['id']:c for c in selected}
    disabled=run.disabled_skills()
    for cell in manifest['schedule']:
        condition=cell['condition']
        print('Starting '+condition+'/'+cell['case'],flush=True)
        result=run.run_cell(by_id[cell['case']],'baseline' if condition=='baseline' else 'skill',1,
            OUTPUT/condition,'gpt-6-astra','medium',360,disabled,
            skills_root=OUTPUT/condition/'skills',persist_session=True)
        row=dict(cell,**{k:result[k] for k in ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
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
