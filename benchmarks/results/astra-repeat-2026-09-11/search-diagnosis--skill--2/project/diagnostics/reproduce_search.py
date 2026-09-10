"""Local, cache-free experiment: vary only request completion order.

Run from the project root: python3 -B diagnostics/reproduce_search.py
"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search import Search
from transport import fetch


async def trial(completion_order):
    search = Search()
    queries = ("old query", "new query")
    loop = asyncio.get_running_loop()
    responses = {query: loop.create_future() for query in queries}
    started = {query: asyncio.Event() for query in queries}
    requests = []
    observations = []

    async def request(path, *, params, headers):
        # No network, stored results, cache, random delays, or wall-clock sleeps.
        query = params["q"]
        requests.append({"path": path, "params": params, "headers": headers})
        started[query].set()
        return await responses[query]

    async def local_fetch(query):
        return await fetch(query, request)

    tasks = {}
    for query in queries:
        tasks[query] = asyncio.create_task(search.run(query, local_fetch))
        await started[query].wait()

    for query in completion_order:
        responses[query].set_result("results for " + query)
        await tasks[query]
        observations.append({"completed": query, "displayed": search.result})

    assert [entry["params"]["q"] for entry in requests] == list(queries)
    assert all(entry["path"] == "/search" for entry in requests)
    assert all(entry["headers"] == {"Cache-Control": "no-cache"} for entry in requests)
    assert search.result == "results for " + completion_order[-1]
    return {
        "completion_order": completion_order,
        "requests": requests,
        "observations": observations,
        "latest_query": queries[-1],
        "final_result": search.result,
        "stale": search.result != "results for " + queries[-1],
    }


async def main():
    in_order = await trial(("old query", "new query"))
    out_of_order = await trial(("new query", "old query"))
    assert not in_order["stale"]
    assert out_of_order["stale"]
    print(json.dumps([in_order, out_of_order], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
