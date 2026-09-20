"""Freeze and execute four Receipt support-routing comparison sessions, once."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
from receipt_ledger_cases import cases
from receipt_route_candidate import snapshot, RESOURCE
from run_hostage_buffer_01 import git
import run

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'benchmarks/local-runs/receipt-route-01'
CONDITIONS=('original','candidate')
SCHEDULE=[(0,'original'),(0,'candidate'),(1,'candidate'),(1,'original')]


def identities():
    names=('benchmarks/run_receipt_route_01.py','benchmarks/receipt_route_candidate.py','benchmarks/receipt_read_candidate.py',
           'benchmarks/receipt_ledger_cases.py','benchmarks/receipt-ledger-cases.json',
           'benchmarks/RECEIPT-ROUTE-01-PROTOCOL.md','benchmarks/run.py',
           'skills/receipt/scripts/compare.py')
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in names}


def preflight():
    path=ROOT/'skills/receipt/scripts/compare.py'
    assert path.read_bytes()==git('show',RESOURCE+':skills/receipt/scripts/compare.py')
    spec=importlib.util.spec_from_file_location('receipt_read_preflight',path)
    helper=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows=[]
    assert cases()==json.loads((ROOT/'benchmarks/receipt-ledger-cases.json').read_text())
    for case,after_exit in zip(cases(),(0,1)):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs',prefix='read-preflight-') as scratch:
            project=Path(scratch)/'project'
            run.prepare(case,project)
            before=helper.tree_inventory(project)
            recipe=dict(fixed=['checks','ledger/schema.sql','ledger/__init__.py'],
                vary=['ledger/delivery.py'],before='HEAD^',after='HEAD',
                imports=['ledger.delivery','checks.test_delivery'],runner='unittest',
                tests=['-v','checks.test_delivery'],invocation='module',guard_tree=True)
            result=helper.compare(project,recipe)
            for phase,expected in [('before',1),('after',after_exit)]:
                check=result['checks'][phase]
                assert check['exit_code']==expected and check['native_exit_code']==expected
                assert check['provenance_ready'] and not check['timed_out'] and not check['output_truncated']
                assert 'Ran 5 tests' in check['output'] and 'ERROR:' not in check['output']
                if expected:
                    assert 'FAILED (failures=2)' in check['output']
                    assert ('(True, 250) != (False, 125)' if phase=='before' else '(False, 250) != (False, 125)') in check['output']
                for name in ('same_event_different_accounts','distinct_events_same_amount','zero_delta_is_accepted'):
                    assert 'test_'+name in check['output']
                assert check['command'][1:]==['-B','-m','unittest','-v','checks.test_delivery']
            assert result['tree_guard']['unchanged'] and result['comparison_copies_removed']
            assert helper.tree_inventory(project)==before
            assert not list(project.glob('.receipt-*')) and not list(project.rglob('*.sqlite'))
            rows.append(dict(case=case['id'],comparison=result))
    return rows


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
        for condition in CONDITIONS:
            snapshot(OUTPUT/condition,candidate=condition=='candidate')
        manifest=dict(resource_revision=git('rev-parse',RESOURCE).decode().strip(),
            identities=identities(),cases=selected,
            schedule=[dict(case=selected[i]['id'],condition=c) for i,c in SCHEDULE],
            model='gpt-6-astra',effort='medium',timeout_seconds=360,repeats=1,jobs=1,
            resource_digests=digests(),native_preflight=controls,completed_cells=[],
            prepared_at=datetime.now(timezone.utc).isoformat(),stopped_after_limit=False)
        for condition in CONDITIONS:
            (OUTPUT/condition/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
        save(manifest)
        print('Prepared four sessions; complete/partial native controls passed; no model calls.',flush=True)
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
