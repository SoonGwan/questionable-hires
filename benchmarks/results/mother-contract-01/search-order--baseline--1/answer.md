I’ll inspect the Search flow and local test setup, then build a deterministic overlap test without changing production files.

`Search.run` assigns every completed response to the displayed result. That appears to let an older query overwrite a newer one. I’ll test both completion orders using gated responses and verify that both requests are pending before releasing either response.

Confirmed a stale-response bug: typing `ca` then `cat` lets a late `ca` response overwrite the latest result.

- Normal completion: passed.
- Reversed completion: failed—expected `results for cat`, got `results for ca`.
- Both requests verified pending before release; waits bounded and owned tasks cleaned up.
- Production files unchanged.

[Rerun instructions](project/qa/README.md) · [Test](project/qa/test_search_overlap.py) · [Captured assertions and controls](project/qa/search_overlap_run.txt)
