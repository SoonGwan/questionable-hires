I’ll use the necromancer skill to trace the parser and public caller, capture all 18 observations, and inspect ancestor history without changing repository files.

The attributed change moved and renamed an existing parser; its parent already had both split expressions and an operational `Response.links` caller. The exception paths are significant: A can treat the whole header as a URL, while B can allow parsing to continue past `token=a=b`. I’ll now capture the public results independently.

## Verdict

**Neither proposal preserves behavior at `Response.links`.** A changes inputs 4–6; B changes input 5.

### All 18 observations

Observed using the specified Python with `-B`, loading this repository’s `httpx`. Each variant started from the original parser; substitutions were in memory, preserving its future settings and bindings. The caller and surrounding logic stayed unchanged. **No observation raised an error.**

| # | Link header | Current | A-only | B-only |
|---|---|---|---|---|
| 1 | No Link header | `{}` | `{}` | `{}` |
| 2 | `</next>` | `{'/next': {'url': '/next'}}` | `{'/next': {'url': '/next'}}` | `{'/next': {'url': '/next'}}` |
| 3 | `</next>; rel=next` | `{'next': {'url': '/next', 'rel': 'next'}}` | `{'next': {'url': '/next', 'rel': 'next'}}` | `{'next': {'url': '/next', 'rel': 'next'}}` |
| 4 | `</next>; rel=next; type=text/plain` | `{'next': {'url': '/next', 'rel': 'next', 'type': 'text/plain'}}` | `{'/next>; rel=next; type=text/plain': {'url': '/next>; rel=next; type=text/plain'}}` | `{'next': {'url': '/next', 'rel': 'next', 'type': 'text/plain'}}` |
| 5 | `</next>; token=a=b; rel=next` | `{'/next': {'url': '/next'}}` | `{'/next>; token=a=b; rel=next': {'url': '/next>; token=a=b; rel=next'}}` | `{'next': {'url': '/next', 'token': 'a=b', 'rel': 'next'}}` |
| 6 | `</next>; preload; rel=next` | `{'/next': {'url': '/next'}}` | `{'/next>; preload; rel=next': {'url': '/next>; preload; rel=next'}}` | `{'/next': {'url': '/next'}}` |

### Why these results occur

The public [`Response.links` property](project/httpx/_models.py#L842) returns `{}` immediately for a missing header. Otherwise, it maps each parser dictionary under `link.get("rel") or link.get("url")`.

In the [parser](project/httpx/_models.py#L93):

- **A:** Removing the semicolon split limit makes inputs 4–6 produce three pieces. Two-variable unpacking raises `ValueError`, which the existing handler catches by assigning the **entire header** to `url` and empty text to `params`. Stripping removes the leading `<`, but leaves the internal `>`. No `rel` is parsed, so that entire stripped string becomes both the mapping key and its `url` value.
- **B:** Current `param.split("=")` produces three pieces for `token=a=b`; unpacking fails and `break` skips that parameter and the later `rel`. With `split("=", 1)`, it produces `token` and `a=b`, then continues to `rel=next`. Both the inner dictionary and outer key change.
- **Unchanged controls:** Input 2 takes the no-semicolon fallback in all variants. Input 3 has exactly one semicolon and one equals sign in its parameter. B leaves input 4 unchanged because each parameter has exactly one equals sign. Input 6 still stops at `preload` under current and B: even the limited equals split cannot produce two pieces without an equals sign.

### Locally evidenced history

Pinned HEAD: `26d48e0634e6ee9cdc0533996db289ce4b430177`.

Blame attributes both split lines to **`41597adffa9d34171a63f7511fc0f702558dd08c`**, “Move remaining utility functions from _utils.py to _models.py (#3387).” I verified it is an ancestor of HEAD and inspected its actual parent-to-commit diff.

That diff **moves and renames** `parse_header_links` to `_parse_header_links`, preserving both split expressions and their exception handling. It updates the caller’s function name and moves existing public-property tests.

The earlier operational implementation is present in its parent, **`6212e8fa3bf90154b891c7721f6d29737caac861`**:

- `httpx/_utils.py:43–77` contains `parse_header_links`, including:
  ```python
  url, params = val.split(";", 1)
  ```
  and:
  ```python
  key, value = param.split("=")
  ```
  with the same fallback, `break`, and stripping.
- `httpx/_models.py:51` imports that function; lines 777–789 contain the operational property:
  ```python
  header = self.headers.get("link")
  if header is None:
      return {}

  return {
      (link.get("rel") or link.get("url")): link
      for link in parse_header_links(header)
  }
  ```

Thus, the attributed commit did **not introduce these behaviors**. This establishes prior operational use, without claiming first-ever origin or author intent.

### Separate recommendations

| Proposal | Recommendation | Behavior to preserve |
|---|---|---|
| A | **Retain** `val.split(";", 1)`; reject the proposed simplification/removal of its limit. | Separate the URL at the first semicolon and retain remaining parameters for parsing. |
| B | **Retain** `param.split("=")` under this compatibility requirement; reject the proposed simplification. | Stop parameter processing when unpacking encounters multiple equals signs, leaving later `rel` unprocessed. |

B might be useful as an intentional behavior change, but it is not an equivalent cleanup.

The six existing Link tests passed with `-p no:cacheprovider`. Repository files and installed resources were preserved; no scratch files were created. **Smallest next action: leave both expressions unchanged.**
