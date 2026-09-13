"""Deterministic, standard-library-only QA; writes a new JSON execution record."""
import argparse
import asyncio
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from lookup import Lookup


ROOT = Path(__file__).resolve().parent
RECORD = {"scenarios": []}


def state(lookup):
    return {"result": lookup.result, "error": lookup.error}


def check(scenario, label, lookup, expected):
    observed = state(lookup)
    scenario["checks"].append({"label": label, "expected": expected.copy(),
                               "observed": observed, "pass": observed == expected,
                               "generation": lookup.generation})


class ControlledFetch:
    def __init__(self, scenario):
        self.scenario = scenario
        self.started = {}
        self.responses = {}

    async def __call__(self, query):
        self.scenario["events"].append({"event": "fetch_started", "query": query})
        self.started[query].set()
        return await self.responses[query]

    async def start(self, lookup, query):
        self.started[query] = asyncio.Event()
        self.responses[query] = asyncio.get_running_loop().create_future()
        task = asyncio.create_task(lookup.run(query, self))
        await self.started[query].wait()
        return task

    async def finish(self, query, task, outcome):
        payload = query + ("-result" if outcome == "success" else "-error")
        self.scenario["events"].append({"event": "release_response", "query": query,
                                        "outcome": outcome, "payload": payload})
        if outcome == "success":
            self.responses[query].set_result(payload)
        else:
            self.responses[query].set_exception(RuntimeError(payload))
        await task
        self.scenario["events"].append({"event": "run_completed", "query": query})


def scenario(name):
    item = {"name": name, "events": [], "checks": []}
    RECORD["scenarios"].append(item)
    return item, Lookup(), ControlledFetch(item)


async def suite():
    item, lookup, fetch = scenario("normal_success")
    task = await fetch.start(lookup, "normal")
    await fetch.finish("normal", task, "success")
    check(item, "current success", lookup, {"result": "normal-result", "error": None})

    item, lookup, fetch = scenario("current_failure_then_successful_retry")
    task = await fetch.start(lookup, "attempt")
    await fetch.finish("attempt", task, "failure")
    check(item, "current failure", lookup, {"result": None, "error": "attempt-error"})
    task = await fetch.start(lookup, "retry")
    await fetch.finish("retry", task, "success")
    check(item, "successful retry", lookup, {"result": "retry-result", "error": None})

    for order in (("new", "old"), ("old", "new")):
        for old_outcome in ("success", "failure"):
            for new_outcome in ("success", "failure"):
                name = f"overlap_old_{old_outcome}_new_{new_outcome}_complete_{order[0]}_first"
                item, lookup, fetch = scenario(name)
                tasks = {"old": await fetch.start(lookup, "old"),
                         "new": await fetch.start(lookup, "new")}
                expected = {"result": None, "error": None}
                outcomes = {"old": old_outcome, "new": new_outcome}
                for query in order:
                    await fetch.finish(query, tasks[query], outcomes[query])
                    if query == "new":
                        if new_outcome == "success":
                            expected = {"result": "new-result", "error": None}
                        else:
                            expected = {"result": None, "error": "new-error"}
                    check(item, f"after {query} {outcomes[query]}", lookup, expected)


def source_hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("lookup.py", "requirements.md", "README.md")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--output", default="qa_catalog_lookup_execution.json")
    args = parser.parse_args()
    if not 0 < args.timeout <= 60:
        parser.error("timeout must be greater than zero and at most 60 seconds")
    output = ROOT / args.output
    if output.parent.resolve() != ROOT or output.suffix != ".json":
        parser.error("output must be a JSON file at the project root")
    # Exclusive creation prevents overwriting any existing file.
    with output.open("x", encoding="utf-8") as record_file:
        RECORD.update({"started_utc": datetime.now(timezone.utc).isoformat(),
                       "python": platform.python_version(), "timeout_seconds": args.timeout,
                       "source_sha256_before": source_hashes(),
                       "ordering": "future release and awaited task completion; no sleeps",
                       "scope": "Python Lookup component; controlled in-process fetch",
                       "limits": ["No browser, backend, network, or real latency exercised",
                                  "Failures use RuntimeError, the implemented exception type",
                                  "Two overlapping requests; no cancellation or larger fan-out",
                                  "Requirements do not specify loading state or result clearing on failure"]})
        try:
            asyncio.run(asyncio.wait_for(suite(), timeout=args.timeout))
        except Exception as error:
            RECORD["execution_error"] = {"type": type(error).__name__, "message": str(error)}
        finally:
            checks = [check for item in RECORD["scenarios"] for check in item["checks"]]
            RECORD["source_sha256_after"] = source_hashes()
            RECORD["sources_unchanged"] = RECORD["source_sha256_before"] == RECORD["source_sha256_after"]
            RECORD["summary"] = {"scenarios": len(RECORD["scenarios"]),
                                 "checks": len(checks), "passed": sum(c["pass"] for c in checks),
                                 "failed": sum(not c["pass"] for c in checks)}
            RECORD["finished_utc"] = datetime.now(timezone.utc).isoformat()
            json.dump(RECORD, record_file, indent=2)
            record_file.write("\n")
    print(json.dumps({"record": str(output), **RECORD["summary"]}))
    return int(bool(RECORD.get("execution_error")) or RECORD["summary"]["failed"] > 0
               or not RECORD["sources_unchanged"])


if __name__ == "__main__":
    raise SystemExit(main())
