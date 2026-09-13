I’ll use the exorcist skill to test whether cache behavior or request completion order explains the stale results, while leaving production files unchanged.



`Search.run` assigns every completed response to `result`, with no check that it belongs to the newest query. The transport sends `Cache-Control: no-cache`. I’ll exercise both real modules with a recording request stub, completing the same two searches in normal and reversed order to see whether the older response can overwrite the newer one.



The local experiment confirms a completion-order race: `Search.run` stores whichever response finishes last, even when it belongs to an earlier query.

- Normal completion: final result is `newer`.
- Reversed completion: `earlier` overwrites `newer`.
- Both actual transport requests recorded `Cache-Control: no-cache`. That header does not guard result assignment order; no cache was needed to reproduce this failure.

Rerun the [experiment](project/experiments/search_completion_probe.py):

```sh
python3 -B experiments/search_completion_probe.py
```

Assertions passed. Behavior-dependent waits have two-second limits, and owned tasks are cleaned up. Production files and existing user changes were preserved.

This establishes the local mechanism, not the cause of every production incident. Production confirmation needs correlated query submissions, response completions, and result assignments.
