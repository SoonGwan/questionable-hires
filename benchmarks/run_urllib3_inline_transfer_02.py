"""Two frozen real-source history-review cells; no retry or resumption."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
import run
from run_necromancer_decision_checks_01 import snapshot, FLAGS, SETTINGS
from run_tool_surface_01 import process_wrapper
from run_urllib3_history_01 import case, source_identity

ROOT=Path(__file__).resolve().parents[1]
RESOURCES={'previous':('e109ae4a','skills/necromancer'), 'candidate':('80c06e2e','benchmarks/candidates/necromancer-inline-matrix/skills/necromancer')}
SCHEDULE=['previous','candidate']
METADATA='src/urllib3/_version.py'

def fixture_identity(source):
    identity=dict(source_identity(source))
    metadata=source/METADATA
    if metadata.is_symlink() or not metadata.is_file():raise ValueError('Missing genuine generated metadata')
    identity['files']=run.resource_manifest(source,exclude=('.git',))
    return identity

def frozen(source,output):
    names=['benchmarks/run_urllib3_inline_transfer_02.py','benchmarks/run_urllib3_history_01.py',
           'benchmarks/preflight_urllib3_history_01.py','benchmarks/run.py',
           'benchmarks/run_necromancer_decision_checks_01.py','benchmarks/run_tool_surface_01.py',
           'benchmarks/URLLIB3-INLINE-TRANSFER-02-PROTOCOL.md','tests/test_urllib3_inline_transfer_02.py',
           'benchmarks/results/urllib3-inline-transfer-01-native/control.py']
    return dict(case=case(),schedule=SCHEDULE,flags=FLAGS,settings=SETTINGS,
        source_identity=fixture_identity(source),source_hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        resource_revisions=RESOURCES,resource_digests={c:run.resource_digest(output/c/'skills') for c in SCHEDULE},
        python=sys.executable,python_version=sys.version,
        cli_version=subprocess.check_output(['codex','--version'],text=True,timeout=15).strip())

def preflight(source):
    before=fixture_identity(source)
    with tempfile.TemporaryDirectory(prefix='urllib3-transfer02-',dir=ROOT/'benchmarks/local-runs') as temp:
        project=Path(temp)/'project';run.prepare_repository(source,project)
        assert fixture_identity(project)==before
        env=dict(os.environ,PYTHONPATH=str(project/'src'),PYTHONDONTWRITEBYTECODE='1')
        code='import urllib3, urllib3.util.retry; from pathlib import Path; assert Path(urllib3.__file__).resolve()==Path("src/urllib3/__init__.py").resolve(); assert Path(urllib3.util.retry.__file__).resolve()==Path("src/urllib3/util/retry.py").resolve(); assert urllib3.__version__=="2.2.3"; print(urllib3.__version__)'
        imported=subprocess.run([sys.executable,'-B','-c',code],cwd=project,env=env,capture_output=True,text=True,timeout=30)
        observer=subprocess.run([sys.executable,'-B',str(ROOT/'benchmarks/results/urllib3-inline-transfer-01-native/control.py'),'--source',str(project)],cwd=project,env=env,capture_output=True,text=True,timeout=30)
        if imported.returncode or observer.returncode:raise ValueError('Actual copied fixture native gate failed')
        report=json.loads(observer.stdout)
        assert [x['report']['mismatches'] for x in report['original_observations']]==[0,1,1]
        assert fixture_identity(project)==before
    assert fixture_identity(source)==before
    return dict(fresh_import_exit=imported.returncode,version=imported.stdout.strip(),observer=report,copied_fixture_preserved=True)

def prepare(source,output):
    if output.exists():raise FileExistsError(output)
    controls=preflight(source);output.mkdir(parents=True)
    for condition,(revision,prefix) in RESOURCES.items():snapshot(output,condition,revision,prefix)
    manifest=dict(frozen(source,output),completed_cells=[],stopped=False,prepared_at=datetime.now(timezone.utc).isoformat())
    (output/'preflight.json').write_text(json.dumps(controls,indent=2)+'\n')
    for directory in (output,*(output/c for c in SCHEDULE)):(directory/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

def execute(source,output,manifest):
    def unchanged():return all(json.loads(json.dumps(v))==manifest.get(k) for k,v in frozen(source,output).items())
    if not unchanged() or manifest['completed_cells'] or manifest['stopped']:raise ValueError('Frozen drift or already attempted')
    with (output/'execution-started.json').open('x') as f:json.dump(dict(started_at=datetime.now(timezone.utc).isoformat()),f)
    disabled=run.disabled_skills()
    for condition in SCHEDULE:
        if not unchanged():raise ValueError('Frozen drift; do not restart')
        print('Starting urllib3 transfer02 / '+condition,flush=True)
        with patch.object(run.subprocess,'Popen',new=process_wrapper(run.subprocess.Popen,FLAGS)):
            result=run.run_cell(manifest['case'],'skill',1,output/condition,SETTINGS['model'],SETTINGS['effort'],SETTINGS['timeout'],disabled,
                skills_root=output/condition/'skills',project_source=source,workspace_root=output/'workspaces'/condition,persist_session=True)
        row=dict(condition=condition,**{k:result[k] for k in ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed_cells'].append(row);manifest['stopped']=bool(result['limit_detected'] or not result['completed'])
        (output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(row),flush=True)
        if manifest['stopped']:break
    manifest['finished_at']=datetime.now(timezone.utc).isoformat();(output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();source=args.source.resolve();output=args.output.resolve()
    if args.execute:execute(source,output,json.loads((output/'run.json').read_text()))
    else:prepare(source,output);print('Transfer02 prepared; zero model calls.')
