"""Local, cache-free experiment using the unchanged search and transport code."""

import asyncio

from search import Search
from transport import fetch


async def scenario(completion_order):
    search = Search()
    queries = ("old query", "new query")
    started = {query: asyncio.Event() for query in queries}
    release = {query: asyncio.Event() for query in queries}
    calls = []
    snapshots = []

    async def request(path, *, params, headers):
        query = params["q"]
        calls.append((path, dict(params), dict(headers)))
        started[query].set()
        await release[query].wait()
        # No cache: each response is constructed from its own request query.
        return {"query": query, "items": [f"result for {query}"]}

    async def local_fetch(query):
        return await fetch(query, request)

    tasks = {}
    for query in queries:
        tasks[query] = asyncio.create_task(search.run(query, local_fetch))
        await started[query].wait()

    # Both searches are in flight; the new query was submitted last.
    assert search.result is None
    for query in completion_order:
        release[query].set()
        await tasks[query]
        snapshots.append(search.result["query"])

    assert calls == [
        ("/search", {"q": query}, {"Cache-Control": "no-cache"})
        for query in queries
    ]
    assert snapshots == list(completion_order)
    print(f"Completion order: {' -> '.join(completion_order)}")
    print(f"Observed results: {' -> '.join(snapshots)}")
    print(f"Final result matches latest query: {search.result['query'] == queries[-1]}")
    return search.result["query"]


async def main():
    assert await scenario(("old query", "new query")) == "new query"
    assert await scenario(("new query", "old query")) == "old query"
    print("PASS: stale results reproduced without a cache; completion order controls the result.")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=5))
