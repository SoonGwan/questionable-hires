"""Controlled termination of an owned server; preserve adverse cleanup evidence."""
import asyncio
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[3]
SERVER=Path(__file__).with_name('server.py')
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
PYTHON='/tmp/qh-validation-env/bin/python'

def state(pid):
    r=subprocess.run(['ps','-p',str(pid),'-o','stat='],capture_output=True,text=True)
    value=r.stdout.strip()
    return dict(exists=bool(value),state=value,live=bool(value) and not value.startswith('Z'))

async def check():
    child=None;server=None
    with tempfile.TemporaryDirectory(prefix='qh-bridge-forced-') as temp:
        root=Path(temp)/'project';run.prepare(cases(PYTHON)[0],root)
        tests=root/'test_windows.py';tests.write_text(tests.read_text()+'''\nimport os, pathlib, time\ndef setUpModule():\n    pathlib.Path(__file__).with_name('native-pid.txt').write_text(str(os.getpid()))\n    time.sleep(10)\n''')
        original=run.resource_manifest(root)
        log=Path(__file__).with_name('server-reading.txt')
        with log.open('w') as errors:
            server=await asyncio.create_subprocess_exec(sys.executable,'-B',str(SERVER),'--source',str(root),'--helper',str(ROOT/'skills/receipt/scripts/compare.py'),'--python',PYTHON,stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=errors)
            async def send(message):
                server.stdin.write((json.dumps(message)+'\n').encode());await server.stdin.drain()
            try:
                await send(dict(jsonrpc='2.0',id=1,method='initialize',params=dict(protocolVersion='2025-11-25',capabilities={},clientInfo=dict(name='owned-forced-exit-control',version='1'))))
                response=json.loads(await asyncio.wait_for(server.stdout.readline(),5));assert response['id']==1 and 'result' in response
                await send(dict(jsonrpc='2.0',method='notifications/initialized'))
                recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD^',after='HEAD',imports=['windows','test_windows'],tests=['-v','test_windows'],invocation='module',observe_assertions=True,guard_tree=True)
                await send(dict(jsonrpc='2.0',id=2,method='tools/call',params=dict(name='receipt_compare',arguments=dict(recipe=recipe,timeout=2))))
                deadline=time.monotonic()+5;markers=[]
                while not markers:
                    assert server.returncode is None and time.monotonic()<deadline
                    await asyncio.sleep(0.01);markers=list(root.glob('.receipt-*/before/native-pid.txt'))
                child=int(markers[0].read_text());before=state(child);assert before['live']
                server.send_signal(signal.SIGTERM);await asyncio.wait_for(server.wait(),5)
                child_after=state(child);scratch=[p.name for p in root.glob('.receipt-*')]
                result=dict(checkpoint='tool-bridge-forced-exit-01',date='2026-09-27',server_sha256=hashlib.sha256(SERVER.read_bytes()).hexdigest(),native_started_before_termination=True,server_exit=server.returncode,child_after_server_exit=child_after,owned_scratch_after_exit=scratch,original_inventory_unchanged_before_owned_cleanup=run.resource_manifest(root)==original,models=0,accepted=True,limitation='One real owned SIGTERM control, not arbitrary crash/platform coverage. Native outcome unavailable; server exited before result. Server terminates without native result, not repair proof. Cleanup observed before author intervention. SIGKILL and longer batches unverified.')
                assert server.returncode==128+signal.SIGTERM and not child_after['live'] and not scratch
                assert run.resource_manifest(root)==original
                Path(__file__).with_name('result.json').write_text(redact_paths(json.dumps(result,indent=2))+'\n')
                print('SIGTERM candidate exits143 after native cleanup; child terminal, no scratch and original inventory unchanged')
            finally:
                if server.returncode is None:
                    server.terminate();await asyncio.wait_for(server.wait(),5)
                if child and state(child)['live']:
                    os.killpg(child,signal.SIGTERM)
                    deadline=time.monotonic()+5
                    while state(child)['live']:
                        assert time.monotonic()<deadline
                        await asyncio.sleep(0.02)
                print('Controlled child terminal; owned project cleaned by author temporary-directory context')
        log.write_text(redact_paths(log.read_text()))
asyncio.run(check())
