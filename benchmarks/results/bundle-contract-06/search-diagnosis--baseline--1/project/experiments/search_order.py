"""Run with python3 -B experiments/search_order.py; standard library only."""

import asyncio
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from search import Search
from transport import fetch


TIMEOUT = 2.0


def source_hashes():
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ("search.py", "transport.py")
    }


async def scenario(completion_order):
    search = Search()
    started = asyncio.Queue()
    gates = {}
    requests = []
    tasks = {}
    snapshots = []

    async def request(url, *, params, headers):
        # No cache, HTTP client, server, or external I/O: each request gets its
        # own response gate. The real transport supplies the recorded arguments.
        query = params["q"]
        gates[query] = asyncio.get_running_loop().create_future()
        requests.append({"url": url, "params": dict(params), "headers": dict(headers)})
        started.put_nowait(query)
        return await gates[query]

    async def actual_fetch(query):
        return await fetch(query, request)

    try:
        for query in ("older", "newer"):
            tasks[query] = asyncio.create_task(search.run(query, actual_fetch))
            observed = await asyncio.wait_for(started.get(), TIMEOUT)
            assert observed == query, (observed, query)

        assert all(not task.done() for task in tasks.values())
        assert search.result is None
        assert requests == [
            {
                "url": "/search",
                "params": {"q": query},
                "headers": {"Cache-Control": "no-cache"},
            }
            for query in ("older", "newer")
        ], requests

        for query in completion_order:
            response = {"query": query, "results": [f"result for {query}"]}
            gates[query].set_result(response)
            await asyncio.wait_for(asyncio.shield(tasks[query]), TIMEOUT)
            assert search.result == response, search.result
            snapshots.append({"completed_query": query, "visible_result": search.result})

        stale = search.result["query"] != "newer"
        assert stale == (completion_order[-1] == "older")
        return {
            "completion_order": list(completion_order),
            "requests": requests,
            "snapshots": snapshots,
            "latest_submitted_query": "newer",
            "final_result": search.result,
            "stale_final_result": stale,
        }
    finally:
        # Clean up only tasks and response gates created by this scenario,
        # including on failed assertions or bounded request/completion waits.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        for gate in gates.values():
            if not gate.done():
                gate.cancel()
        if tasks:
            done, pending = await asyncio.wait(tasks.values(), timeout=TIMEOUT)
            for task in done:
                if not task.cancelled():
                    task.exception()  # Retrieve exceptions on failure paths.
            if pending:
                raise RuntimeError("Owned search tasks did not terminate within cleanup deadline")


async def main():
    before = source_hashes()
    outcomes = [
        await scenario(("older", "newer")),
        await scenario(("newer", "older")),
    ]
    after = source_hashes()
    assert before == after, "Production source changed during experiment"
    print(json.dumps({
        "boundary": "Actual Search and transport; controlled request stub with no cache or network",
        "wait_timeout_seconds": TIMEOUT,
        "source_sha256": before,
        "production_sources_unchanged": before == after,
        "scenarios": outcomes,
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
