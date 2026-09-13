"""Local, standard-library-only experiment; no network requests or production edits.

Run from this directory: python3 -B experiment_search.py
"""

import asyncio
from functools import partial
import hashlib
import json
from pathlib import Path

from search import Search
from transport import fetch


TIMEOUT = 2.0
ROOT = Path(__file__).resolve().parent


def production_hashes():
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ("search.py", "transport.py")
    }


async def exercise(order):
    queries = ("older", "newer")
    loop = asyncio.get_running_loop()
    gates = {query: loop.create_future() for query in queries}
    started = {query: asyncio.Event() for query in queries}
    requests = []
    tasks = {}
    snapshots = []
    search = Search()

    async def request(url, *, params, headers):
        # This is the only substituted boundary. There is no cache or network.
        query = params["q"]
        requests.append({"url": url, "params": dict(params), "headers": dict(headers)})
        started[query].set()
        return await gates[query]

    try:
        actual_transport = partial(fetch, request=request)
        for query in queries:
            tasks[query] = asyncio.create_task(
                search.run(query, actual_transport), name=f"search-{query}"
            )
            await asyncio.wait_for(started[query].wait(), timeout=TIMEOUT)

        assert search.result is None, "A result appeared before any response was released"
        for query in order:
            gates[query].set_result({"query": query, "items": [f"result for {query}"]})
            await asyncio.wait_for(asyncio.shield(tasks[query]), timeout=TIMEOUT)
            snapshots.append({"completed_query": query, "visible_result": search.result})
            assert search.result["query"] == query

        assert requests == [
            {"url": "/search", "params": {"q": query},
             "headers": {"Cache-Control": "no-cache"}}
            for query in queries
        ], requests
        assert search.result["query"] == order[-1]
        return {
            "invocation_order": list(queries),
            "completion_order": list(order),
            "requests": requests,
            "snapshots": snapshots,
            "latest_query": queries[-1],
            "final_result": search.result,
            "stale_final_result": search.result["query"] != queries[-1],
        }
    finally:
        # Clean up only tasks/futures owned by this scenario, including on failure.
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
                    task.exception()  # Retrieve failures even if setup timed out.
            if pending:
                raise RuntimeError("Owned search tasks did not stop within the cleanup bound")


async def main():
    before = production_hashes()
    normal = await exercise(("older", "newer"))
    reversed_order = await exercise(("newer", "older"))
    assert normal["stale_final_result"] is False
    assert reversed_order["stale_final_result"] is True
    after = production_hashes()
    assert before == after, "Production files changed during the experiment"
    print(json.dumps({
        "boundary": "Actual Search.run and transport.fetch; controlled in-memory request stub",
        "wait_timeout_seconds": TIMEOUT,
        "production_sha256_before": before,
        "production_sha256_after": after,
        "normal": normal,
        "reversed": reversed_order,
        "verification": "passed",
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
