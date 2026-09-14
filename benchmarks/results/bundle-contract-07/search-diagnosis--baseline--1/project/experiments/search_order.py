"""Offline experiment: actual Search and transport, controlled request boundary.

Run from the project root: python3 -B experiments/search_order.py
No dependencies, sockets, cache, or production edits.
"""

import asyncio
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from search import Search
from transport import fetch


TIMEOUT = 2.0


async def bounded(awaitable):
    return await asyncio.wait_for(awaitable, timeout=TIMEOUT)


class ControlledRequest:
    """Record real transport arguments; return only explicitly released values."""

    def __init__(self):
        self.records = []
        self.arrivals = asyncio.Queue()
        self.responses = {}

    async def __call__(self, path, *, params, headers):
        query = params["q"]
        response = asyncio.get_running_loop().create_future()
        self.responses[query] = response
        self.records.append({"path": path, "params": dict(params), "headers": dict(headers)})
        self.arrivals.put_nowait(query)
        return await response

    def complete(self, query):
        self.responses[query].set_result({"query": query, "items": [f"fresh result for {query}"]})


async def scenario(completion_order):
    search = Search()
    request = ControlledRequest()
    tasks = {}
    states = []
    try:
        # Wait for each request to reach the transport boundary, not an arbitrary sleep.
        for query in ("old", "new"):
            tasks[query] = asyncio.create_task(
                search.run(query, lambda q: fetch(q, request)), name=f"search-{query}"
            )
            assert await bounded(request.arrivals.get()) == query

        assert search.result is None
        assert all(not task.done() for task in tasks.values())
        for query in completion_order:
            request.complete(query)
            await bounded(asyncio.shield(tasks[query]))
            states.append({"completed": query, "visible_result": dict(search.result)})
            assert search.result["query"] == query

        assert request.records == [
            {"path": "/search", "params": {"q": query},
             "headers": {"Cache-Control": "no-cache"}}
            for query in ("old", "new")
        ]
        return {
            "start_order": ["old", "new"],
            "completion_order": completion_order,
            "requests": request.records,
            "states_after_completion": states,
            "latest_query": "new",
            "final_result": search.result,
            "stale_final_result": search.result["query"] != "new",
        }
    finally:
        # Own and drain every task, including when an assertion or deadline fails.
        for task in tasks.values():
            if not task.done():
                task.cancel()
        if tasks:
            await bounded(asyncio.gather(*tasks.values(), return_exceptions=True))
        for response in request.responses.values():
            if not response.done():
                response.cancel()


def production_hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("search.py", "transport.py")}


async def main():
    before = production_hashes()
    normal = await scenario(["old", "new"])
    reversed_order = await scenario(["new", "old"])
    assert normal["stale_final_result"] is False
    assert reversed_order["stale_final_result"] is True
    after = production_hashes()
    assert before == after, "Production files changed during the experiment"
    report = {
        "request_boundary": "in-process controlled double; no HTTP server or cache",
        "behavior_wait_timeout_seconds": TIMEOUT,
        "production_sha256_before": before,
        "production_sha256_after": after,
        "scenarios": {"normal": normal, "reversed": reversed_order},
        "verification": "passed; all owned search tasks drained",
    }
    output = ROOT / "experiments" / "search_order_results.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
