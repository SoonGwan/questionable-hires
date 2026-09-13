I’ll read the requirements and catalog code, then run deterministic checks without changing existing files or installing dependencies. I’ll save the execution results as JSON in the project.


The component guards responses by request generation. I’ll use manually released async responses to test all success/failure pairs in both completion orders, including an older response arriving while the newer request is pending. The harness will use only the standard library, enforce a time limit, and record each state comparison.


All **19 checks passed** across 10 deterministic scenarios.

| Case | Expected | Observed |
|---|---|---|
| Normal success | Result displayed; error cleared | `normal-result`, error `None` |
| Current failure | Error displayed | `attempt-error`, result `None` |
| Successful retry | Retry result; error cleared | `retry-result`, error `None` |
| Older response arrives while newer pending | State unchanged | Both fields remained `None` |
| Older response arrives after newer completes | Newer state preserved | Newer result or error retained |

Overlap checks covered all four success/failure pairs in both completion orders, using explicitly released futures.

Reproduce from the project root:

```sh
python3 -B qa_catalog.py
```

The harness has a 10-second cooperative timeout and writes a fresh JSON record each run. Actual execution: [JSON record](project/qa_catalog_execution_863660589e224e958090ea08fc27417d.json).

Limits: Python component only; failures tested with `RuntimeError`. Cancellation, other exceptions, and three-plus overlapping requests were not exercised. Result retention after failure is unspecified. The timeout cannot interrupt synchronous blocking code.

Existing files remained unchanged, verified by hashes. No dependencies installed or external services used.
