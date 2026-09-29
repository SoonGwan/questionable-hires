"""Actual loopback HTTP handshake/native/termination controls, no model calls."""
import asyncio
import hashlib
from datetime import timedelta
import json
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import time
from mcp.shared.exceptions import McpError
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
SERVER=Path(__file__).with_name('server.py')
PYTHON='/tmp/qh-validation-env/bin/python'

def state(pid):
    r=subprocess.run(['ps','-p',str(pid),'-o','stat='],capture_output=True,text=True)
    value=r.stdout.strip();return dict(exists=bool(value),state=value,live=bool(value) and not value.startswith('Z'))

async def check():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='qh-bridge-http-') as temp:
        for label in ('ordinary','terminate'):
            root=Path(temp)/label;run.prepare(cases(PYTHON)[0],root)
            if label=='terminate':
                tests=root/'test_windows.py';tests.write_text(tests.read_text()+'''\nimport os, pathlib, time\ndef setUpModule():\n    pathlib.Path(__file__).with_name('native-pid.txt').write_text(str(os.getpid()))\n    time.sleep(10)\n''')
            original=run.resource_manifest(root)
            with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
            log=Path(__file__).with_name(label+'-server-reading.txt');child=None
            with log.open('w') as errors:
                server=await asyncio.create_subprocess_exec(sys.executable,'-B',str(SERVER),'--source',str(root),'--helper',str(ROOT/'skills/receipt/scripts/compare.py'),'--python',PYTHON,'--port',str(port),stdout=errors,stderr=errors)
                try:
                    deadline=time.monotonic()+10
                    while True:
                        try:
                            with socket.create_connection(('127.0.0.1',port),timeout=0.1):break
                        except OSError:
                            assert server.returncode is None and time.monotonic()<deadline
                            await asyncio.sleep(0.02)
                    async with streamable_http_client(f'http://127.0.0.1:{port}/mcp') as (read,write,get_id):
                        async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=4)) as session:
                            initialized=await session.initialize();tools=await session.list_tools()
                            assert [t.name for t in tools.tools]==['receipt_compare']
                            recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD^',after='HEAD',imports=['windows','test_windows'],tests=['-v','test_windows'],invocation='module',observe_assertions=True,guard_tree=True)
                            call=asyncio.create_task(session.call_tool('receipt_compare',dict(recipe=recipe,timeout=2)))
                            if label=='terminate':
                                deadline=time.monotonic()+5;markers=[]
                                while not markers:
                                    assert not call.done() and time.monotonic()<deadline
                                    await asyncio.sleep(0.01);markers=list(root.glob('.receipt-*/before/native-pid.txt'))
                                child=int(markers[0].read_text());assert state(child)['live']
                                server.send_signal(signal.SIGTERM)
                            if label=='ordinary':
                                result=await call;value=json.loads(result.content[0].text)
                                assert not result.isError and value['status']=='observed'
                                assert [c['native_exit_code'] for c in value['checks'].values()]==[1,0]
                                assert all(c['suite_observation']['tests']==6 and c['assertion_observation']['complete'] for c in value['checks'].values())
                                assert value['originals']['unchanged'] and value['comparison_copies_removed'] and value['tree_guard']['unchanged']
                                response=result.model_dump(mode='json')
                            else:
                                await asyncio.wait_for(server.wait(),6)
                                assert not state(child)['live'] and not list(root.glob('.receipt-*'))
                                assert run.resource_manifest(root)==original
                                try:
                                    await call
                                except McpError as error:
                                    assert 'Timed out' in str(error)
                                    response=dict(native_result_available=False,client_error=str(error),complete=False)
                                else:
                                    raise AssertionError('Unexpected success after interrupted HTTP delivery')
                    if label=='ordinary':server.send_signal(signal.SIGTERM)
                    await asyncio.wait_for(server.wait(),6)
                    assert run.resource_manifest(root)==original and not list(root.glob('.receipt-*'))
                    rows.append(dict(condition=label,handshake=initialized.model_dump(mode='json'),result=response,server_exit=server.returncode,child_after_exit=state(child) if child else None,originals_unchanged=True,scratch_removed=True))
                finally:
                    if server.returncode is None:server.kill();await server.wait()
            log.write_text(redact_paths(log.read_text()))
    Path(__file__).with_name('results.json').write_text(redact_paths(json.dumps(dict(checkpoint='tool-bridge-http-exit-01',date='2026-09-27',source_sha256=hashlib.sha256(SERVER.read_bytes()).hexdigest(),rows=rows,models=0,limitation='Controlled loopback HTTP ordinary/SIGTERM draining; not abrupt client loss, SIGKILL, other hosts or all8 efficiency.'),indent=2))+'\n')
    print('HTTP ordinary native1/0 passes; active SIGTERM leaves child terminal/source unchanged/no scratch, but RPC result unavailable with bounded client error')
asyncio.run(check())
