I’ll use the exorcist skill to compare request dispatch and completion order in the actual Search path, keeping the experiment local and production files unchanged.

Search assigns every completed response to `result`, and transport sends `Cache-Control: no-cache`. I’ll use a standard-library Python probe with a recording request dependency to run both completion orders. This will test whether a late response overwrites the newer result without any cache involved.

Local evidence supports a response-order race: Search assigns each response when it completes.

- Normal completion (`old → new`): final result is `new`.
- Reversed completion (`new → old`): the older response overwrites `new`.
- Actual transport sent `Cache-Control: no-cache` on both requests. That header does not prevent out-of-order updates; this reproduction requires no cache.

Rerun the [local experiment](project/experiments/search_order_probe.py):

```sh
python3 -B experiments/search_order_probe.py
```

Verification passed. The probe records headers and result transitions, bounds waits, and cleans up owned tasks. Production files remain unchanged; existing user changes were preserved.

Production causality remains unconfirmed: request/completion and result-update traces from an affected session would establish whether this mechanism explains those incidents.
