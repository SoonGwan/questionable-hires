"""Run with: python3 experiments/search_completion_order.py (stdlib only)."""

import asyncio
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from search import Search
from transport import fetch


TIMEOUT = 2.0
QUERIES = ("older-query", "newer-query")


def production_hashes():
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ("search.py", "transport.py")
    }


async def scenario(completion_order):
    search = Search()
    loop = asyncio.get_running_loop()
    arrived = {q: asyncio.Event() for q in QUERIES}
    releases = {q: loop.create_future() for q in QUERIES}
    requests = []
    snapshots = []
    tasks = {}

    async def request(url, *, params, headers):
        query = params["q"]
        requests.append({"url": url, "params": dict(params), "headers": dict(headers)})
        arrived[query].set()
        # A distinct response for each request, with no cache or network involved.
        return await asyncio.wait_for(asyncio.shield(releases[query]), TIMEOUT)

    async def actual_transport(query):
        return await fetch(query, request)

    try:
        # Ensure request issue order without relying on sleeps or scheduler timing.
        for query in QUERIES:
            tasks[query] = asyncio.create_task(search.run(query, actual_transport))
            await asyncio.wait_for(arrived[query].wait(), TIMEOUT)

        assert search.result is None, "A request completed before its release"
        assert requests == [
            {"url": "/search", "params": {"q": q},
             "headers": {"Cache-Control": "no-cache"}}
            for q in QUERIES
        ], requests

        for query in completion_order:
            response = {"query": query, "request_id": QUERIES.index(query) + 1}
            releases[query].set_result(response)
            await asyncio.wait_for(asyncio.shield(tasks[query]), TIMEOUT)
            assert search.result == response, (query, search.result)
            snapshots.append({"completed_query": query, "visible_result": search.result})

        stale = search.result["query"] != QUERIES[-1]
        assert stale == (completion_order[-1] == QUERIES[0])
        return {
            "issue_order": list(QUERIES),
            "completion_order": list(completion_order),
            "recorded_requests": requests,
            "snapshots": snapshots,
            "latest_issued_query": QUERIES[-1],
            "final_result": search.result,
            "final_result_is_stale": stale,
        }
    finally:
        # Own and drain every spawned task, including when an assertion/timeout fails.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        for release in releases.values():
            if not release.done():
                release.cancel()
        if tasks:
            await asyncio.wait_for(
                asyncio.gather(*tasks.values(), return_exceptions=True), TIMEOUT
            )


async def main():
    before = production_hashes()
    cases = {
        "normal": await scenario(QUERIES),
        "reversed": await scenario(tuple(reversed(QUERIES))),
    }
    after = production_hashes()
    assert before == after, "Production files changed during experiment"
    print(json.dumps({
        "production_sha256": after,
        "production_files_unchanged": before == after,
        "request_boundary": "Controlled in-memory request stub; no cache or network",
        "wait_timeout_seconds": TIMEOUT,
        "cases": cases,
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
