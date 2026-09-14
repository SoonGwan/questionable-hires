I’ll inspect the search flow, then build a local experiment that records transport headers and controls response order. I’ll preserve production files and existing changes.

`Search.run` assigns every completed response to the same result field. The transport sends `Cache-Control: no-cache`, but there’s no check that a response belongs to the latest query. I’ll test both completion orders through those actual functions, using a controlled request stub with no cache.

The experiment reproduced the stale result: when the newer request finishes first, the older response overwrites it. Normal completion order ends with the newer result. Both runs recorded `Cache-Control: no-cache`; the stub has no cache, so this race can explain the symptom independently of caching. Production cache behavior remains untested.

Reproduced a response-order race: `Search.run` lets an older response overwrite newer results.

- Normal completions: newer result wins.
- Reversed completions: older result overwrites newer.
- Actual Search and transport exercised; all requests recorded `Cache-Control: no-cache`. No cache existed in the stub.

This demonstrates a local cause; production cache behavior remains untested. Production files are unchanged. Waits are bounded and owned tasks cleaned up.

Rerun: `python3 experiments/search_completion_order.py`

[Experiment and findings](project/experiments/README.md) · [Recorded results](project/experiments/search_completion_order.results.json)
