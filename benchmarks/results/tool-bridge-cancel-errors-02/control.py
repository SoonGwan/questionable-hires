"""Owned SDK cancellation/error intersection controls; no model/policy changes."""
import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import sys
import tempfile
import time
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CancelledNotification, CancelledNotificationParams, ClientNotification
from mcp.shared.exceptions import McpError

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
SERVER=OUT/'server.py'
PYTHON='/tmp/qh-validation-env/bin/python'


def phases(log):
    return [json.loads(s[len('NATIVE_PHASE '):]) for s in log.read_text().splitlines()
            if s.startswith('NATIVE_PHASE ')]


def live(pid):
    try: os.kill(pid,0)
    except ProcessLookupError: return False
    return True


@asynccontextmanager
async def transport(root, record):
    with socket.socket() as s:
        s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    log=OUT/(root.name+'-server-reading.txt')
    with log.open('x') as output:
        process=await asyncio.create_subprocess_exec(sys.executable,'-B',str(SERVER),
            '--source',str(root),'--helper',str(ROOT/'skills/receipt/scripts/compare.py'),
            '--python',PYTHON,'--port',str(port),'--phase-cancellation',stdout=output,stderr=output)
        try:
            deadline=time.monotonic()+10
            while True:
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                except OSError:
                    assert process.returncode is None and time.monotonic()<deadline
                    await asyncio.sleep(.02)
            async with streamable_http_client(f'http://127.0.0.1:{port}/mcp') as (read,write,_):
                yield read,write,log
        finally:
            if process.returncode is None:
                process.send_signal(signal.SIGTERM)
                await asyncio.wait_for(process.wait(),6)
            record['server_exit_code']=process.returncode
    log.write_text(redact_paths(log.read_text()))


