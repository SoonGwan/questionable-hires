"""Local, deterministic response-order experiment; no network or cache."""

import asyncio
from functools import partial

from search import Search
from transport import fetch


async def trial(completion_order):
    search = Search()
    queries = ("earlier", "newer")
    started = {query: asyncio.Event() for query in queries}
    release = {query: asyncio.Event() for query in queries}
    requests = []

    async def request(path, *, params, headers):
        query = params["q"]
        assert path == "/search"
        assert headers == {"Cache-Control": "no-cache"}
        requests.append(query)
        started[query].set()
        await release[query].wait()
        return f"results for {query}"

    tasks = {}
    for query in queries:
        tasks[query] = asyncio.create_task(
            search.run(query, partial(fetch, request=request))
        )
        await started[query].wait()

    snapshots = []
    for query in completion_order:
        release[query].set()
        await tasks[query]
        snapshots.append(search.result)

    assert requests == list(queries)
    assert snapshots == [f"results for {query}" for query in completion_order]
    print(f"start={requests}; completion={list(completion_order)}")
    print(f"  result after each completion={snapshots}")
    print(f"  final matches latest query: {search.result == 'results for newer'}")


async def main():
    # Same inputs and implementation; only response completion order changes.
    await trial(("earlier", "newer"))
    await trial(("newer", "earlier"))


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=5))
