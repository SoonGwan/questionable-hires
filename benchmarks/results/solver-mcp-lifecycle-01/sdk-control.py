import asyncio
import base64
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run(vm, output):
    server = Path(__file__).with_name('server.py').resolve()
    params = StdioServerParameters(command=sys.executable,
        args=['-B', str(server), '--vm', str(vm), '--log', str(output / 'guest.txt')])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            assert len(listed.tools) == 1
            tool = listed.tools[0]
            assert tool.name == 'guest_command'
            assert tool.annotations.readOnlyHint is False and tool.annotations.destructiveHint is True
            responses = []
            for request in [dict(command='/bin/busybox uname -s'),
                            dict(command='/bin/busybox printf failed; exit 7'),
                            dict(command='echo unavailable', cwd='/Users'),
                            dict(command='/bin/busybox printf recovered')]:
                result = await session.call_tool('guest_command', request)
                response = json.loads(result.content[0].text)
                responses.append(dict(isError=result.isError, response=response))
            def stdout(index):
                return base64.b64decode(responses[index]['response']['result']['output']['stdout']['base64'])
            assert stdout(0) == b'Linux\n'
            assert responses[1]['response']['result']['exit_code'] == 7 and stdout(1) == b'failed'
            assert not responses[1]['isError']
            assert responses[2]['isError'] and responses[2]['response']['error'] == 'FileNotFoundError'
            assert stdout(3) == b'recovered'
            record = dict(result='PASS', tool=tool.model_dump(mode='json'), responses=responses,
                          models=0, selected_issue_tests=0)
    (output / 'result.json').write_text(json.dumps(record, indent=2) + '\n')


if __name__ == '__main__':
    asyncio.run(asyncio.wait_for(run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()), timeout=40))
