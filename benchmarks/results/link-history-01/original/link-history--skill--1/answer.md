I’m using the necromancer skill to compare the two changes independently through `Response.links`, then trace the relevant ancestor code. I’ll preserve the files and run the probes in memory.



Neither proposal preserves all six observations. A changes inputs 4–6 by treating the whole link as the URL; B changes input 5 by accepting `a=b` and reaching `rel=next`. The attributed commit moved and renamed the parser: its parent already contains both split operations and a live `Response.links` caller.



## Verdict

**Neither A nor B is behavior-preserving at `Response.links`.** Retain both current split expressions for compatibility.

### All 18 observations

These are actual `httpx.Response(200, headers=...).links` results from the local repository. Each proposal was applied independently in memory. **No observation raised an error.**

| Link header | Current | A-only | B-only |
|---|---|---|---|
| 1. No Link header | `{}` | `{}` | `{}` |
| 2. `</next>` | `{'/next': {'url': '/next'}}` | `{'/next': {'url': '/next'}}` | `{'/next': {'url': '/next'}}` |
| 3. `</next>; rel=next` | `{'next': {'url': '/next', 'rel': 'next'}}` | `{'next': {'url': '/next', 'rel': 'next'}}` | `{'next': {'url': '/next', 'rel': 'next'}}` |
| 4. `</next>; rel=next; type=text/plain` | `{'next': {'url': '/next', 'rel': 'next', 'type': 'text/plain'}}` | `{'/next>; rel=next; type=text/plain': {'url': '/next>; rel=next; type=text/plain'}}` | `{'next': {'url': '/next', 'rel': 'next', 'type': 'text/plain'}}` |
| 5. `</next>; token=a=b; rel=next` | `{'/next': {'url': '/next'}}` | `{'/next>; token=a=b; rel=next': {'url': '/next>; token=a=b; rel=next'}}` | `{'next': {'url': '/next', 'token': 'a=b', 'rel': 'next'}}` |
| 6. `</next>; preload; rel=next` | `{'/next': {'url': '/next'}}` | `{'/next>; preload; rel=next': {'url': '/next>; preload; rel=next'}}` | `{'/next': {'url': '/next'}}` |

### Why these results occur

The public [Response.links property](project/httpx/_models.py#L842) returns `{}` immediately when the header is absent. Otherwise, it keys each parser dictionary by `link.get("rel") or link.get("url")`, retaining the complete dictionary as its value.

In the [parser](project/httpx/_models.py#L93):

- **A, inputs 4–6:** Unrestricted semicolon splitting produces three pieces. Unpacking raises `ValueError`, which the existing handler catches, assigning the entire `val` to `url` and empty text to `params`. URL stripping removes the leading `<`, but the embedded `>` remains. With no parsed `rel`, this whole string becomes the public mapping key.
- **B, input 5:** Current unrestricted equals splitting produces three pieces for `token=a=b`; the caught `ValueError` breaks parameter processing before `rel=next`. B produces two pieces, stores `token: 'a=b'`, and continues to `rel=next`, changing both the mapping key and value.
- **Unchanged controls:** Input 2 uses the semicolon fallback and returns only the stripped URL. Input 3 has exactly one semicolon and one equals sign. B also preserves input 4 because both parameters contain one equals sign. Input 6 still breaks at `preload` under B because there is no equals sign. Input 1 bypasses parsing entirely.

### Locally evidenced history

Pinned HEAD: `26d48e0634e6ee9cdc0533996db289ce4b430177`.

Blame attributes both split lines to **`41597adffa9d34171a63f7511fc0f702558dd08c`**, “Move remaining utility functions from _utils.py to _models.py (#3387).” I verified that commit is an ancestor of HEAD and inspected its before/after diff.

Its parent, **`6212e8fa3bf90154b891c7721f6d29737caac861`**, provides an earlier operational implementation:

- `httpx/_utils.py:43–77`, `parse_header_links`, already contains:
  ```python
  url, params = val.split(";", 1)
  ```
  and:
  ```python
  key, value = param.split("=")
  ```
  with the same fallback, break, stripping, and append logic.
- `httpx/_models.py:47–52` imports that parser.
- `httpx/_models.py:777–789`, `Response.links`, calls it:
  ```python
  return {
      (link.get("rel") or link.get("url")): link
      for link in parse_header_links(header)
  }
  ```

Thus, the attributed change **moved and renamed existing operational code**, updating the caller to `_parse_header_links`. It did not introduce these split behaviors. This evidence does not establish first-ever origin or author intent.

### Separate recommendations

| Proposal | Retain / simplify / remove | Behavior to preserve |
|---|---|---|
| **A** | **Retain** `val.split(";", 1)`. Reject the proposed simplification; do not remove the split limit. | Multiple parameters must remain parameters, with the URL isolated and `rel` available when parsing reaches it. |
| **B** | **Retain** `param.split("=")`. Reject B as an equivalent cleanup; do not remove its current rejection behavior. | A parameter containing multiple equals signs stops parameter processing, including later `rel` parameters. |

Smallest next action: decline both compatibility-cleanup proposals. B may be useful as a separately authorized behavior change, but it fails the requested compatibility criterion.

**Validation:** All 18 probes completed; the six existing focused header-link tests passed. Used the specified Python with `-B` and pytest with `-p no:cacheprovider`. No files or installed resources were modified, no scratch was created, and no network access was used.
