I’ll use the exorcist skill to test the cache hypothesis against other possible causes locally, without changing production code.

Each completed request assigns directly to `Search.result`, with no check that its query is still current. I’ll test whether completion order alone can produce stale results using a local request stub with no cache and explicitly controlled responses.

Confirmed a response-order race: `Search.run` assigns every completed response to `self.result`, so a slower earlier search overwrites newer results.

The local experiment used no cache or network and changed only completion order:

- Earlier finishes first → newer results remain.
- Newer finishes first → earlier results overwrite them.

This reproduces the symptom without a cache. The smallest corrective action would be to accept responses only from the latest request; no fix was applied.

Production files are unchanged. Reproduce with `python3 -B diagnose_search.py`; both diagnostic cases passed their assertions.
