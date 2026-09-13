"""Local, cache-free response-order experiment. Run with Python's standard library."""

import asyncio
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))

from search import Search
from transport import fetch


TIMEOUT_SECONDS = 2
QUERIES = ("older query", "newer query")


def production_hashes():
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ("search.py", "transport.py")
    }


def require(condition, message):
    if not condition:
        raise AssertionError(message)


async def bounded(awaitable):
    return await asyncio.wait_for(awaitable, timeout=TIMEOUT_SECONDS)


async def run_case(name, completion_order):
    search = Search()
    entered = {query: asyncio.Event() for query in QUERIES}
    release = {query: asyncio.Event() for query in QUERIES}
    requests = []
    transport_completions = []
    snapshots = []
    tasks = {}

    async def request(path, *, params, headers):
        # Only this lowest-level I/O boundary is replaced. No network or cache.
        query = params["q"]
        requests.append({"path": path, "params": dict(params), "headers": dict(headers)})
        entered[query].set()
        await bounded(release[query].wait())
        transport_completions.append(query)
        return {"query": query, "items": [f"result for {query}"]}

    async def actual_transport(query):
        return await fetch(query, request)

    try:
        # Start the older query first, then start the newer query before either
        # request can complete. Handshakes avoid timing-dependent sleeps.
        for query in QUERIES:
            tasks[query] = asyncio.create_task(
                search.run(query, actual_transport), name=f"{name}: {query}"
            )
            await bounded(entered[query].wait())

        require(search.result is None, "A result appeared before any release")
        for query in completion_order:
            release[query].set()
            await bounded(asyncio.shield(tasks[query]))
            snapshots.append({"completed_query": query, "search_result": search.result})
            require(search.result["query"] == query, "Unexpected result after completion")

        require(transport_completions == list(completion_order), "Wrong completion order")
        require(requests == [
            {"path": "/search", "params": {"q": query},
             "headers": {"Cache-Control": "no-cache"}}
            for query in QUERIES
        ], "Actual transport did not send the expected requests")
        require(search.result["query"] == completion_order[-1], "Wrong final result")
        return {
            "case": name,
            "latest_started_query": QUERIES[-1],
            "recorded_requests": requests,
            "completion_order": transport_completions,
            "result_after_each_completion": snapshots,
            "final_result_is_stale": search.result["query"] != QUERIES[-1],
        }
    finally:
        # Own and settle every task, including when a handshake/assertion fails.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        if tasks:
            await bounded(asyncio.gather(*tasks.values(), return_exceptions=True))


async def main():
    before = production_hashes()
    normal = await run_case("normal", QUERIES)
    reversed_case = await run_case("reversed", tuple(reversed(QUERIES)))
    require(not normal["final_result_is_stale"], "Normal-order control failed")
    require(reversed_case["final_result_is_stale"], "Stale overwrite was not reproduced")
    after = production_hashes()
    require(before == after, "Production source changed during experiment")
    print(json.dumps({
        "experiment": "actual Search and transport; controlled cache-free request stub",
        "wait_timeout_seconds": TIMEOUT_SECONDS,
        "production_sha256_before": before,
        "production_sha256_after": after,
        "cases": [normal, reversed_case],
        "checks_passed": True,
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
