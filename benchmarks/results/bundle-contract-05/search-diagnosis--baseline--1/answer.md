I’ll inspect Search and its transport, then build a local experiment that records request headers and controls completion order without changing production files.

Search assigns every completed response to the same result field, with no check that it belongs to the latest query. The transport sends `Cache-Control: no-cache`. I’ll test whether reversing two responses reproduces the stale result using a local request stub with no cache.

The experiment reproduced the stale result: normal completion order leaves the newer result visible; reversed order lets the older response overwrite it. Both runs recorded the expected query parameters and `Cache-Control: no-cache`. This establishes a response-order race locally; it doesn’t establish which conditions occur in production.

Local evidence confirms a response-order race: `Search.run` lets an older response overwrite the newer result when completions arrive in reverse order.

- Normal order: newer result remains.
- Reversed order: older result overwrites it.
- Actual Search and transport exercised; all requests recorded `Cache-Control: no-cache`.

No cache was needed to reproduce this. Production timing and cache behavior remain unverified.

[Experiment](project/experiment_search.py), [recorded evidence](project/experiment_search_results.json), and [diagnosis](project/experiment_search_notes.md) are saved locally. Rerun with `python3 -B experiment_search.py`.

Waits are bounded and owned tasks cleaned up. Production files are unchanged.
