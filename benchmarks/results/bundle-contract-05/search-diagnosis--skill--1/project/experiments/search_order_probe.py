"""Run from the project root: python3 -B experiments/search_order_probe.py."""

import asyncio
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from search import Search
from transport import fetch


async def bounded(awaitable):
    # All owned coroutines await standard asyncio primitives and do not suppress
    # cancellation; no network, threads, or blocking dependencies are involved.
    return await asyncio.wait_for(awaitable, timeout=1.0)


async def scenario(order):
    search = Search()
    gates = {q: asyncio.get_running_loop().create_future() for q in ('old', 'new')}
    dispatched = {q: asyncio.Event() for q in gates}
    trace = []
    tasks = {}

    async def request(url, *, params, headers):
        query = params['q']
        trace.append({'event': 'request', 'url': url,
                      'params': dict(params), 'headers': dict(headers)})
        dispatched[query].set()
        # This recording dependency has no cache. Each response is supplied
        # independently, only when the experiment releases its own gate.
        return await gates[query]

    async def actual_transport(query):
        return await fetch(query, request)

    try:
        for query in ('old', 'new'):
            tasks[query] = asyncio.create_task(search.run(query, actual_transport))
            await bounded(dispatched[query].wait())
        assert search.result is None
        for query in order:
            payload = {'query': query, 'results': [query + '-result']}
            trace.append({'event': 'release_response', 'query': query, 'payload': payload})
            gates[query].set_result(payload)
            await bounded(asyncio.shield(tasks[query]))
            trace.append({'event': 'observed_result', 'after_completion': query,
                          'result': search.result})
            assert search.result == payload
        requests = [event for event in trace if event['event'] == 'request']
        assert requests == [
            {'event': 'request', 'url': '/search', 'params': {'q': q},
             'headers': {'Cache-Control': 'no-cache'}} for q in ('old', 'new')
        ]
        assert search.result['query'] == order[-1]
        return {'submission_order': ['old', 'new'], 'completion_order': order,
                'trace': trace, 'final_result': search.result,
                'stale_relative_to_latest_query': search.result['query'] != 'new'}
    finally:
        for task in tasks.values():
            if not task.done():
                task.cancel()
        await bounded(asyncio.gather(*tasks.values(), return_exceptions=True))
        for gate in gates.values():
            if not gate.done():
                gate.cancel()


def source_hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ('search.py', 'transport.py')}


async def main():
    before = source_hashes()
    normal = await scenario(['old', 'new'])
    reversed_order = await scenario(['new', 'old'])
    assert normal['stale_relative_to_latest_query'] is False
    assert reversed_order['stale_relative_to_latest_query'] is True
    assert source_hashes() == before, 'Production files changed during probe'
    print(json.dumps({'source_sha256': before, 'scenarios': [normal, reversed_order],
                      'verification': 'passed'}, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
