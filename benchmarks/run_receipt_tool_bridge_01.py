"""Frozen same-skill direct-tool availability pilot; no models during preparation."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_receipt_bridge_base', ROOT/'benchmarks/run_receipt_assertion_api_01.py')
reuse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reuse)
driver = reuse.driver
base = driver.base
base.CONDITIONS = ('cli', 'bridge')
base.RESOURCES = {condition: 'b081240e' for condition in base.CONDITIONS}
base.SCHEDULE = [(0,'cli'),(0,'bridge'),(1,'bridge'),(1,'cli')]
BRIDGE_CONDITIONS = ('bridge',)
SDK_PYTHON = Path('/tmp/qh-tool-bridge-env-01/bin/python')
SERVER = ROOT/'benchmarks/results/tool-bridge-http-exit-01/server.py'
original_cases = base.cases
def cases():
    values = original_cases()
    for case in values:
        case['task'] += '\nLaunch-supplied loopback project tools, if present, are authorized local facilities. Their host runtime may use separately installed dependencies; the specified native project interpreter and standard-library test requirement still apply. No particular facility is required.\n'
    return values
base.cases = cases
original_identities, original_frozen = base.identities, base.frozen
def identities():
    result = original_identities()
    for name in ('benchmarks/run_receipt_tool_bridge_01.py', 'benchmarks/RECEIPT-TOOL-BRIDGE-01-PROTOCOL.md',
                 'benchmarks/results/tool-bridge-http-exit-01/server.py',
                 'benchmarks/results/tool-bridge-native-prototype-01/requirements.lock'):
        result['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result
def frozen(output):
    result = original_frozen(output)
    result.update(condition_models={c:'gpt-6-astra' for c in base.CONDITIONS},
        condition_flags={c:['--disable','apps','-c','features.code_mode.excluded_tool_namespaces=["web","imagegen","clock"]'] for c in base.CONDITIONS},
        bridge_conditions=list(BRIDGE_CONDITIONS),
        sdk_runtime=str(SDK_PYTHON), sdk_version=subprocess.check_output([str(SDK_PYTHON),'-c','import importlib.metadata;print(importlib.metadata.version("mcp"))'],text=True).strip())
    return result
base.identities, base.frozen = identities, frozen

def execute(output, manifest):
    def unchanged():
        return all(manifest.get(key)==value for key,value in frozen(output).items())
    if not unchanged() or manifest['completed_cells'] or manifest['stopped_after_limit']:
        raise ValueError('Frozen inputs changed or already attempted; do not restart')
    with (output/'execution-started.json').open('x') as stream:
        json.dump(dict(revision=base.git('rev-parse','HEAD').decode().strip(),started_at=datetime.now(timezone.utc).isoformat()),stream)
    disabled = base.run.disabled_skills()
    for index, condition in base.SCHEDULE:
        if not unchanged():
            raise ValueError('Frozen inputs changed between cells')
        case = manifest['cases'][index]
        server = None
        setup_seconds = 0
        log_path = output/f'{case["id"]}-{condition}-server.log'
        print('Starting '+case['id']+' / '+condition,flush=True)
        def launcher(workspace, args):
            nonlocal server, setup_seconds
            flags = frozen(output)['condition_flags'][condition]
            # Both arms replace scoped MCP configuration. Only bridge adds a target.
            table = 'mcp_servers={}'
            if condition in BRIDGE_CONDITIONS:
                started = time.monotonic()
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
                helper = output/condition/'skills/receipt/scripts/compare.py'
                with log_path.open('w') as log:
                    server = subprocess.Popen([str(SDK_PYTHON),'-B',str(SERVER),'--source',str(workspace),
                        '--helper',str(helper),'--python',sys.executable,'--port',str(port)],stdout=log,stderr=log,start_new_session=True)
                deadline = time.monotonic()+10
                while True:
                    try:
                        with socket.create_connection(('127.0.0.1',port),timeout=.1): break
                    except OSError:
                        if server.poll() is not None or time.monotonic()>=deadline:
                            raise RuntimeError('Bridge startup failed; preserve attempt, no retry')
                        time.sleep(.02)
                setup_seconds = time.monotonic()-started
                table = f'mcp_servers={{ qh_receipt_bridge_01={{url="http://127.0.0.1:{port}/mcp",enabled_tools=["receipt_compare"],tool_timeout_sec=40}} }}'
            return args[:2]+flags+['-c',table]+args[2:]
        cleanup_started = None
        try:
            result = base.run.run_cell(case,'skill',1,output/condition,'gpt-6-astra','medium',360,disabled,
                skills_root=output/condition/'skills',workspace_root=output/'workspaces'/condition,
                persist_session=True,launcher=launcher,launcher_execution='host-workspace-write-scoped-mcp')
        finally:
            cleanup_started = time.monotonic()
            if server is not None and server.poll() is None:
                server.send_signal(signal.SIGTERM)
                # Native default helper timeout30 may still drain after model timeout.
                server.wait(timeout=35)
        cleanup_seconds = time.monotonic()-cleanup_started
        cell = dict(case_id=case['id'],condition=condition,
            **{key:result[key] for key in ('completed','timed_out','limit_detected','usage','elapsed_seconds')},
            bridge_setup_seconds=round(setup_seconds,3),bridge_cleanup_seconds=round(cleanup_seconds,3),
            elapsed_including_bridge_lifecycle_seconds=round(result['elapsed_seconds']+setup_seconds+cleanup_seconds,3),
            bridge_exit_code=None if server is None else server.returncode)
        manifest['completed_cells'].append(cell)
        manifest['stopped_after_limit']=bool(result['limit_detected'])
        manifest['stopped_after_uncompleted']=not result['completed']
        (output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(json.dumps(cell),flush=True)
        if result['limit_detected'] or not result['completed']: break
    manifest['finished_at']=datetime.now(timezone.utc).isoformat()
    (output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if args.execute: execute(output,json.loads((output/'run.json').read_text()))
    else:
        base.prepare(output)
        print('Prepared four same-resource tool-availability cells; zero models.')
