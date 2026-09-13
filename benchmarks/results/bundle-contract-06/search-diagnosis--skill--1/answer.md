I’ll use the exorcist skill to test the cache suspicion against request ordering, exercising the actual Search and transport while leaving production code unchanged.

`Search.run` writes each response into `result` when it completes; it has no check that the response belongs to the latest query. The transport sends `Cache-Control: no-cache`. I’ll test both completion orders using a recording request dependency with no cache, while keeping the real Search and transport in the path.

Local evidence confirms a completion-order race: `Search.run` lets an older response overwrite newer results.

The [rerunnable experiment](project/experiments/search_order_probe.py) exercises actual Search and transport with a cache-free recording request dependency:

- Normal completion: newer result remains.
- Reversed completion: older result overwrites newer.
- Every recorded request includes `Cache-Control: no-cache`; that header does not guard result assignment.

Run: `python3 -B experiments/search_order_probe.py` — passed, printing the full trace. Behavior-dependent waits are bounded; owned tasks are cleaned up.

Cache is unnecessary for this reproduction. Production attribution still requires observing overlapping queries, completion order, and result writes; production cache behavior remains untested.

Production files are unchanged, and existing user files were preserved.
