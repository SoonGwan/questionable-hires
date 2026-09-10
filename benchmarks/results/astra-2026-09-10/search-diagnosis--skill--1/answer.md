I’m using the exorcist skill to compare the cache theory with other causes and run a controlled local experiment. I’ll keep production code unchanged.

The search code assigns every response to the same result field, with no check that it belongs to the latest query. I’ll use a cache-free fake transport and control response order: first complete requests in order, then complete the older request last. This will test whether response timing alone reproduces the symptom.

Confirmed locally: **out-of-order responses overwrite newer results**. `Search.run` assigns every completed response to `self.result`.

The controlled, cache-free experiment showed:

- Older request finishes first → correct final result.
- Older request finishes last → overwrites the newer result.

Only completion order changed; both requests carried the correct query. A cache is therefore unnecessary to reproduce the bug.

Smallest corrective action: track a request generation and update results only when the response belongs to the latest generation. No production code was changed.

Reproduce with `python3 -B diagnose_search.py` using [the diagnostic script](project/diagnose_search.py).
