I’ll inspect the requirements and catalog lookup, then run deterministic checks without changing existing files or installing dependencies. I’ll save the execution results as JSON in the project.

The success path updates the result but never clears an existing error, which appears to violate the retry requirement. I’ll verify that and test overlapping requests with explicitly controlled completion order, covering both successes and failures.

Found one requirement violation: **successful retry retains the previous error**. Executed 10 scenarios: 18/19 state checks passed.

| Case | Expected `(result, error)` | Observed |
|---|---|---|
| Normal success | `("normal-result", null)` | Matches |
| Current failure | `(null, "attempt-error")` | Matches |
| Successful retry | `("retry-result", null)` | `("retry-result", "attempt-error")` |
| Overlapping requests | Older responses never alter state; newest response determines outcome | Matches in all 8 combinations |

Overlap checks covered both completion orders and every success/failure pairing. Futures controlled response release deterministically, without sleeps.

Reproduce from the project root with a five-second suite timeout:

```sh
python3 -B qa_catalog_lookup.py --timeout 5 --output qa_catalog_lookup_rerun.json
```

Exit code `1` indicates the detected failure. Use a fresh output filename; existing files are never overwritten.

Retained [execution JSON](project/qa_catalog_lookup_execution.json) includes expected/observed states, ordered events, timestamps, and source hashes.

Limits: Python component only; simulated `RuntimeError` failures; two overlapping requests. No browser, backend, cancellation, or larger concurrency tests. Existing files remained unchanged; no dependencies installed.
