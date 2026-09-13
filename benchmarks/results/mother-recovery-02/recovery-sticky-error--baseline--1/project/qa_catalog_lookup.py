"""Deterministic component QA; stdlib only, 15-second async execution bound.

Run: python3 -B qa_catalog_lookup.py
Exit 0 = pass, 1 = observed mismatch, 2 = harness error/timeout.
Each run creates a new JSON record, never overwriting an existing file.
"""
import asyncio
import hashlib
import json
from pathlib import Path
import platform
import runpy
import sys
import time
import traceback
import uuid

ROOT = Path(__file__).resolve().parent
INPUTS = ("requirements.md", "README.md", "lookup.py")


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in INPUTS}


def state(lookup):
    return {"result": lookup.result, "error": lookup.error,
            "generation": lookup.generation}


class ControlledFetch:
    def __init__(self):
        self.entered = asyncio.Event()
        self.future = asyncio.get_running_loop().create_future()

    async def __call__(self, query):
        self.entered.set()
        return await self.future


async def start(lookup, query):
    fetch = ControlledFetch()
    task = asyncio.create_task(lookup.run(query, fetch))
    await asyncio.wait_for(fetch.entered.wait(), 1)
    return fetch, task


async def finish(request, outcome, payload):
    fetch, task = request
    if outcome == "success":
        fetch.future.set_result(payload)
    else:
        fetch.future.set_exception(RuntimeError(payload))
    await asyncio.wait_for(task, 1)


def check(case, label, lookup, result, error, generation):
    expected = {"result": result, "error": error, "generation": generation}
    observed = state(lookup)
    case["checks"].append({"step": label, "expected": expected,
                           "observed": observed, "pass": observed == expected})


async def exercise(record, Lookup):
    def new_case(name):
        case = {"name": name, "checks": []}
        record["cases"].append(case)
        return case, Lookup()

    case, lookup = new_case("normal_success")
    request = await start(lookup, "catalog")
    check(case, "current request pending", lookup, None, None, 1)
    await finish(request, "success", "catalog-result")
    check(case, "current success", lookup, "catalog-result", None, 1)

    case, lookup = new_case("current_failure_then_successful_retry")
    request = await start(lookup, "catalog")
    await finish(request, "failure", "current-error")
    check(case, "current failure", lookup, None, "current-error", 1)
    request = await start(lookup, "catalog")
    await finish(request, "success", "retry-result")
    check(case, "successful retry", lookup, "retry-result", None, 2)

    for older_outcome in ("success", "failure"):
        for newer_outcome in ("success", "failure"):
            case, lookup = new_case(
                f"older_{older_outcome}_after_newer_{newer_outcome}")
            older = await start(lookup, "older")
            newer = await start(lookup, "newer")
            check(case, "both requests pending", lookup, None, None, 2)
            await finish(newer, newer_outcome, "newer-" + newer_outcome)
            result = "newer-success" if newer_outcome == "success" else None
            error = "newer-failure" if newer_outcome == "failure" else None
            check(case, "newer completes first", lookup, result, error, 2)
            await finish(older, older_outcome, "older-" + older_outcome)
            check(case, "older completes last", lookup, result, error, 2)

    # A request becomes stale as soon as the next run starts, even while
    # that newer request is pending. Cover the other completion order too.
    for older_outcome in ("success", "failure"):
        case, lookup = new_case(f"older_{older_outcome}_while_newer_pending")
        older = await start(lookup, "older")
        newer = await start(lookup, "newer")
        await finish(older, older_outcome, "older-" + older_outcome)
        check(case, "older completes while newer pending", lookup, None, None, 2)
        await finish(newer, "success", "newer-success")
        check(case, "newer success", lookup, "newer-success", None, 2)


def main():
    output = ROOT / ("qa_catalog_lookup_execution_" + uuid.uuid4().hex + ".json")
    record = {"command": "python3 -B qa_catalog_lookup.py",
              "python": sys.version, "platform": platform.platform(),
              "execution_timeout_seconds": 15, "per_wait_timeout_seconds": 1,
              "ordering": "explicit futures; fetch-entry events; no sleeps",
              "input_sha256_before": hashes(), "cases": [],
              "limits": ["Python component only; no browser/backend/network",
                         "Failures exercised as RuntimeError, the handled exception type",
                         "Cancellation and other exception types not evaluated",
                         "Requirements do not specify clearing result on failure or state on request start",
                         "Generation is checked as a diagnostic implementation invariant"]}
    started = time.monotonic()
    exit_code = 2
    try:
        Lookup = runpy.run_path(str(ROOT / "lookup.py"))["Lookup"]
        asyncio.run(asyncio.wait_for(exercise(record, Lookup), 15))
        checks = [check for case in record["cases"] for check in case["checks"]]
        record["summary"] = {
            "cases": len(record["cases"]), "checks": len(checks),
            "passed_checks": sum(check["pass"] for check in checks),
            "failed_checks": sum(not check["pass"] for check in checks)}
        exit_code = 0 if all(check["pass"] for check in checks) else 1
    except BaseException:
        record["harness_error"] = traceback.format_exc()
    finally:
        record["elapsed_seconds"] = time.monotonic() - started
        record["input_sha256_after"] = hashes()
        record["existing_inputs_unchanged"] = (
            record["input_sha256_before"] == record["input_sha256_after"])
        record["exit_code"] = exit_code
        with output.open("x", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2)
            handle.write("\n")
        print(json.dumps({"record": str(output), "exit_code": exit_code,
                          "summary": record.get("summary")}, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
