I’ll inspect Search and its transport, then build a local experiment that records headers and controls response order. I’ll preserve production files and existing changes.

`Search.run` assigns every completed response to the same result field, with no check for a newer query. The transport sends `Cache-Control: no-cache`. I’ll test whether reversing two responses produces stale results even when the local request double has no cache.

The experiment reproduced stale results: normal completion left the new result visible; reversed completion let the old response overwrite it. Both runs used the actual Search and transport, and recorded `Cache-Control: no-cache`. This establishes a local response-ordering bug without a cache; production timing and cache behavior remain untested.

Reproduced a response-ordering bug: `Search.run` unconditionally writes each completed response. An older response can overwrite the newer result.

- Normal completion: final result is **new**.
- Reversed completion: final result is **old**.
- Actual Search and transport exercised; both requests recorded `Cache-Control: no-cache`. No cache was present.

Production timing and cache behavior remain unverified. Production files are unchanged. Waits are bounded and owned tasks cleaned up.

Rerun: `python3 -B experiments/search_order.py`

[Experiment notes](project/experiments/README.md) · [Recorded results](project/experiments/search_order_results.json)
