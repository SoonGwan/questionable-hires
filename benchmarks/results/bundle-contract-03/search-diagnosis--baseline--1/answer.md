I’ll inspect the search flow and build a local experiment that records request headers and controls response order, without changing production code.

`Search.run` assigns every completed response to the same result field, with no check for a newer query. The transport sends `Cache-Control: no-cache`. I’ll test both completion orders through these actual functions, using a controlled request boundary with no cache.

Reproduced a response-order race: `Search.run` writes every completed response into `result`.

- Normal completion: newer query wins.
- Reversed completion: older response overwrites newer results.
- Actual Search and transport were exercised; all four requests recorded `Cache-Control: no-cache`.

This reproduces stale results without a cache. It does not establish production response ordering or exclude additional production cache issues.

Rerun: `python3 -B experiment_search_order.py`

[Experiment](project/experiment_search_order.py) · [Recorded evidence](project/experiment_search_order.results.json)

Waits are bounded to two seconds, owned tasks are cleaned up, and production files remain unchanged, verified by hashes and Git diff.
