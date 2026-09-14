I’m using the necromancer skill to trace the current behavior and local history, then compare the proposed removal with synthetic credentials through `Client` and `MockTransport`. I’ll preserve the project files and use only local evidence.

The current tests explicitly cover Basic authentication from URL credentials. The fallback is also reached when request `auth=None` overrides client authentication. Local history shows the URL behavior existed before the refactor blamed for these lines; I’m checking the exact headers for all five cases now.

## Recommendation: retain

The proposed deletion is **not behavior-preserving**. It removes outgoing URL-derived authentication in cases **1 and 4**. This is active, tested behavior, so removal would require a separate compatibility/policy decision.

Reviewed pinned HEAD: `26d48e0634e6ee9cdc0533996db289ce4b430177`.

### Observed outgoing headers

I ran all five cases through the repository’s actual `httpx.Client`, with `MockTransport` and `trust_env=False`, using the specified Python with `-B`. The proposed method was substituted only in memory, preserving the module’s future annotations and bindings.

“Absent” means the transport received no `Authorization` header.

| Case | Current | Proposed |
|---|---|---|
| 1. URL credentials; no client/request auth | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | Absent |
| 2. URL credentials + client auth; request auth omitted | `Basic Y2xpZW50LXVzZXI6Y2xpZW50LXBhc3M=` | Same |
| 3. URL credentials + client auth + request auth | `Basic cmVxdWVzdC11c2VyOnJlcXVlc3QtcGFzcw==` | Same |
| 4. URL credentials + client auth; request `auth=None` | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | Absent |
| 5. No URL credentials + client auth; request `auth=None` | Absent | Absent |

These observations establish header emission only; they say nothing about server-side acceptance.

### Current necessity

In [BaseClient._build_request_auth](project/httpx/_client.py#L457):

- **Omitted auth** uses `USE_CLIENT_DEFAULT`, selecting client authentication.
- **Explicit `None`** bypasses client authentication and resolves to `None`. The current method then checks URL credentials.
- Thus, `auth=None` does **not** universally suppress URL-derived authentication. With no URL credentials, it reaches the final `Auth()`.

Both [Client.send](project/httpx/_client.py#L912) and [AsyncClient.send](project/httpx/_client.py#L1627) call this method. [BasicAuth](project/httpx/_auth.py#L126) writes the header.

The existing [test_basic_auth_in_url](project/tests/client/test_auth.py#L195) asserts URL-derived Basic authentication. [test_auth_disable_per_request](project/tests/client/test_auth.py#L288) covers explicit `None` with a credential-free URL; it does not establish that `None` suppresses URL credentials. These tests were inspected; the five-case comparison above was executed.

### Locally evidenced history

All inspected revisions were verified as ancestors of pinned HEAD.

| Revision | Evidence and interpretation |
|---|---|
| `206c5372` — parent of `00e150f6` | Actual `httpx/client.py:307–327` already selects `BasicAuthMiddleware` from URL username/password after explicit auth handling. Its caller installs that middleware, and `httpx/middleware/basic_auth.py` writes `Authorization`. This establishes earlier live behavior. |
| `00e150f6` — 2019-11-27, “Client handles redirect + auth” | Blame attributes the current username/password assignment and condition here. The patch moves URL authentication from middleware selection into `authenticate()`. **That attribution is not its behavioral introduction.** |
| `6c69e093` — 2019-12-18, “No I/O auth” | Changes direct authentication into returning `BasicAuth` from `setup_auth()`, retaining the URL fallback. |
| `cb620e67` — 2020-08-17, “Add Client.auth setter” | Separates auth normalization from request selection and introduces the `_build_request_auth` name while preserving the fallback. |
| `69409bb8` — 2021-05-11 | Replaces `UNSET` with `USE_CLIENT_DEFAULT`; the preceding implementation already distinguished omission using a sentinel. |

The earlier 2019 implementation used `None` to inherit client auth, so its presence does **not** establish today’s explicit-`None` semantics. First-ever origin and original intent remain unclaimed.

**Smallest next action:** reject this removal-only proposal and retain the fallback. No project files or installed resources were changed, no scratch files were created, and the in-memory method was restored.
