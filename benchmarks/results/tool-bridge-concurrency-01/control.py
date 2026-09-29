"""Reproduce overlapping owner guards, then verify project-serialized requests."""
import asyncio
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
PYTHON='/tmp/qh-validation-env/bin/python'

async def check():
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix='qh-bridge-concurrency-') as temp:
        for label,server in [('previous',ROOT/'benchmarks/results/tool-bridge-native-prototype-01/server.py'),('serialized',Path(__file__).with_name('server.py'))]:
            root=Path(temp)/label;run.prepare(cases(PYTHON)[0],root)
            tests=root/'test_windows.py'
            tests.write_text(tests.read_text()+'''\nimport pathlib, time\ndef setUpModule():\n    pathlib.Path(__file__).with_name('native-started.txt').write_text('started')\n    time.sleep(0.4)\n''')
            original=run.resource_manifest(root)
            recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD^',after='HEAD',imports=['windows','test_windows'],tests=['-v','test_windows'],invocation='module',observe_assertions=True,guard_tree=True)
            params=StdioServerParameters(command=sys.executable,args=['-B',str(server),'--source',str(root),'--helper',str(ROOT/'skills/receipt/scripts/compare.py'),'--python',PYTHON])
            async with stdio_client(params) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    first=asyncio.create_task(session.call_tool('receipt_compare',{'recipe':recipe}))
                    deadline=time.monotonic()+10
                    while not list(root.glob('.receipt-*/before/native-started.txt')):
                        assert not first.done() and time.monotonic()<deadline
                        await asyncio.sleep(0.01)
                    second=asyncio.create_task(session.call_tool('receipt_compare',{'recipe':recipe}))
                    results=await asyncio.gather(first,second)
                    assert run.resource_manifest(root)==original and not list(root.glob('.receipt-*'))
                    if label=='previous':
                        assert any(r.isError and 'Project tree changed' in r.content[0].text for r in results)
                    else:
                        for result in results:
                            assert not result.isError
                            value=json.loads(result.content[0].text)
                            assert value['status']=='observed' and value['tree_guard']['unchanged'] and value['comparison_copies_removed']
                            assert [c['native_exit_code'] for c in value['checks'].values()]==[1,0]
                            assert all(c['suite_observation']['tests']==6 and c['assertion_observation']['complete'] for c in value['checks'].values())
                    outcomes.append(dict(condition=label,source_sha256=hashlib.sha256(server.read_bytes()).hexdigest(),overlap_admitted_after_native_marker=True,results=[r.model_dump(mode='json') for r in results],originals_unchanged=True,scratch_removed=True))
    Path(__file__).with_name('results.json').write_text(redact_paths(json.dumps(dict(checkpoint='tool-bridge-concurrency-01',date='2026-09-27',outcomes=outcomes,models=0,limitation='Local SDK overlap control; cancellation/disconnection/host/model/all8 efficiency unverified.'),indent=2))+'\n')
    print('Native overlap reproduces guard failure before; serialized requests preserve both complete native1/0 comparisons and originals/cleanup')
asyncio.run(check())
