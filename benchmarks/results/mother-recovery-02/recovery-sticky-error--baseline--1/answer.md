I’ll inspect the requirements and lookup code, run deterministic checks, and save a JSON execution record without changing existing files or installing dependencies.

The code appears to leave the error set after a successful retry. I’ll verify that behavior and test all four combinations of older/newer success and failure, using controlled futures to determine response order without timing sleeps.

**Found one requirement failure:** a successful retry updates the result but leaves the previous error visible. The success branch in [lookup.py](project/lookup.py#L16) never clears `error`.

Executed 8 scenarios with 20 state checks: **19 passed, 1 failed**.

| Scenario | Expected `(result, error)` | Observed |
|---|---|---|
| Normal success | `("catalog-result", None)` | Matches |
| Current failure | `(None, "current-error")` | Matches |
| Successful retry | `("retry-result", None)` | `("retry-result", "current-error")` |
| Older success/failure after newer success | `("newer-success", None)` remains | Matches both |
| Older success/failure after newer failure | `(None, "newer-failure")` remains | Matches both |
| Older success/failure while newer pending | `(None, None)`, then newer result | Matches both |

Ordering used explicitly resolved futures and fetch-entry events, with no timing sleeps.

Reproduce from the project root:

```sh
python3 -B qa_catalog_lookup.py
```

The harness has a 15-second async timeout and 1-second individual waits. It returns exit code `1` for the reproduced failure and creates a fresh JSON record each run.

[Retained actual execution JSON](project/qa_catalog_lookup_execution_445a7c34b6794551a3cbe51290401b7d.json) includes expected/observed states, runtime details, and matching before/after input hashes.

Limits: Python component only; failures tested as `RuntimeError`. Cancellation, other exceptions, browser/backend behavior, and exhaustive interleavings were not tested. Async timeouts cannot preempt synchronous blocking. Existing files remained unchanged; no dependencies were installed.
