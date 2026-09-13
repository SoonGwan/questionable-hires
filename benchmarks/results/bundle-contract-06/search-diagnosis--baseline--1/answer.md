I’ll inspect Search and the transport, then build a local experiment that records headers and controls completion order. I’ll preserve production files and existing changes.

`Search.run` assigns every completed response to `self.result`, with no check for a newer query. The transport sends `Cache-Control: no-cache`. I’ll test whether reversing two response completions reproduces stale results using a request stub with no cache.

The experiment reproduced stale results without a cache: normal completions leave the newer result visible, while reversed completions let the older response overwrite it. Both requests passed through the actual transport with `Cache-Control: no-cache`. This establishes a local response-order race; it doesn’t establish how production caches behave.

Reproduced a response-order race: `Search.run` lets an older response overwrite a newer result.

- Normal completions: newer result remains.
- Reversed completions: older result overwrites it.
- Actual Search and transport exercised; both requests recorded `Cache-Control: no-cache`.

The stub has no cache, proving caching is unnecessary for this reproduction. Production cache behavior remains unverified.

Rerun: `python3 -B experiments/search_order.py`

[Report](project/experiments/README.md) · [Recorded evidence](project/experiments/evidence.json)

Waits are bounded and owned tasks cleaned up. Production files remain unchanged.
