"""Frozen six-cell development comparison; prepare before one exclusive execution."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
from hostage_modes_candidate import ROOT, RESOURCE, snapshot
from hostage_refresh_cases import cases as refresh_cases, preflight
from korean_auto_cases import cases as korean_cases
import run

OUTPUT=ROOT/'benchmarks/local-runs/hostage-modes-01'
SCHEDULE=[(0,'baseline'),(0,'original'),(0,'candidate'),
          (1,'candidate'),(1,'original'),(1,'baseline')]


def cases():
    return [next(c for c in korean_cases() if c['id']=='ko-label-change'),refresh_cases()[0]]


def identities():
    names=['benchmarks/hostage_modes_candidate.py','benchmarks/run_hostage_modes_01.py',
           'benchmarks/hostage_refresh_cases.py','benchmarks/korean_auto_cases.py','benchmarks/cases.json',
           'benchmarks/HOSTAGE-MODES-01-PROTOCOL.md','benchmarks/run.py']
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    selected=cases()
    def save(manifest):
        (OUTPUT/'run.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    def digests():
        return {c:run.resource_digest(OUTPUT/c/'skills') for c in ('baseline','original','candidate')}
    if not args.execute:
        controls=preflight()
        OUTPUT.mkdir(parents=True,exist_ok=False)
        for condition in ('baseline','original','candidate'):
            directory=OUTPUT/condition
            directory.mkdir()
            if condition!='baseline':
                snapshot(directory,candidate=condition=='candidate')
        manifest=dict(resource_revision=RESOURCE,identities=identities(),cases=selected,
            schedule=[dict(case=selected[i]['id'],condition=c) for i,c in SCHEDULE],
            model='gpt-6-astra',effort='medium',timeout_seconds=300,repeats=1,jobs=1,
            resource_digests=digests(),native_preflight=controls,completed_cells=[],
            prepared_at=datetime.now(timezone.utc).isoformat())
        for condition in ('baseline','original','candidate'):
            (OUTPUT/condition/'run.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        save(manifest)
        print('Prepared six cells; native positive/negative controls passed; no model calls.',flush=True)
        return
    manifest=json.loads((OUTPUT/'run.json').read_text())
    if manifest['identities']!=identities() or manifest['cases']!=selected or manifest['resource_digests']!=digests():
        raise ValueError('Frozen inputs/resources changed')
    with (OUTPUT/'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
            revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()),stream)
    disabled=run.disabled_skills()
    for index,condition in SCHEDULE:
        case=selected[index]
        print('Starting '+condition+'/'+case['id'],flush=True)
        result=run.run_cell(case,'baseline' if condition=='baseline' else 'skill',1,
            OUTPUT/condition,'gpt-6-astra','medium',300,disabled,
            skills_root=OUTPUT/condition/'skills',persist_session=True)
        row=dict(case=case['id'],condition=condition,**{k:result[k] for k in
            ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed_cells'].append(row)
        save(manifest)
        print(json.dumps(row),flush=True)
        if result.get('limit_detected'):
            break
    manifest['finished_at']=datetime.now(timezone.utc).isoformat()
    save(manifest)


if __name__=='__main__':
    main()
