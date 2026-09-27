"""No-model actual Codex app-server native calls to an owned loopback tool."""
import asyncio
import hashlib
import json
from pathlib import Path
import signal
import socket
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths

SERVER = ROOT / 'benchmarks/results/tool-bridge-http-exit-01/server.py'
NAME = 'qh_receipt_host_native_01'
PYTHON = '/tmp/qh-validation-env/bin/python'

async def stop(process):
    if process.returncode is None:
        process.send_signal(signal.SIGTERM)
        await asyncio.wait_for(process.wait(), 8)

async def main():
    with tempfile.TemporaryDirectory(prefix='qh-host-discovery-') as temp:
        root = Path(temp) / 'project'
        run.prepare(cases(PYTHON)[0], root)
        original = run.resource_manifest(root)
        config_paths = [Path.home()/'.codex/config.toml', ROOT/'.codex/config.toml']
        def identity(path):
            return None if not path.exists() else (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mode)
        config_before = [identity(path) for path in config_paths]
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        with (Path(temp)/'server.log').open('w') as server_log, (Path(temp)/'host.log').open('w') as host_log:
            server = await asyncio.create_subprocess_exec(
                sys.executable, '-B', str(SERVER), '--source', str(root),
                '--helper', str(ROOT/'skills/receipt/scripts/compare.py'),
                '--python', PYTHON, '--port', str(port), stdout=server_log, stderr=server_log)
            host = None
            try:
                deadline = time.monotonic()+10
                while True:
                    try:
                        with socket.create_connection(('127.0.0.1', port), timeout=.1):
                            break
                    except OSError:
                        assert server.returncode is None and time.monotonic()<deadline
                        await asyncio.sleep(.02)
                # Replace the entire scoped table; no global registration/config write.
                override = f'mcp_servers={{ {NAME}={{ url="http://127.0.0.1:{port}/mcp", enabled_tools=["receipt_compare"], tool_timeout_sec=30 }} }}'
                host = await asyncio.create_subprocess_exec(
                    'codex', 'app-server', '-c', override, '-c', 'features.apps=false',
                    cwd=root, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=host_log)
                async def request(number, method, params):
                    host.stdin.write((json.dumps(dict(id=number, method=method, params=params))+'\n').encode())
                    await host.stdin.drain()
                    deadline = time.monotonic()+25
                    while True:
                        line = await asyncio.wait_for(host.stdout.readline(), max(.01, deadline-time.monotonic()))
                        assert line, 'host exited before response'
                        value = json.loads(line)
                        if value.get('id') == number:
                            assert 'error' not in value, str(value.get('error'))
                            return value['result']
                        # Other host messages may contain private configuration; never export.
                initialized = await request(1, 'initialize', dict(clientInfo=dict(name='qh-local-discovery', version='1'), capabilities=dict(experimentalApi=True)))
                host.stdin.write(b'{"method":"initialized"}\n')
                await host.stdin.drain()
                inventory = await request(2, 'mcpServerStatus/list', dict(detail='toolsAndAuthOnly', limit=100))
                target = next(row for row in inventory['data'] if row['name']==NAME)
                assert not target.get('toolsError'), 'target discovery failed'
                tools = target['tools']
                assert len(tools)==1 and next(iter(tools.values()))['name']=='receipt_compare'
                tool = next(iter(tools.values()))
                assert tool['inputSchema']['properties']['recipe']
                thread = await request(3, 'thread/start', dict(cwd=str(root), ephemeral=True,
                    environments=[], baseInstructions='', developerInstructions=''))
                thread_id = thread['thread']['id']
                native = []
                for number, invocation in enumerate(('bootstrap', 'module'), start=4):
                    recipe = dict(fixed=['test_windows.py'], vary=['windows.py'], before='HEAD^',
                        after='HEAD', imports=['windows','test_windows'], tests=['-v','test_windows'],
                        invocation=invocation, observe_assertions=True, guard_tree=True)
                    call = await request(number, 'mcpServer/tool/call', dict(threadId=thread_id,
                        server=NAME, tool='receipt_compare', arguments=dict(recipe=recipe)))
                    assert not call.get('isError') and call.get('structuredContent') is None
                    observation = json.loads(call['content'][0]['text'])
                    assert observation['status']=='observed' and observation['tree_guard']['unchanged']
                    assert observation['comparison_copies_removed']
                    assert [c['native_exit_code'] for c in observation['checks'].values()]==[1,0]
                    for check in observation['checks'].values():
                        assert check['suite_observation']['tests']==6 and check['suite_observation']['skipped']==0
                        assert all('Verified copied import: '+name+' ' in check['output'] for name in recipe['imports'])
                        if invocation=='module':
                            assert check['provenance_ready']
                        args = check['assertion_observation']
                        assert args['v']==2 and args['complete'] and len(args['observations'])==7
                    assert run.resource_manifest(root)==original and not list(root.glob('.receipt-*'))
                    native.append(dict(invocation=invocation, result=observation))
                result = dict(checkpoint='tool-bridge-host-native-01' , date='2026-09-27', models=0,
                    server_sha256=hashlib.sha256(SERVER.read_bytes()).hexdigest(),
                    actual_host_initialize=True, actual_host_tool_discovery=True,
                    target=target, host_user_agent=initialized.get('userAgent'), native=native, actual_host_native_calls=True, ephemeral_thread=True,
                    limitations='Direct host API calls with no turn/model. Native host execution only; no model selection, whole-task/all8 efficiency, host cancellation or abrupt-loss proof. Other host inventory/thread instructions not exported.')
            finally:
                if host is not None:
                    await stop(host)
                await stop(server)
            assert run.resource_manifest(root)==original
            assert [identity(path) for path in config_paths]==config_before
            result.update(originals_unchanged=True, config_bytes_modes_unchanged=True,
                          host_exit_code=host.returncode, server_exit_code=server.returncode)
            Path(__file__).with_name('results.json').write_text(redact_paths(json.dumps(result, indent=2))+'\n')
            print('Actual Codex host bootstrap/module native1/0 calls, original/config preservation and owned process exit pass')

asyncio.run(main())
