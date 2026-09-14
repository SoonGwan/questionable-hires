I’ll use the exorcist skill to compare the four cases with the supplied interpreter, then trace where HTTPX chooses between URL query values and params. I’ll keep the probe offline and use captured output without changing files.

The loss comes from **query replacement**, not encoding or request caching. I reproduced all four cases with actual `Client.build_request` from this checkout, using the supplied interpreter with `-B`. A mock transport would fail on any send; no requests were sent.

For `https://example.invalid/items?from=url&tag=url1&tag=url2`:

| Case | Built URL | Ordered query items (`url.params.multi_items()`) |
|---|---|---|
| 1. No defaults; params omitted | `https://example.invalid/items?from=url&tag=url1&tag=url2` | `[('from', 'url'), ('tag', 'url1'), ('tag', 'url2')]` |
| 2. No defaults; `params={}` | `https://example.invalid/items` | `[]` |
| 3. Default tenant; params omitted | `https://example.invalid/items?tenant=client` | `[('tenant', 'client')]` |
| 4. Default tenant/tag; request tag/page | `https://example.invalid/items?tenant=client&tag=request1&tag=request2&page=2` | `[('tenant', 'client'), ('tag', 'request1'), ('tag', 'request2'), ('page', '2')]` |

The responsible path is:

- [`Client._merge_queryparams`](project/httpx/_client.py#L433) merges **client defaults and request params only**. Embedded URL values do not participate. With neither populated, it returns the request argument unchanged, preserving the distinction between `None` and `{}`.
- [`Request.__init__`](project/httpx/_models.py#L399) uses `URL(url)` when params is `None`, preserving the existing query. Otherwise it uses `URL(url, params=params)`.
- [`URL.__init__`](project/httpx/_urls.py#L107) converts supplied params into a replacement query. Empty params set the query to `None`, removing it. The empty-query safeguard prevents a trailing `?`; it does not preserve embedded values.
- [`QueryParams.merge`](project/httpx/_urls.py#L582) replaces each colliding key’s **whole value list** with the later layer’s list. Thus request tags replace client tags, retaining both request values.

Omission therefore differs from an empty mapping when there are no populated client defaults: omission reaches `Request` as `None`, while `{}` explicitly replaces the query with nothing. Populated client defaults produce replacement params even when request params are omitted.

For a scoped caller-side solution, preserve omission in adapters instead of automatically converting it to `{}`. Where defaults or explicit params must coexist with embedded values, define collision precedence explicitly and assemble the complete query using `QueryParams`. For example, **if the caller’s intended policy is client defaults < URL values < explicit request params**:

```python
parsed = httpx.URL(url)
combined = (
    httpx.QueryParams(client.params)
    .merge(parsed.params)
    .merge(request_params)  # None if omitted
)
request = client.build_request("GET", parsed, params=combined)
```

This preserves repeated values within the winning layer. Avoid `dict(parsed.params)` or `.items()`, which collapse repeated values. If collisions should append values or be rejected, implement that policy explicitly instead of using `.merge()`. Also decide whether an explicit `{}` means “no additions” or “clear query”; this example treats it as no additions.

These observations establish the local construction mechanism; caching is unnecessary to reproduce it. Existing files were unchanged, and no diagnostic files, installs, commits, or network access were used.
