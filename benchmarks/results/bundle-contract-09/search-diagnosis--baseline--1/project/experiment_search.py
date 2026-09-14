"""Local race reproduction: python3 -B experiment_search.py

Uses the real Search and transport.fetch; only the request boundary is fake.
No network, cache implementation, dependencies, or production edits required.
"""

import asyncio
import copy
import hashlib
import json
from pathlib import Path

from search import Search
from transport import fetch


TIMEOUT = 2.0
QUERIES = ("earlier", "newer")


def production_hashes():
    root = Path(__file__).resolve().parent
    return {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in ("search.py", "transport.py")
    }


async def run_case(order):
    search = Search()
    started = {q: asyncio.Event() for q in QUERIES}
    release = {q: asyncio.Event() for q in QUERIES}
    requests = []
    completions = []
    tasks = {}

    async def request(path, *, params, headers):
        query = params["q"]
        requests.append(copy.deepcopy({
            "path": path, "params": params, "headers": headers,
        }))
        started[query].set()
        await asyncio.wait_for(release[query].wait(), timeout=TIMEOUT)
        completions.append(query)
        return {"query": query, "items": [f"result for {query}"]}

    async def through_transport(query):
        return await fetch(query, request)

    snapshots = []
    try:
        # Start the earlier search first, then type/start the newer query while
        # the earlier request is still pending. No scheduler-timing sleeps.
        for query in QUERIES:
            tasks[query] = asyncio.create_task(
                search.run(query, through_transport), name=f"search-{query}"
            )
            await asyncio.wait_for(started[query].wait(), timeout=TIMEOUT)
        assert all(not task.done() for task in tasks.values())
        assert search.result is None

        for query in order:
            release[query].set()
            await asyncio.wait_for(tasks[query], timeout=TIMEOUT)
            snapshots.append(copy.deepcopy(search.result))

        assert [r["params"]["q"] for r in requests] == list(QUERIES)
        assert all(r["path"] == "/search" for r in requests)
        assert all(r["headers"] == {"Cache-Control": "no-cache"}
                   for r in requests)
        assert completions == list(order)
        assert [s["query"] for s in snapshots] == list(order)
        assert search.result["query"] == order[-1]
        result = {
            "start_order": list(QUERIES),
            "completion_order": completions,
            "recorded_requests": requests,
            "result_after_each_completion": snapshots,
            "final_result": copy.deepcopy(search.result),
            "latest_query": QUERIES[-1],
            "stale_final_result": search.result["query"] != QUERIES[-1],
        }
    finally:
        # Clean up only tasks this case owns, including on timeout/assertion.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.wait_for(
                asyncio.gather(*tasks.values(), return_exceptions=True),
                timeout=TIMEOUT,
            )
    result["owned_tasks_finished"] = all(t.done() for t in tasks.values())
    return result


async def main():
    before = production_hashes()
    normal = await run_case(QUERIES)
    reversed_case = await run_case(tuple(reversed(QUERIES)))
    assert not normal["stale_final_result"]
    assert reversed_case["stale_final_result"]
    after = production_hashes()
    assert before == after, "Production files changed during the experiment"
    print(json.dumps({
        "boundary": "in-memory controlled request; no cache or HTTP server",
        "wait_timeout_seconds": TIMEOUT,
        "production_sha256_before": before,
        "production_sha256_after": after,
        "normal": normal,
        "reversed": reversed_case,
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
