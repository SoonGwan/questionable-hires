"""Real SDK cancellation notifications and subsequent native recovery."""
import asyncio
import hashlib
from contextlib import asynccontextmanager
import signal
import socket
from datetime import timedelta
import json
from pathlib import Path
import sys
import tempfile
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CancelledNotification, CancelledNotificationParams, ClientNotification
from mcp.shared.exceptions import McpError
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
SERVER=ROOT/'benchmarks/results/tool-bridge-http-exit-01/server.py'
PYTHON='/tmp/qh-validation-env/bin/python'

@asynccontextmanager
async def http_transport(root):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    log=Path(__file__).with_name(root.name+'-server-reading.txt')
    with log.open('w') as errors:
        process=await asyncio.create_subprocess_exec(sys.executable,'-B',str(SERVER),'--source',str(root),'--helper',str(ROOT/'skills/receipt/scripts/compare.py'),'--python',PYTHON,'--port',str(port),stdout=errors,stderr=errors)
        try:
            deadline=time.monotonic()+10
            while True:
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=0.1):break
                except OSError:
                    assert process.returncode is None and time.monotonic()<deadline
                    await asyncio.sleep(0.02)
            async with streamable_http_client(f'http://127.0.0.1:{port}/mcp') as (read,write,get_id):
                yield read,write
        finally:
            if process.returncode is None:
                process.send_signal(signal.SIGTERM)
                await asyncio.wait_for(process.wait(),6)
    log.write_text(redact_paths(log.read_text()))

async def started(root,task):
    deadline=time.monotonic()+10
    while not list(root.glob('.receipt-*/before/native-started.txt')):
        assert not task.done() and time.monotonic()<deadline
        await asyncio.sleep(0.01)

async def check():
    evidence=[]
    with tempfile.TemporaryDirectory(prefix='qh-bridge-cancel-') as temp:
        for position in ('active','queued'):
            print('STAGE begin',position,flush=True)
            root=Path(temp)/position;run.prepare(cases(PYTHON)[0],root)
            tests=root/'test_windows.py';tests.write_text(tests.read_text()+'''\nimport pathlib, time\ndef setUpModule():\n    pathlib.Path(__file__).with_name('native-started.txt').write_text('started')\n    time.sleep(0.4)\n''')
            original=run.resource_manifest(root)
            recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD^',after='HEAD',imports=['windows','test_windows'],tests=['-v','test_windows'],invocation='module',observe_assertions=True,guard_tree=True)
            params=StdioServerParameters(command=sys.executable,args=['-B',str(SERVER),'--source',str(root),'--helper',str(ROOT/'skills/receipt/scripts/compare.py'),'--python',PYTHON])
            async with http_transport(root) as (read,write):
                async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=5)) as session:
                    await session.initialize()
                    first_id=session._request_id  # controlled SDK client instrumentation only
                    first=asyncio.create_task(session.call_tool('receipt_compare',{'recipe':recipe}))
                    await started(root,first)
                    print('STAGE native started',position,flush=True)
                    if position=='queued':
                        request_id=session._request_id
                        cancelled=asyncio.create_task(session.call_tool('receipt_compare',{'recipe':recipe}))
                        deadline=time.monotonic()+10
                        while session._request_id==request_id:
                            assert time.monotonic()<deadline
                            await asyncio.sleep(0.01)
                    else:
                        request_id=first_id;cancelled=first
                    await session.send_notification(ClientNotification(CancelledNotification(params=CancelledNotificationParams(requestId=request_id,reason='controlled cancellation'))))
                    print('STAGE cancellation sent',position,flush=True)
                    try:
                        await cancelled
                    except McpError as error:
                        assert 'Request cancelled' in str(error)
                        cancellation=str(error)
                        print('STAGE cancellation error received',position,flush=True)
                    else:
                        raise AssertionError('cancelled call returned success')
                    if position=='queued':
                        initial_result=await first
                        assert not initial_result.isError
                    recovery=await session.call_tool('receipt_compare',{'recipe':recipe})
                    print('STAGE recovery returned',position,flush=True)
                    assert not recovery.isError and recovery.structuredContent is None
                    result=json.loads(recovery.content[0].text)
                    assert result['status']=='observed' and result['tree_guard']['unchanged'] and result['comparison_copies_removed']
                    assert [c['native_exit_code'] for c in result['checks'].values()]==[1,0]
                    assert all(c['suite_observation']['tests']==6 and c['assertion_observation']['complete'] for c in result['checks'].values())
                    assert run.resource_manifest(root)==original and not list(root.glob('.receipt-*'))
                    evidence.append(dict(position=position,cancellation=cancellation,recovery=result,originals_unchanged=True,scratch_removed=True))
                print('STAGE session closed',position,flush=True)
            print('STAGE transport closed',position,flush=True)
            assert run.resource_manifest(root)==original
    value=dict(checkpoint='tool-bridge-http-cancellation-01',date='2026-09-27',server_sha256=hashlib.sha256(SERVER.read_bytes()).hexdigest(),models=0,evidence=evidence,limitation='SDK cancellation/after-recovery proof only. Cancellation acknowledgement is not immediate native interruption or cleanup. Active helper may finish before gate release. Abrupt disconnect/cross-instance/host/all8 efficiency unverified. HTTP listener termination after settled calls observed.')
    Path(__file__).with_name('results.json').write_text(redact_paths(json.dumps(value,indent=2))+'\n')
    print('Active and queued real cancellation errors followed by complete native1/0 recovery, original preservation and cleanup pass')
asyncio.run(check())
