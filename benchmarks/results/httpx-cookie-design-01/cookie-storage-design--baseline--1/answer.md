I’ll trace the cookie boundary and its consumers, then check scope behavior with the existing tests and a bounded local probe. I’ll preserve the checkout’s files and keep any diagnostics inside the project.

The boundary serves request header generation, response parsing, client persistence, and redirects. All 15 relevant existing tests passed. I’ll now check same-name cookies through those runtime consumers: the scope tests cover storage operations, but don’t establish which values reach outgoing requests.

**Recommend keep the `Cookies`/`CookieJar` boundary.** A name-only dictionary cannot represent behavior actively supported by this checkout.

- **Requests:** [Request construction](project/httpx/_models.py#L403) delegates header generation to `CookieJar`, preserving domain/path selection.
- **Responses:** [Response.cookies](project/httpx/_models.py#L835) extracts cookies through adapters that preserve repeated `Set-Cookie` headers ([adapter](project/httpx/_models.py#L1270)).
- **Clients:** [cookie merging](project/httpx/_client.py#L413) preserves cookie records. Both [sync](project/httpx/_client.py#L1022) and [async](project/httpx/_client.py#L1737) clients extract response cookies into persistent storage. [Redirects](project/httpx/_client.py#L475) rebuild cookies from that storage after [removing the previous Cookie header](project/httpx/_client.py#L567).
- **Public behavior:** [scoped get/delete/clear](project/httpx/_models.py#L1143), [`CookieJar` inputs](project/httpx/_types.py#L52), and [documented domain/path access](project/docs/quickstart.md#L403) would need incompatible changes.

The maintenance cost is approximately 200 lines for the mapping interface, scoped operations, and two compatibility adapters ([implementation](project/httpx/_models.py#L1079)). Those adapters delegate parsing and cookie policy to the standard library. Replacing storage with a dictionary would either remove supported semantics or require maintaining those mechanisms elsewhere.

Runtime verification used the specified interpreter, Python 3.9.6, with no network:

- **15 existing tests passed:** cookie model, client cookie, and redirect cookie tests, including expiration during logout.
- A [bounded probe](project/.cookie-review/probe.py#L1) passed for scoped request selection, sync/async persistence, scoped copy/deletion, Secure filtering, and single-cookie controls.
- With three cookies named `sid`, actual request headers were:

| Destination | Scoped storage | Name-only projection¹ |
|---|---|---|
| `example.org/` | `sid=root` | `sid=app` |
| `example.org/app/x` | `sid=app; sid=root` | `sid=app` |
| `example.net/` | `sid=other` | `sid=app` |
| `unrelated.test/` | absent | `sid=app` |

¹ Explicit `{cookie.name: cookie.value for cookie in jar}` passed through existing request construction; this demonstrates information loss, not an implemented replacement. Direct `dict(cookies)` instead raised `CookieConflict` for duplicates. The single-cookie normal control converted and sent successfully.

**Nearest viable alternative:** retain the existing dictionary input convenience and normalize it to `Cookies`, as already implemented. Consumers needing one value can use `get(name, domain=..., path=...)`. A replacement store would need at least domain/path/name identity plus cookie metadata and policy; a name-only dictionary is insufficient.

Original files remain unchanged. Only the disposable `.cookie-review/probe.py` was added; no dependencies were installed.
