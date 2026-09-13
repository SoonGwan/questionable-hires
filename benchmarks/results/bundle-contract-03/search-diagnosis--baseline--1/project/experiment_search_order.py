"""Local-only reproduction: python3 -B experiment_search_order.py.

Uses the real Search and transport.fetch; replaces only the request boundary.
No network, cache, third-party dependencies, or production edits are involved.
"""

import asyncio
import hashlib
import json
from pathlib import Path

from search import Search
from transport import fetch


TIMEOUT_SECONDS = 2
QUERIES = ("older-query", "newer-query")
ROOT = Path(__file__).resolve().parent


def production_hashes():
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ("search.py", "transport.py")
    }


class ControlledRequest:
    def __init__(self):
        self.records = []
        self.arrived = {q: asyncio.Event() for q in QUERIES}
        self.responses = {
            q: asyncio.get_running_loop().create_future() for q in QUERIES
        }

    async def __call__(self, url, *, params, headers):
        query = params["q"]
        self.records.append({
            "url": url,
            "params": dict(params),
            "headers": dict(headers),
        })
        self.arrived[query].set()
        return await self.responses[query]


async def exercise(label, completion_order):
    search = Search()
    request = ControlledRequest()
    tasks = {}
    snapshots = []

    async def actual_transport(query):
        return await fetch(query, request)

    try:
        # Start the older search first and confirm each request has arrived.
        # Events, rather than sleeps, establish the ordering.
        for query in QUERIES:
            tasks[query] = asyncio.create_task(
                search.run(query, actual_transport), name=label + ":" + query
            )
            await asyncio.wait_for(
                request.arrived[query].wait(), TIMEOUT_SECONDS
            )

        assert search.result is None, "A held response unexpectedly completed"
        assert all(not task.done() for task in tasks.values())
        for query in completion_order:
            payload = {"query": query, "items": ["result for " + query]}
            request.responses[query].set_result(payload)
            await asyncio.wait_for(
                asyncio.shield(tasks[query]), TIMEOUT_SECONDS
            )
            snapshots.append({"completed_query": query, "result": search.result})
            assert search.result == payload, "Unexpected result assignment"

        assert request.records == [
            {"url": "/search", "params": {"q": q},
             "headers": {"Cache-Control": "no-cache"}}
            for q in QUERIES
        ], "Actual transport request differs from expectation"
        stale = search.result["query"] != QUERIES[-1]
        assert stale == (completion_order[-1] == QUERIES[0])
        evidence = {
            "scenario": label,
            "query_start_order": list(QUERIES),
            "completion_order": list(completion_order),
            "request_records": request.records,
            "result_after_each_completion": snapshots,
            "final_result": search.result,
            "final_result_is_stale": stale,
        }
    finally:
        # This experiment owns these tasks/futures. Reap tasks on failure too.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        for response in request.responses.values():
            if not response.done():
                response.cancel()
        await asyncio.wait_for(
            asyncio.gather(*tasks.values(), return_exceptions=True),
            TIMEOUT_SECONDS,
        )

    assert all(task.done() for task in tasks.values())
    assert all(response.done() for response in request.responses.values())
    evidence["owned_tasks_and_response_futures_finished"] = True
    return evidence


async def main():
    before = production_hashes()
    scenarios = [
        await exercise("normal", QUERIES),
        await exercise("reversed", tuple(reversed(QUERIES))),
    ]
    after = production_hashes()
    assert before == after, "Production files changed during the experiment"
    print(json.dumps({
        "request_boundary": "controlled in-memory responses; no cache or network",
        "behavior_wait_timeout_seconds": TIMEOUT_SECONDS,
        "scenarios": scenarios,
        "production_sha256_before": before,
        "production_sha256_after": after,
        "production_files_unchanged": True,
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
