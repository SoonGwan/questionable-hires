I’ll use the exorcist skill to compare the four cases with a small offline probe, then trace where URL queries and client/request params are handled. I’ll leave existing files unchanged and use captured output as the evidence.


The probe reproduces the loss without sending a request: `{}` clears the URL query, and client defaults replace it. The code uses a `None` check at request construction, while client/request params merge by key. I’ll verify the caller-side merge approach, including repeated values and explicit precedence.


Reproduced with the specified interpreter, importing this checkout’s HTTPX and calling actual `Client.build_request`. No requests were sent; a rejecting `MockTransport` guarded against dispatch.

| Case | Built URL | Ordered query items (`multi_items()`) |
|---|---|---|
| 1. Both omitted | `https://example.invalid/items?from=url&tag=url1&tag=url2` | `[('from', 'url'), ('tag', 'url1'), ('tag', 'url2')]` |
| 2. Request `params={}` | `https://example.invalid/items` | `[]` |
| 3. Client defaults only | `https://example.invalid/items?tenant=client` | `[('tenant', 'client')]` |
| 4. Client and request params | `https://example.invalid/items?tenant=client&tag=request1&tag=request2&page=2` | `[('tenant', 'client'), ('tag', 'request1'), ('tag', 'request2'), ('page', '2')]` |

The mechanism is deterministic query replacement:

- In `httpx/_client.py:433`, `_merge_queryparams` merges **client and request params only**. It does not include the URL query.
- In `httpx/_urls.py:582`, `QueryParams.merge` replaces each conflicting key’s entire value list with the right-hand list. Thus case 4 retains `tenant`, replaces both client tags with both request tags, and adds `page`.
- In `httpx/_models.py:399`, `Request` preserves the URL when effective `params is None`; otherwise it constructs `URL(url, params=params)`.
- In `httpx/_urls.py:107`, supplied params replace the query. Empty params set the query to `None`; the existing safeguard prevents a trailing `?`, not query loss.

Omission and `{}` differ because `_merge_queryparams` returns the original argument when both parameter sources are empty: omitted params remain `None`, while `{}` remains a non-`None` mapping. Nonempty client defaults produce effective params even when request params are omitted.

Neither encoding trouble nor caching is needed to reproduce this report. These observations establish the local construction mechanism, not every possible production incident.

For a scoped adapter change, retain omission when no params were supplied. When combining sources, explicitly choose collision precedence and use `QueryParams`, never `dict(url.params)` or `.items()`, which lose repeated values. For example, **if the caller’s intended precedence is URL < client < request**:

```python
combined = (
    httpx.URL(url).params
    .merge(client.params)
    .merge(request_params)
)
request = client.build_request("GET", url, params=combined)
```

This approach was also verified offline. It preserves URL-only keys and all repeated values from each winning source. If URL values should override client defaults, reverse those first two sources. Treat explicit clearing separately: this recipe interprets `{}` as “no additions,” not “erase the query.”

Existing files were unchanged. No dependencies, network access, disposable files, commits, or publication were used.
