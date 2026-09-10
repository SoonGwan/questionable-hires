I’ll use the exorcist skill to trace the search path and run a controlled local experiment that tests the cache hypothesis. I’ll leave production code unchanged.


The search code assigns every completed response to the same result field, with no check that it belongs to the latest query. The transport requests cache revalidation via `Cache-Control: no-cache`, but that alone doesn’t rule out caching. I’ll use a local request stub with no cache and hold the responses so I can compare completion orders.


The cause is an out-of-order response race: `Search.run` unconditionally assigns each response to `self.result`, so an older request completing last overwrites newer results.

The local experiment used the real search and transport functions with a cache-free request stub:

- Earlier response first → correct newer results.
- Newer response first → older results overwrite them.

Only completion order changed. This reproduces the symptom without caching; it doesn’t establish whether any external cache has separate issues.

Smallest corrective action: track request sequence and accept results only from the latest search.

Production code is unchanged. Reproduce with `python3 -B diagnose_search.py`; assertions passed.
