I’m using the landlord skill to review the proposal against QueryParams’ behavior and request-building consumers. I’ll run the specified tests and probes locally without changing files.

All 14 QueryParams tests passed. The probes show duplicate loss, changed boolean/None normalization, and list stringification; the space-encoding control matches. Request building replaces the client’s entire `a` group with `7, 8` while leaving client defaults unchanged. Repairing the proposal requires preserving that policy alongside encoding.

**Keep QueryParams.** The proposed replacement cannot preserve current behavior or consumers. QueryParams already delegates encoding to `urlencode(..., doseq=False)`; its value is normalization, repeated-value storage, and immutable operations before encoding. See [constructor and normalization](project/httpx/_urls.py#L425) and [serialization](project/httpx/_urls.py#L623).

Executed results, numbered by your exact inputs:

| Input | `str(httpx.QueryParams(raw_input))` | `multi_items()` | `urlencode(dict(raw_input))` |
|---|---|---|---|
| 1 | `a=1&a=2&keep=x` | `[('a', '1'), ('a', '2'), ('keep', 'x')]` | `a=2&keep=x` |
| 2 | `enabled=true&empty=` | `[('enabled', 'true'), ('empty', '')]` | `enabled=True&empty=None` |
| 3 | `a=1&a=2` | `[('a', '1'), ('a', '2')]` | `a=%5B%271%27%2C+%272%27%5D` |
| 4 | `a=one+two&keep=x` | `[('a', 'one two'), ('keep', 'x')]` | `a=one+two&keep=x` |

Input 1 loses the first duplicate during `dict()` conversion. Input 2 loses HTTPX’s lowercase boolean and empty-`None` conventions. Input 3 encodes the list’s textual representation instead of repeated parameters. Input 4 is the preserved control: scalar strings, key order, and space-to-`+` encoding agree. These contracts appear in [model tests](project/tests/models/test_queryparams.py#L6).

After `derived = base.add('a', '3')`:

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
request.url:
  https://example.invalid/path?a=7&a=8&keep=x
client.params afterward:
  a=1&a=2&keep=x
  [('a', '1'), ('a', '2'), ('keep', 'x')]
```

The actual path is `build_request()` → [`_merge_queryparams()`](project/httpx/_client.py#L433), which copies client parameters and calls `merge(params)`. [`merge()`](project/httpx/_urls.py#L582) normalizes request parameters, then replaces each matching key’s **whole value group**. Thus `7, 8` replaces `1, 2`; it neither appends all four nor keeps only `8`. Unmatched `keep=x` survives.

Client construction copies incoming QueryParams, including their value lists. `add()` copies the outer dictionary and creates a fresh affected list; other lists may be shared internally under the immutable public API. This is deliberate ownership policy, not universal deep copying. `Request` then passes parameters to URL construction for serialization ([request binding](project/httpx/_models.py#L399)).

The nearest viable repair requires more than `doseq=True`:

- **Normalization:** retain a shared adapter for query strings/bytes, blank values, scalar/list inputs, string keys, and HTTPX primitive conversion.
- **Repeated values:** avoid the initial lossy `dict(raw_input)`. Accumulate ordered value groups, then flatten into pairs for default `urlencode`, or encode normalized groups with `doseq=True`. Preserve first-value mapping access and all-value access.
- **Ownership and merging:** retain fresh results, protected value lists, and whole-group replacement. With exposed mutable dictionaries, copying and mutation rules move into client storage, request merging, and URL editing.
- **Public compatibility:** retain the QueryParams interface or migrate its consumers. Client tests explicitly require that type, and URL editing calls its `set/add/remove/merge` methods ([client contracts](project/tests/client/test_queryparams.py#L8), [URL consumers](project/httpx/_urls.py#L342)).

The proposed deletion saves local code but transfers compatibility work into adapters and callers. Centralizing the repaired policies effectively recreates QueryParams; retaining it avoids that migration and maintenance burden.

Validation: the requested interpreter with `-B` and pytest `-p no:cacheprovider` ran **14 tests, all passed**. Probes imported this repository. These are local observations and source analysis, not a complete replacement implementation or evidence of network behavior. No request was sent, no files or installed resources changed, and no scratch files were created.
