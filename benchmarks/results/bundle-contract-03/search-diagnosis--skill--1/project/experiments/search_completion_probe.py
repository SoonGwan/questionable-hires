"""Run with python3 -B experiments/search_completion_probe.py (stdlib only).

Exercise real Search and transport.fetch; replace only the request dependency.
No network or cache. Each request returns its own query after explicit release.
Detailed evidence is printed as JSON; assertions fail on unexpected behavior.
"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from search import Search
from transport import fetch


TIMEOUT = 2


async def scenario(order):
    search = Search()
    queries = ("earlier", "newer")
    arrived = {q: asyncio.Event() for q in queries}
    release = {q: asyncio.Event() for q in queries}
    trace = []
    tasks = {}

    async def request(url, *, params, headers):
        query = params["q"]
        trace.append({"event": "request", "url": url,
                      "params": dict(params), "headers": dict(headers)})
        arrived[query].set()
        await asyncio.wait_for(release[query].wait(), TIMEOUT)
        response = {"query": query, "results": [query + " result"]}
        trace.append({"event": "response", "body": response})
        return response

    async def real_transport(query):
        return await fetch(query, request)

    try:
        # Confirm dispatch of each query before submitting/releasing the next.
        for query in queries:
            trace.append({"event": "submit", "query": query})
            tasks[query] = asyncio.create_task(search.run(query, real_transport))
            await asyncio.wait_for(arrived[query].wait(), TIMEOUT)
        assert search.result is None

        for query in order:
            release[query].set()
            await asyncio.wait_for(tasks[query], TIMEOUT)
            trace.append({"event": "stored", "after_completion": query,
                          "result": search.result})
            assert search.result["query"] == query

        requests = [event for event in trace if event["event"] == "request"]
        assert requests == [
            {"event": "request", "url": "/search", "params": {"q": q},
             "headers": {"Cache-Control": "no-cache"}}
            for q in queries
        ]
        assert search.result["query"] == order[-1]
        return {"submission_order": queries, "completion_order": order,
                "cache_present": False, "trace": trace,
                "final_result": search.result,
                "stale_relative_to_latest_submission":
                    search.result["query"] != queries[-1]}
    finally:
        # All owned tasks use cancellation-cooperative local asyncio operations.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.wait_for(
                asyncio.gather(*tasks.values(), return_exceptions=True), TIMEOUT
            )


async def main():
    outcomes = []
    for order in (("earlier", "newer"), ("newer", "earlier")):
        outcomes.append(await scenario(order))
    assert [outcome["stale_relative_to_latest_submission"]
            for outcome in outcomes] == [False, True]
    print(json.dumps({"outcomes": outcomes, "checks": "passed"}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
