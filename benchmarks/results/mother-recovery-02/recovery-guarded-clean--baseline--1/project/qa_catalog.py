"""Deterministic, standard-library-only QA. Creates a fresh JSON record per run."""
import sys
sys.dont_write_bytecode = True

import asyncio
import hashlib
import itertools
import json
import platform
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

from lookup import Lookup

ROOT = Path(__file__).resolve().parent
SOURCES = ("lookup.py", "requirements.md", "README.md")


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in SOURCES}


class Case:
    def __init__(self, record):
        self.record = record
        self.lookup = Lookup()
        self.futures = {}
        self.tasks = {}
        self.events = {}

    async def start(self, query):
        self.futures[query] = asyncio.get_running_loop().create_future()
        self.events[query] = asyncio.Event()

        async def fetch(q):
            self.events[q].set()
            return await self.futures[q]

        self.tasks[query] = asyncio.create_task(self.lookup.run(query, fetch))
        await self.events[query].wait()
        self.record["actions"].append({"start": query})

    async def finish(self, query, outcome):
        if outcome == "success":
            self.futures[query].set_result(query + " result")
        else:
            self.futures[query].set_exception(RuntimeError(query + " error"))
        await self.tasks[query]
        self.record["actions"].append({"complete": query, "outcome": outcome})

    def check(self, label, result, error, generation):
        expected = dict(result=result, error=error, generation=generation)
        observed = {key: getattr(self.lookup, key) for key in expected}
        self.record["checkpoints"].append(dict(
            label=label, expected=expected, observed=observed,
            passed=expected == observed))


async def normal(c):
    c.check("initial", None, None, 0)
    await c.start("normal")
    c.check("pending", None, None, 1)
    await c.finish("normal", "success")
    c.check("current success", "normal result", None, 1)


async def retry(c):
    await c.start("first")
    await c.finish("first", "failure")
    c.check("current failure", None, "first error", 1)
    await c.start("retry")
    # The requirements do not specify clearing state at request start.
    await c.finish("retry", "success")
    c.check("successful retry clears error", "retry result", None, 2)


async def overlap(c, older, newer, order):
    await c.start("older")
    await c.start("newer")
    c.check("both pending", None, None, 2)
    outcomes = {"older": older, "newer": newer}
    result = error = None
    for query in order:
        await c.finish(query, outcomes[query])
        if query == "newer":
            if newer == "success":
                result, error = "newer result", None
            else:
                error = "newer error"
        c.check(query + " completed", result, error, 2)


async def run(record):
    cases = [("normal success", normal), ("failure then retry", retry)]
    for older, newer, newest_first in itertools.product(
            ("success", "failure"), ("success", "failure"), (False, True)):
        order = ("newer", "older") if newest_first else ("older", "newer")
        async def scenario(c, older=older, newer=newer, order=order):
            await overlap(c, older, newer, order)
        cases.append((f"older {older}, newer {newer}, order {order}", scenario))
    for name, scenario in cases:
        item = dict(name=name, actions=[], checkpoints=[])
        record["cases"].append(item)
        await asyncio.wait_for(scenario(Case(item)), timeout=1.0)


def main():
    record = dict(started_utc=datetime.now(timezone.utc).isoformat(),
                  python=platform.python_version(), sources_before=hashes(),
                  reproduction="python3 -B qa_catalog.py",
                  timeout_seconds=15, cases=[],
                  method="Event handshakes and explicitly settled futures; no network or sleeps",
                  limits=["Python component only; no browser or backend",
                          "RuntimeError failures only; other exceptions and cancellation unspecified",
                          "Two overlapping requests; no stress/performance testing",
                          "Pending-state policy and retention of prior results on failure unspecified"])
    started = time.monotonic()
    try:
        asyncio.run(asyncio.wait_for(run(record), timeout=15.0))
    except BaseException:
        record["execution_error"] = traceback.format_exc()
    record["sources_after"] = hashes()
    record["existing_sources_unchanged"] = record["sources_before"] == record["sources_after"]
    checks = [point for case in record["cases"] for point in case["checkpoints"]]
    record["summary"] = dict(cases=len(record["cases"]), checks=len(checks),
                             passed=sum(p["passed"] for p in checks))
    record["passed"] = (len(record["cases"]) == 10 and len(checks) == 29
                        and all(p["passed"] for p in checks)
                        and "execution_error" not in record
                        and record["existing_sources_unchanged"])
    record["elapsed_seconds"] = time.monotonic() - started
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = ROOT / f"qa_catalog_execution_{stamp}.json"
    with path.open("x") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    print(json.dumps(dict(record=str(path), passed=record["passed"], summary=record["summary"])))
    return 0 if record["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
