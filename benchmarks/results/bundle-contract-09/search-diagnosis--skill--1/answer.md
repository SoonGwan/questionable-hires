I’ll use the exorcist skill to test the cache suspicion against request completion order, using the actual Search and transport while leaving production files unchanged.


Search assigns each response when it completes, and transport sends `Cache-Control: no-cache`. I’ll run a small standard-library probe with a recording request dependency, releasing responses in normal and reversed order. This will test whether completion order alone can reproduce the stale result without a cache.


The local experiment reproduced a completion-order race: `Search.run` assigns every response, so an earlier request finishing last overwrites newer results.

- Normal completion: newer results remain.
- Reversed completion: earlier results overwrite newer results.
- Actual transport recorded `Cache-Control: no-cache` on every request. That header provides no protection against response ordering.

Rerun the [probe](project/experiments/search_order_probe.py):
```sh
python3 -B experiments/search_order_probe.py
```

All checks passed. Waits are bounded and owned tasks are cleaned up. Production files and existing user changes were preserved.

No cache was needed for this reproduction. Confirming production incidents still requires observing request overlap, completion order, and result assignments; production cache behavior remains untested.
