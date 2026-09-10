"""Local diagnosis: run with `python3 -B diagnose_search.py` (no network)."""

import asyncio
import json

from search import Search
from transport import fetch


async def experiment(completion_order):
    search = Search()
    queries = ("earlier", "newer")
    started = {query: asyncio.Event() for query in queries}
    release = {query: asyncio.Event() for query in queries}
    calls = []

    async def request(path, *, params, headers):
        query = params["q"]
        calls.append({"path": path, "params": params, "headers": headers})
        started[query].set()
        await release[query].wait()
        # Fresh response for this exact query; no cache or external service.
        return {"query": query, "results": [query + " result"]}

    async def local_fetch(query):
        return await fetch(query, request)

    tasks = {}
    for query in queries:
        tasks[query] = asyncio.create_task(search.run(query, local_fetch))
        await started[query].wait()

    snapshots = []
    for query in completion_order:
        release[query].set()
        await tasks[query]
        snapshots.append({"completed": query, "visible": search.result})

    assert [call["params"]["q"] for call in calls] == list(queries)
    assert all(call["path"] == "/search" for call in calls)
    assert all(call["headers"] == {"Cache-Control": "no-cache"} for call in calls)
    assert [row["visible"]["query"] for row in snapshots] == list(completion_order)
    assert search.result["query"] == completion_order[-1]
    stale = search.result["query"] != queries[-1]
    assert stale == (completion_order[-1] == "earlier")
    print(json.dumps({
        "started": list(queries),
        "completion_order": completion_order,
        "cache": "absent",
        "calls": calls,
        "snapshots": snapshots,
        "stale_final_result": stale,
    }, indent=2))


async def main():
    await experiment(("earlier", "newer"))
    await experiment(("newer", "earlier"))


if __name__ == "__main__":
    asyncio.run(main())
