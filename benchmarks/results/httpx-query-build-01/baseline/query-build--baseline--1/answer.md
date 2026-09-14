I’ll reproduce all four cases with the specified interpreter, then trace how this checkout handles URL queries and client/request params. I’ll keep the work read-only and offline.

All four cases reproduce the reported loss. The code treats non-`None` params as a replacement for the URL’s entire query; client and request params are merged separately. I also verified a caller-side composition that preserves repeated values with an explicit precedence order.

Reproduced offline with actual `Client.build_request`, using the specified interpreter and confirming `httpx` imported from this checkout. No requests were sent.

| Case | Built URL | Ordered `url.params.multi_items()` |
|---|---|---|
| 1. No defaults; params omitted | `https://example.invalid/items?from=url&tag=url1&tag=url2` | `[('from', 'url'), ('tag', 'url1'), ('tag', 'url2')]` |
| 2. No defaults; `params={}` | `https://example.invalid/items` | `[]` |
| 3. Client tenant; params omitted | `https://example.invalid/items?tenant=client` | `[('tenant', 'client')]` |
| 4. Client tenant/tags; request tags/page | `https://example.invalid/items?tenant=client&tag=request1&tag=request2&page=2` | `[('tenant', 'client'), ('tag', 'request1'), ('tag', 'request2'), ('page', '2')]` |

The cause is query replacement during construction, not encoding or request caching:

- [`Client._merge_queryparams`](project/httpx/_client.py#L433) merges **client and request params only**. URL query values do not participate. If neither params collection is truthy, it returns the request argument unchanged—preserving the distinction between `None` and `{}`.
- [`Request.__init__`](project/httpx/_models.py#L399) uses `URL(url)` for `params is None`, preserving the embedded query. Otherwise it uses `URL(url, params=params)`.
- [`URL.__init__`](project/httpx/_urls.py#L107) turns supplied params into a replacement query. Empty params remove the query, including the `?`.
- [`QueryParams.merge`](project/httpx/_urls.py#L582) lets request keys replace the client’s entire value list for that key. Thus case 4 retains both request tags, replaces both client tags, and retains `tenant`.

For an adapter, preserve omission instead of automatically converting it to `{}`. That alone handles case 1, but cannot preserve URL values when nonempty client defaults apply.

Where combining queries is intended, compose them explicitly at that caller boundary. For example, **if the agreed precedence is client defaults < URL values < explicit request params**:

```python
parsed = httpx.URL(url)
combined = client.params.merge(parsed.params).merge(request_params)
request = client.build_request(
    "GET",
    parsed.copy_with(query=None),
    params=combined,
)
```

I verified this approach offline. Use `QueryParams` directly rather than `dict(parsed.params)`, which loses repeated values. Each winning key retains its complete value list; collisions deliberately replace lower-priority lists. Agree on precedence before adopting this order—URL-versus-client precedence is an application choice. `QueryParams` preserves repeated values but groups them by key, so this approach does not promise original query bytes or interleaving.

No existing files were modified, no diagnostic files were created, and the working tree remains clean.