async def one(root, scenario):
    record=dict(scenario=scenario,passed=False)
    run.prepare(cases(PYTHON)[0],root)
    original=run.resource_manifest(root)
    source=root/'windows.py';tests=root/'test_windows.py'
    original_source=source.read_bytes();original_tests=tests.read_bytes()
    action="time.sleep(10)" if scenario=='timeout' else "time.sleep(.4)\n    with (base.parents[1]/'windows.py').open('ab') as out:\n        out.write(b'\\n# controlled original mutation\\n')"
    tests.write_text(tests.read_text()+"\nimport os, pathlib, time\ndef setUpModule():\n    base=pathlib.Path(__file__).parent\n    (base/'native-started.txt').write_text(str(os.getpid()))\n    "+action+"\n")
    injected=run.resource_manifest(root)
    recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD^',after='HEAD',
                imports=['windows','test_windows'],tests=['-v','test_windows'],
                invocation='module',observe_assertions=True,guard_tree=True)
    try:
        async with transport(root,record) as (read,write,log):
            async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=5)) as session:
                await session.initialize()
                request_id=session._request_id
                request=asyncio.create_task(session.call_tool('receipt_compare',dict(recipe=recipe,timeout=1 if scenario=='timeout' else 3)))
                deadline=time.monotonic()+10
                while not list(root.glob('.receipt-*/before/native-started.txt')):
                    assert not request.done() and time.monotonic()<deadline
                    await asyncio.sleep(.01)
                marker=next(root.glob('.receipt-*/before/native-started.txt'))
                native_pid=int(marker.read_text());record['native_pid']=native_pid
                assert live(native_pid)
                assert not any(e['event']=='end' for e in phases(log))
                if scenario!='guard_uncancelled':
                    await session.send_notification(ClientNotification(CancelledNotification(params=CancelledNotificationParams(requestId=request_id,reason='owned error intersection'))))
                if scenario=='guard_uncancelled':
                    failed=await request
                    record['ordinary_error']=[c.text for c in failed.content if hasattr(c,'text')]
                    assert failed.isError and 'Selected originals changed' in str(record['ordinary_error'])
                else:
                    try:
                        await request
                    except McpError as error:
                        assert 'Request cancelled' in str(error)
                        record['cancellation']=str(error)
                    else: raise AssertionError('Cancelled request returned a comparison')
                deadline=time.monotonic()+6
                while list(root.glob('.receipt-*')) or live(native_pid):
                    assert time.monotonic()<deadline, 'native process or copies still live'
                    await asyncio.sleep(.02)
                record['native_terminal_before_author_reset']=not live(native_pid)
                record['scratch_removed_before_author_reset']=not list(root.glob('.receipt-*'))
                events=phases(log);record['interrupted_phases']=events
                assert [e['phase'] for e in events if e['event']=='start']==(['before','after'] if scenario=='guard_uncancelled' else ['before'])
                assert [e['event'] for e in events]==(['start','end']*(2 if scenario=='guard_uncancelled' else 1))
                current=run.resource_manifest(root)
                changed=sorted(p for p in current.keys()|injected.keys() if current.get(p)!=injected.get(p))
                record['changed_before_author_reset']=changed
                assert changed==(['windows.py'] if scenario.startswith('guard') else [])
                if scenario=='timeout':assert events[-1]['timed_out']
                else:
                    assert not events[-1]['timed_out']
                    # SDK logging can arrive just after copy cleanup. Readiness is
                    # determined by a short bounded diagnostic wait, not a rerun.
                    deadline=time.monotonic()+2
                    while 'Selected originals changed' not in log.read_text() and time.monotonic()<deadline:
                        await asyncio.sleep(.02)
                    record['guard_error_logged']='Selected originals changed' in log.read_text()
                    assert record['guard_error_logged'], 'original-change failure not visible in server log'
                source.write_bytes(original_source);tests.write_bytes(original_tests)
                record['author_reset_owned_fault_fixture']=True
                assert run.resource_manifest(root)==original
                recovered=await session.call_tool('receipt_compare',dict(recipe=recipe,timeout=3))
                assert not recovered.isError and recovered.structuredContent is None
                result=json.loads(recovered.content[0].text);record['recovery']=result
                assert result['status']=='observed' and result['tree_guard']['unchanged'] and result['comparison_copies_removed']
                assert [c['native_exit_code'] for c in result['checks'].values()]==[1,0]
                for c in result['checks'].values():
                    assert c['suite_observation']['tests']==6 and c['suite_observation']['skipped']==0
                    assert c['assertion_observation']['complete'] and c['assertion_observation']['v']==3
                    assert len(c['assertion_observation']['observations'])==7
                assert run.resource_manifest(root)==original and not list(root.glob('.receipt-*'))
                record['recovery_originals_preserved']=True
                assert 'Request already responded to' not in log.read_text()
                record['no_duplicate_response_error']=True
        record['passed']=True
    except BaseException as error:
        record['control_error']=repr(error)
    finally:
        log=OUT/(root.name+'-server-reading.txt')
        if log.exists():log.write_text(redact_paths(log.read_text()))
    return record


async def main():
    output=OUT/'results.json'
    if output.exists():raise FileExistsError('Retain prior outcomes; do not overwrite')
    value=dict(checkpoint='tool-bridge-cancel-errors-02',date='2026-09-28',models=0,
        source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),SERVER,ROOT/'skills/receipt/scripts/compare.py')},evidence=[],
        limitation='Owned SDK fault fixture only. Recovery follows an explicit author reset of deliberately slow/mutating test source; not automatic restoration. No model approval, arbitrary crash, normal-task efficiency or deployment evidence.')
    with tempfile.TemporaryDirectory(prefix='qh-cancel-errors-') as temporary:
        for scenario in ('timeout','guard','guard_uncancelled'):
            record=await one(Path(temporary)/scenario,scenario)
            value['evidence'].append(record)
            output.write_text(redact_paths(json.dumps(value,indent=2))+'\n')
            print(scenario,record['passed'],record.get('control_error',''),flush=True)
            if not record.get('native_terminal_before_author_reset',False):break
    if not all(r['passed'] for r in value['evidence']) or len(value['evidence'])!=3:
        raise SystemExit(1)

asyncio.run(main())
