I’ll use the landlord skill to trace QueryParams and its request-building consumer, then run the specified tests and probes. I’ll preserve the repository and installed resources and use no network access.

All 14 QueryParams tests passed. The probes show three behavior changes and one preserved control: spaces still encode as `+`. The consumer trace also confirms that request values replace all client values for the same key while leaving the client defaults unchanged; a viable repair must retain that policy.

**Keep QueryParams.** The proposed `urlencode(dict(raw_input))` cannot preserve current behavior or consumers. QueryParams already delegates encoding to stdlib `urlencode`; the maintained layer supplies normalization, repeated values, and immutable operations. Removing it would move those policies into replacement helpers or callers. See [construction and normalization](project/httpx/_urls.py#L425) and [serialization](project/httpx/_urls.py#L623).

Executed locally, using the requested interpreter with `-B`:

| Actual `raw_input` | `str(httpx.QueryParams(raw_input))` | `multi_items()` | `urlencode(dict(raw_input))` |
|---|---|---|---|
| `[('a', '1'), ('a', '2'), ('keep', 'x')]` | `a=1&a=2&keep=x` | `[('a', '1'), ('a', '2'), ('keep', 'x')]` | `a=2&keep=x` |
| `{'enabled': True, 'empty': None}` | `enabled=true&empty=` | `[('enabled', 'true'), ('empty', '')]` | `enabled=True&empty=None` |
| `{'a': ['1', '2']}` | `a=1&a=2` | `[('a', '1'), ('a', '2')]` | `a=%5B%271%27%2C+%272%27%5D` |
| `{'a': 'one two', 'keep': 'x'}` | `a=one+two&keep=x` | `[('a', 'one two'), ('keep', 'x')]` | `a=one+two&keep=x` |

The first conversion loses duplicates before encoding. The second loses HTTPX’s boolean/`None` normalization. The third encodes the list’s string representation. The fourth is the preserved control: scalar strings, key order, and space-to-`+` encoding agree. These contracts are covered by [the existing model tests](project/tests/models/test_queryparams.py#L6).

After `derived = base.add('a', '3')`, the actual observations were:

```text
base:
  a=1&a=2&keep=x
  [('a', '1'), ('a', '2'), ('keep', 'x')]
derived:
  a=1&a=2&a=3&keep=x
  [('a', '1'), ('a', '2'), ('a', '3'), ('keep', 'x')]
```

The specified context-managed client built:

```text
https://example.invalid/path?a=7&a=8&keep=x

client.params afterward:
  a=1&a=2&keep=x
  [('a', '1'), ('a', '2'), ('keep', 'x')]
```

`client.params is base` was `False`; both `base` and `derived` remained as recorded above.

The actual consumer is [`build_request()` → `_merge_queryparams()`](project/httpx/_client.py#L340). The [merge helper](project/httpx/_client.py#L433) copies client params and invokes `merge(params)`. [QueryParams.merge](project/httpx/_urls.py#L582) normalizes incoming values and overlays their whole per-key lists: `['7', '8']` replaces `['1', '2']`, retaining `keep=x`. It neither appends client values nor collapses incoming duplicates.

Ownership is deliberate: construction from QueryParams copies its value lists; `add()` copies the dictionary and creates a new list for the changed key. Functional operations can share untouched internal lists because the public API does not mutate them; `get_list()` returns a copy. A shallow mutable `dict` would require additional ownership rules to avoid list aliasing.

The nearest viable repair would need to retain these responsibilities:

- **Normalization:** a shared adapter must handle mappings, pair sequences, query strings/bytes, and QueryParams; preserve blank values; stringify keys; and normalize boolean/`None` values. This policy currently lives in the constructor and [`primitive_value_to_str`](project/httpx/_utils.py#L15).
- **Repeated values:** `doseq=True` repairs the list example, but cannot recover duplicates already discarded by `dict()`, or fix normalization. A viable representation needs grouped value lists or normalized repeated pairs. Flattened scalar pairs work with default `doseq=False`, as the current implementation demonstrates.
- **Merge and ownership:** helpers must replace complete groups by key, preserve ordering, and produce independent derived results. Mutable lists require defensive copies or immutable storage. Concatenating pairs would incorrectly append defaults.
- **Public consumers:** preserving serialization alone is insufficient. First-value mapping access, `get_list()`, `multi_items()`, functional updates, equality, and hashability remain compatibility obligations. [`URL.params` and URL copy operations](project/httpx/_urls.py#L275) also consume this abstraction.

A centralized repair would substantially recreate QueryParams; distributing it would increase caller maintenance and regression risk. No maintenance reduction is established by this proposal.

Verification: `python -B -m pytest -p no:cacheprovider tests/models/test_queryparams.py` using the specified interpreter produced **14 passed**. These are local observations and source analysis, not a complete replacement implementation or evidence of network behavior. The request was built only. No source or installed-resource changes, scratch files, installs, network access, commits, or publication occurred.
