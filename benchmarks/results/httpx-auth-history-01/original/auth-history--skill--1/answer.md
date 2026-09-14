I’m using the necromancer skill to check the live authentication path, compare the five cases, and trace the relevant ancestor history without changing project files.

The Client comparison shows that the removal changes cases 1 and 4: both lose the URL-derived Authorization header. Explicit `auth=None` bypasses client auth but currently still allows URL auth. Ancestor code also shows the fallback existed before the commit blamed for its current username/password lines.

**Retain. The proposed deletion is not behavior-preserving:** it removes outgoing URL-derived Basic authentication in cases 1 and 4.

I ran all five cases through the repository’s actual `httpx.Client` with `MockTransport` and `trust_env=False`, using the specified Python with `-B`. The proposed method was produced by deleting exactly the requested block in memory; the original method was restored afterward.

| Case | Current Authorization header | Proposed Authorization header |
|---|---|---|
| 1. URL credentials; no client/request auth | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | Absent |
| 2. URL credentials + client auth; request auth omitted | `Basic Y2xpZW50LXVzZXI6Y2xpZW50LXBhc3M=` | Same |
| 3. URL credentials + client auth + request auth | `Basic cmVxdWVzdC11c2VyOnJlcXVlc3QtcGFzcw==` | Same |
| 4. URL credentials + client auth; explicit `auth=None` | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | Absent |
| 5. No URL credentials + client auth; explicit `auth=None` | Absent | Absent |

These are locally captured outgoing headers, not evidence of server-side acceptance.

In [the current selection logic](project/httpx/_client.py#L457), omitted request auth uses `USE_CLIENT_DEFAULT`, selecting client auth. Explicit `None` instead passes through `_build_auth(None)`, bypassing client auth. When that selection produces `None`, URL credentials still supply Basic auth. Thus explicit `None` currently disables **client auth**, but does not suppress this fallback.

This is a live path: both synchronous and asynchronous `send()` call this method. The existing [URL-authentication test](project/tests/client/test_auth.py#L195) explicitly expects the URL-derived header. The [per-request disable test](project/tests/client/test_auth.py#L289) uses a URL without credentials; it does not establish that `None` suppresses URL auth. I inspected these tests; the execution evidence above comes from the five-case comparison.

Local history, restricted to verified ancestors of pinned HEAD `26d48e0634e6ee9cdc0533996db289ce4b430177`, establishes:

- **`00e150f6` (2019-11-27):** blame attributes the username/password assignment and condition here. Its change moves authentication handling from middleware into `Client.authenticate`; this is not evidence of the fallback’s behavioral introduction.
- **Its parent, `206c5372`:** actual `httpx/client.py:296–327` calls `_get_auth_middleware`, which already selects `BasicAuthMiddleware` from URL credentials after explicit/client auth selection. Actual `httpx/middleware/basic_auth.py:18` writes `Authorization`, with Basic encoding at lines 25–27. This proves earlier operational presence.
- **`6c69e093` (2019-12-18):** changes URL authentication from applying `BasicAuth` directly to returning a `BasicAuth` object for the authentication flow. The fallback exists on both sides.
- **`69409bb8` (2021-05-11):** replaces `UNSET`/`UnsetType` with `USE_CLIENT_DEFAULT`/`UseClientDefault`; its parent already distinguishes the sentinel from `None`. The older 2019 caller instead treated `None` as selecting client auth, so that earlier implementation should not be described as having today’s complete semantics.

First-ever origin and original intent remain unclaimed.

The smallest next action is to reject this deletion as compatibility cleanup. Any simplification must preserve the observed selection behavior; removing URL auth requires a separate policy decision. No project files or installed resources were changed, no scratch files were created, and the original untracked `.agents/` state remains.
