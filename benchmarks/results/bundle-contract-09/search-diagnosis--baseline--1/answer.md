I’ll inspect the search flow, then build a rerunnable local experiment that records headers and controls response order without changing production files.

`Search.run` assigns every completed response to the same result field, with no check that its query is still current. The transport sends `Cache-Control: no-cache`. I’ll exercise both modules with a controlled local request function to test whether reversing completion order makes an older result overwrite the newer one.

The experiment reproduced the stale result with no cache present: normal completion order leaves the newer result; reversed order lets the earlier response overwrite it. Both requests passed through the real transport and recorded `Cache-Control: no-cache`. All owned tasks finished, and the production files are unchanged.

Reproduced a response-order race: `Search.run` lets an earlier request overwrite newer results when it finishes last.

- Normal completions leave the newer result; reversed completions leave the earlier result.
- Actual Search and transport exercised; both requests recorded `Cache-Control: no-cache`.
- Waits bounded, owned tasks cleaned up, production files unchanged.

No cache was needed to reproduce this. Production cache behavior remains unverified.

Rerun: `python3 -B experiment_search.py`

[Experiment report](project/experiment_search.md) · [Recorded evidence](project/experiment_search.results.json)
