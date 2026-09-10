I’ll use the exorcist skill to trace the search flow and run a controlled local experiment, leaving production code unchanged.


The search code assigns every response to the displayed result, with no check that it belongs to the latest query. I’ll test that possible race using the real search and transport functions with a cache-free request stub, changing only the response completion order.


Confirmed a response-order race in [search.py](project/search.py#L5): every completed request overwrites `self.result`, including an older request finishing last.

The local experiment used the real search and transport functions with a cache-free, controlled request stub:

| Response completion order | Final result |
|---|---|
| Earlier → newer | Newer, correct |
| Newer → earlier | Earlier, stale |

Identical queries and requests; only completion order changed. This reproduces the symptom without a cache, establishing that caching is unnecessary for this failure. Actual user frequency remains unmeasured.

Smallest corrective action: track a request generation and assign results only if the completing request is still current. **No production code was changed.**

Rerun the diagnostic with `PYTHONDONTWRITEBYTECODE=1 python3 diagnose_search.py`. Both assertions passed.
