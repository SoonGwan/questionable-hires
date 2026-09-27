"""Frozen paired history-review development screen; no retries or resumption."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
import run
from run_tool_surface_01 import process_wrapper

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = 'ecef2516'
CANDIDATE = 'e5061da5'
CASES = ('history-invoice-01-cases.json', 'necromancer-regions-cases.json')
SCHEDULE = [(0, 'previous'), (0, 'candidate'), (1, 'candidate'), (1, 'previous')]
FLAGS = ['--disable', 'apps', '-c', 'features.code_mode.excluded_tool_namespaces=["web","imagegen","clock"]']
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout=360)

def cases():
    rows = [json.loads((ROOT/'benchmarks'/name).read_text())[0] for name in CASES]
    if [r['id'] for r in rows] != ['history-invoice-boundary','history-three-decisions']:
        raise ValueError('Unexpected frozen case IDs')
    return rows

def frozen(output):
    names = ['benchmarks/'+n for n in CASES] + ['benchmarks/run.py',
        'benchmarks/run_tool_surface_01.py', 'benchmarks/run_necromancer_decision_checks_01.py',
        'benchmarks/NECROMANCER-DECISION-CHECKS-01-PROTOCOL.md',
        'tests/test_necromancer_decision_checks_01.py']
    return dict(cases=cases(),schedule=SCHEDULE,flags=FLAGS,settings=SETTINGS,
        source_hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        resource_digests={c:run.resource_digest(output/c/'skills') for c in ('previous','candidate')},
        python=sys.executable,python_version=sys.version,
        cli_version=subprocess.check_output(['codex','--version'],text=True,timeout=15).strip())

def snapshot(output,condition,revision,prefix):
    listing=subprocess.check_output(['git','-C',str(ROOT),'ls-tree','-r',revision,'--',prefix],text=True)
    for line in listing.splitlines():
        info,name=line.split('\t');mode,kind,oid=info.split()
        if kind!='blob' or mode not in ('100644','100755'):raise ValueError('Unexpected resource entry')
        relative=Path(name).relative_to(prefix);dest=output/condition/'skills'/'necromancer'/relative
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(subprocess.check_output(['git','-C',str(ROOT),'cat-file','blob',oid]))
        dest.chmod(int(mode[-3:],8))
    if not (output/condition/'skills/necromancer/SKILL.md').is_file():raise ValueError('Missing entry')

def preflight():
    records=[]
    for case in cases():
        with tempfile.TemporaryDirectory(prefix='history-controls-',dir=ROOT/'benchmarks') as temp:
            project=Path(temp)/'project';run.prepare(case,project)
            module='test_invoice' if case['id']=='history-invoice-boundary' else 'test_consumer'
            probe="import importlib; m=importlib.import_module('invoice' if 'invoice' in MODULE else 'consumer'); import unittest; result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName(MODULE)); raise SystemExit(not result.wasSuccessful())".replace('MODULE',repr(module))
            passed=subprocess.run([sys.executable,'-B','-c',probe],cwd=project,capture_output=True,text=True,timeout=15)
            path=project/('amounts.py' if module=='test_invoice' else 'summary.py');original=path.read_text()
            broken=original.replace('rounding=ROUND_HALF_UP','rounding=__import__("decimal").ROUND_DOWN') if module=='test_invoice' else original.replace("    if amount < 0:\n        raise ValueError('negative amount')\n",'')
            if broken==original:raise ValueError('Control mutation did not match')
            path.write_text(broken)
            failed=subprocess.run([sys.executable,'-B','-c',probe],cwd=project,capture_output=True,text=True,timeout=15)
            path.write_text(original)
            expected='100 != 101' if module=='test_invoice' else 'ValueError not raised'
            if passed.returncode!=0 or failed.returncode!=1 or expected not in failed.stderr or 'ERROR:' in failed.stderr:
                raise ValueError('Native assertion preflight failed')
            if subprocess.check_output(['git','status','--porcelain'],cwd=project)!=b'':raise ValueError('Fixture drift')
            records.append(dict(case_id=case['id'],pass_exit=passed.returncode,fail_exit=failed.returncode,
                passed=passed.stderr.replace(str(project),'<AUTHOR-COPY>'),failed=failed.stderr.replace(str(project),'<AUTHOR-COPY>')))
    return records

def prepare(output):
    if output.exists():raise FileExistsError(output)
    controls=preflight();output.mkdir(parents=True)
    snapshot(output,'previous',PREVIOUS,'skills/necromancer')
    snapshot(output,'candidate',CANDIDATE,'benchmarks/candidates/necromancer-decision-checks/skills/necromancer')
    manifest=dict(frozen(output),completed_cells=[],stopped=False,prepared_at=datetime.now(timezone.utc).isoformat())
    (output/'preflight.json').write_text(json.dumps(controls,indent=2)+'\n')
    for directory in (output,output/'previous',output/'candidate'):
        (directory/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

def execute(output,manifest):
    def unchanged():
        return all(json.loads(json.dumps(v))==manifest.get(k) for k,v in frozen(output).items())
    if not unchanged() or manifest['completed_cells'] or manifest['stopped']:raise ValueError('Drift or already attempted')
    with (output/'execution-started.json').open('x') as f:json.dump(dict(started_at=datetime.now(timezone.utc).isoformat()),f)
    disabled=run.disabled_skills()
    for index,condition in SCHEDULE:
        if not unchanged():raise ValueError('Frozen drift; do not restart')
        case=manifest['cases'][index];print('Starting '+case['id']+' / '+condition,flush=True)
        with patch.object(run.subprocess,'Popen',new=process_wrapper(run.subprocess.Popen,FLAGS)):
            result=run.run_cell(case,'skill',1,output/condition,SETTINGS['model'],SETTINGS['effort'],SETTINGS['timeout'],disabled,
                skills_root=output/condition/'skills',workspace_root=output/'workspaces'/condition,persist_session=True)
        row=dict(case_id=case['id'],condition=condition,**{k:result[k] for k in ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed_cells'].append(row);manifest['stopped']=bool(result['limit_detected'] or not result['completed'])
        (output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(row),flush=True)
        if manifest['stopped']:break
    manifest['finished_at']=datetime.now(timezone.utc).isoformat();(output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();output=args.output.resolve()
    if args.execute:execute(output,json.loads((output/'run.json').read_text()))
    else:prepare(output);print('Four cells prepared; zero model calls.')
