I’ll use the exorcist skill to compare the cache theory with other causes in a controlled local experiment. I’ll leave production code unchanged.


The search code assigns every completed response to the same result field, with no check for a newer query. I’ll test whether an older request can overwrite a newer result by controlling completion order through a local request stub with no cache.


Confirmed a response-order race in [search.py](project/search.py#L5): each response overwrites `self.result`, even when a newer search has completed.

The controlled experiment used the actual search and transport code with a cache-free local request stub:

| Response completion order | Final result |
|---|---|
| Old → new | New query, correct |
| New → old | Old query, stale |

Only completion order changed. This reproduces the symptom without a cache; it does not establish how often it occurs for users.

Smallest corrective action: track request generation and assign results only when the response belongs to the latest search. No production code was changed.

Reproduce locally: `python3 -B diagnostics/reproduce_search.py`. All experiment assertions passed.
