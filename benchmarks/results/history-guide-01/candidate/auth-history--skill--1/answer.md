I’ll use the necromancer skill to inspect the auth selection logic, compare both versions through MockTransport, and trace the relevant history within pinned HEAD’s ancestors. I’ll leave project files unchanged.



The fallback is active on the request path, and a current test expects URL credentials to produce an Authorization header. Explicit `auth=None` bypasses client auth but still reaches the URL fallback. I’ll verify the five header results and check the commits behind the line attribution.



The probe shows that removal changes cases 1 and 4: both lose the URL-derived Authorization header. Cases 2, 3, and 5 stay the same. The history also confirms that URL fallback existed before the commit blamed for these lines; its parent selected middleware that wrote the Basic header.



## Recommendation: retain

The proposed deletion is **not behavior-preserving**. It removes observable authentication behavior in cases **1 and 4**, and current tests explicitly cover URL-based Basic authentication.

Reviewed at pinned HEAD `26d48e0634e6ee9cdc0533996db289ce4b430177`.

## Observed outgoing headers

I used the repository’s actual `Client`, `MockTransport`, and `trust_env=False`, with only the supplied synthetic credentials. The proposed method was substituted in memory by deleting exactly the assignment and following `if` block, preserving module future settings and bindings.

| Case | Current Authorization | Proposed Authorization |
|---|---|---|
| 1. URL credentials; no client/request auth | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | Absent |
| 2. URL credentials + client auth; request auth omitted | `Basic Y2xpZW50LXVzZXI6Y2xpZW50LXBhc3M=` | Same |
| 3. URL credentials + client auth + request auth | `Basic cmVxdWVzdC11c2VyOnJlcXVlc3QtcGFzcw==` | Same |
| 4. URL credentials + client auth; explicit `auth=None` | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | Absent |
| 5. No URL credentials + client auth; explicit `auth=None` | Absent | Absent |

**Omitted auth** uses `USE_CLIENT_DEFAULT`, selecting client authentication. **Explicit `None`** bypasses client authentication, but currently still permits URL-userinfo fallback. It does not mean “suppress all authentication.”

These are headers captured at the transport boundary; they establish nothing about server-side acceptance.

## Current necessity

In the auth-selection method, explicit/client authentication takes precedence, then URL credentials, then `Auth()`. Both sync and async send paths call this method.

Existing [URL-auth coverage](project/tests/client/test_auth.py#L195) expects a URL-derived Basic header. The [per-request disable test](project/tests/client/test_auth.py#L289) uses a URL **without** credentials, so it does not establish suppression of URL authentication.

The live probe supplies a concrete compatibility break; this is not merely unused-looking code.

## Locally evidenced history

All cited revisions were verified as ancestors of pinned HEAD.

- **`00e150f6` — 2019-11-27, “Client handles redirect + auth”**: blame attributes the username/password assignment and condition here. The patch moves URL fallback from middleware selection into `Client.authenticate`; this attribution does **not** establish behavioral introduction.
- **Its parent, `206c5372`**, already contains actual working plumbing:
  - `httpx/client.py:296–305` selects and invokes auth middleware.
  - `:324–327` selects `BasicAuthMiddleware` from URL username/password.
  - `httpx/middleware/basic_auth.py:13–19` builds and writes the Authorization header before forwarding the request.
  
  This proves earlier presence directly from ancestor code.
- **`6c69e093` — 2019-12-18, “No I/O auth”**: changes immediate authentication into returning an auth object, including the currently blamed `return BasicAuth(...)`. Its parent already applies the same URL fallback.
- **`69409bb8` — 2021-05-11**: replaces `UNSET` with `USE_CLIENT_DEFAULT`; the preceding implementation already distinguished the sentinel from explicit `None`.

The earlier middleware implementation treated request `None` as client-default selection, so its existence should not be mistaken for proof that every modern precedence detail already existed. First-ever origin and original intent remain unclaimed.

**Smallest next action:** reject this deletion as compatibility cleanup and retain the fallback. Removing URL authentication would require a separate policy-change decision.

No files or installed resources were changed, no scratch was created, and the in-memory substitution was restored. Final Git status matched the initial state.
