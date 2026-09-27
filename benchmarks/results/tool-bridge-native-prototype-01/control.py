"""Real SDK stdio/native controls; no model sessions or plugin registration."""
import asyncio
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import tempfile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
SERVER = Path(__file__).with_name('server.py')
HELPER = ROOT / 'skills/receipt/scripts/compare.py'
PROJECT_PYTHON = '/tmp/qh-validation-env/bin/python'

async def controls():
    evidence=[]
    with tempfile.TemporaryDirectory(prefix='qh-bridge-native-') as temporary:
        for case in cases(PROJECT_PYTHON):
            root=Path(temporary)/case['id'];run.prepare(case,root)
            before=run.resource_manifest(root)
            params=StdioServerParameters(command=sys.executable,args=['-B',str(SERVER),'--source',str(root),'--helper',str(HELPER),'--python',PROJECT_PYTHON])
            async with stdio_client(params) as (read,write):
                async with ClientSession(read,write) as session:
                    initialized=await session.initialize()
                    tools=await session.list_tools()
                    assert [t.name for t in tools.tools]==['receipt_compare']
                    recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD~2' if case['id'].endswith('multiple') else 'HEAD^',after='HEAD',imports=['windows','test_windows'],tests=['-v','test_windows'],observe_assertions=True,guard_tree=True)
                    if case['id'].endswith('multiple'):recipe['additional_before']=['HEAD^']
                    for mode in ('bootstrap','module'):
                        result=await session.call_tool('receipt_compare',dict(recipe=dict(recipe,invocation=mode)))
                        assert not result.isError and result.structuredContent is None and len(result.content)==1
                        value=json.loads(result.content[0].text)
                        assert value['status']=='observed' and value['comparison_copies_removed'] and value['originals']['unchanged'] and value['tree_guard']['unchanged']
                        assert [v['native_exit_code'] for v in value['checks'].values()]==([1,1,0] if case['id'].endswith('multiple') else [1,0])
                        for check in value['checks'].values():
                            assert check['suite_observation']['tests']==6 and check['suite_observation']['skipped']==0
                            report=check['assertion_observation'];assert report['v']==2 and report['complete'] and len(report['observations'])==7
                            assert all('Verified copied import: '+name+' ' in check['output'] for name in recipe['imports'])
                        assert run.resource_manifest(root)==before
                        evidence.append(dict(case=case['id'],mode=mode,handshake=initialized.model_dump(mode='json'),tool=tools.tools[0].model_dump(mode='json'),result=value,unchanged=True,single_text_no_duplicate_structured=True))
                    invalid=[]
                    for name,arguments in [('unknown_tool',{}),('receipt_compare',{'recipe':dict(recipe,observe_assertions=1)}),('receipt_compare',{'recipe':dict(recipe,fixed=['../outside.py'])})]:
                        result=await session.call_tool(name,arguments)
                        assert result.isError and run.resource_manifest(root)==before
                        invalid.append(dict(name=name,arguments=arguments,result=result.model_dump(mode='json')))
                    evidence.append(dict(case=case['id'],invalid=invalid))
                    if case['id']=='windows-single':
                        tests=root/'test_windows.py';original=tests.read_bytes()
                        tests.write_bytes(original+b'\nimport sys\ndef _owned_profile(*args): return None\nsys.setprofile(_owned_profile)\ndef tearDownModule():\n    assert sys.getprofile() is _owned_profile\n')
                        with_profile=run.resource_manifest(root)
                        try:
                            result=await session.call_tool('receipt_compare',dict(recipe=dict(recipe,invocation='module')))
                            assert result.isError and result.structuredContent is None
                            value=json.loads(result.content[0].text)
                            assert value['status']=='incomplete' and list(value['checks'])==['before']
                            check=value['checks']['before']
                            assert check['native_exit_code']==1 and check['exit_code']==7
                            assert check['assertion_observation']['reason']=='existing_profile'
                            assert check['suite_observation']['tests']==6 and value['comparison_copies_removed']
                            assert run.resource_manifest(root)==with_profile
                            evidence.append(dict(case=case['id'],incomplete=value,tool_is_error=True))
                        finally:
                            tests.write_bytes(original)
                        assert run.resource_manifest(root)==before

    result=dict(checkpoint='tool-bridge-native-prototype-01',date='2026-09-27',parent='ecf33669',sdk=importlib.metadata.version('mcp'),source_sha256=hashlib.sha256(SERVER.read_bytes()).hexdigest(),helper_sha256=hashlib.sha256(HELPER.read_bytes()).hexdigest(),native_comparisons=5,native_processes=11,invalid_calls=6,models=0,global_registration=False,evidence=evidence,limitation='SDK client/stdio/native proof only; Codex model calls, concurrency/cancellation/shutdown and all8 efficiency unverified.')
    Path(__file__).with_name('result.json').write_text(redact_paths(json.dumps(result,indent=2))+'\n')
    print('Actual stdio initialization/discovery, five native comparisons/eleven six-test processes, six rejected calls, original preservation and no duplicate structured output pass')

asyncio.run(controls())
