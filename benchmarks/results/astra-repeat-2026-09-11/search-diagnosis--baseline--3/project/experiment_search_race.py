"""Local, cache-free experiment; run with python3 experiment_search_race.py."""

import asyncio

from search import Search
from transport import fetch


async def scenario(completion_order):
    search = Search()
    queries = ("old", "new")
    started = {query: asyncio.Event() for query in queries}
    release = {query: asyncio.Event() for query in queries}
    calls = []

    async def request(path, *, params, headers):
        query = params["q"]
        calls.append((path, dict(params), dict(headers)))
        started[query].set()
        await release[query].wait()
        # Construct a fresh, query-specific response; there is no cache.
        return {"query": query, "results": [f"result for {query}"]}

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
        snapshots.append(search.result["query"])

    assert calls == [
        ("/search", {"q": query}, {"Cache-Control": "no-cache"})
        for query in queries
    ], calls
    assert snapshots == list(completion_order), snapshots
    print(f"Started: {queries}; completed: {completion_order}")
    print(f"  Visible result after each completion: {snapshots}")
    print(f"  Final result matches latest query: {search.result['query'] == 'new'}")
    return search.result["query"]


async def main():
    assert await scenario(("old", "new")) == "new"
    assert await scenario(("new", "old")) == "old"
    print("Confirmed: a late older response overwrites the newer result without caching.")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=5))
