I’ll use the exorcist skill to test where search results become stale, with controlled request completions and recorded headers. I’ll keep the experiment local and leave production code unchanged.


`Search.run` assigns every completed response to the same result field. The transport sends `Cache-Control: no-cache`, but there’s no check that a response belongs to the latest query. I’ll run both completion orders through these actual functions, using a local recording request dependency with no cache.


The local experiment confirms an out-of-order response overwrite: `Search.run` stores whichever response completes last.

- Normal completion (`old → new`): final result is `new`.
- Reversed completion (`new → old`): the older result overwrites `new`.
- Actual Search and transport ran; recorded requests both included `Cache-Control: no-cache`. That header does not guard result assignment against late responses.

Rerun the [experiment](project/experiments/search_order_probe.py):

```sh
python3 -B experiments/search_order_probe.py
```

Verification passed. Waits have one-second bounds, owned tasks are cleaned up, and production files remain unchanged.

No cache was needed to reproduce this symptom. Establishing the cause of production incidents still requires correlated query submissions, response completions, and result assignments; production cache behavior was not tested.
