"""Local diagnosis: control response order without caches or external services."""

import asyncio
import hashlib
from pathlib import Path

from search import Search
from transport import fetch


async def trial(completion_order):
    search = Search()
    queries = ("old query", "new query")
    responses = {q: [f"result for {q}"] for q in queries}
    pending = {q: asyncio.get_running_loop().create_future() for q in queries}
    started = {q: asyncio.Event() for q in queries}
    calls = []

    async def request(path, *, params, headers):
        query = params["q"]
        calls.append((path, dict(params), dict(headers)))
        started[query].set()
        return await pending[query]

    async def controlled_fetch(query):
        return await fetch(query, request)

    tasks = {}
    for query in queries:
        tasks[query] = asyncio.create_task(search.run(query, controlled_fetch))
        await started[query].wait()

    print(f"\nCompletion order: {completion_order}")
    print(f"Requests: {calls}")
    for query in completion_order:
        pending[query].set_result(responses[query])
        await tasks[query]
        print(f"Completed {query!r}; shared result = {search.result!r}")

    assert calls == [
        ("/search", {"q": q}, {"Cache-Control": "no-cache"}) for q in queries
    ]
    assert search.result == responses[completion_order[-1]]
    stale = search.result != responses[queries[-1]]
    print(f"Stale relative to latest query: {stale}")
    return stale


async def main():
    source_paths = [Path(__file__).with_name(p) for p in ("search.py", "transport.py")]
    before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths]
    assert not await trial(("old query", "new query"))
    assert await trial(("new query", "old query"))
    assert before == [hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths]
    print("\nPASS: response order alone reproduces stale results; production files unchanged.")


if __name__ == "__main__":
    asyncio.run(main())
