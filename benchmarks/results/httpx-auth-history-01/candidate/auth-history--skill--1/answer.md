I’ll use the necromancer skill to compare the live request behavior and trace the relevant ancestor code, without changing project files or authentication policy.

The fallback is on the live send path, and an existing test explicitly expects URL credentials to produce a Basic Authorization header. I’ll now measure the five cases and inspect the commits behind the fallback’s line attribution.

The probe confirms that removal changes cases 1 and 4: both lose the URL-derived Authorization header. Explicit `auth=None` bypasses client auth but currently still reaches the URL fallback. The parent of the 2019 attribution commit already contains a live URL-auth middleware path, so that commit did not introduce the fallback behavior.

**Retain the fallback. Its removal is not behavior-preserving:** cases 1 and 4 lose their Authorization header.

At pinned HEAD `26d48e0634e6ee9cdc0533996db289ce4b430177`, I ran all five cases through the repository’s actual `Client`, with `MockTransport` and `trust_env=False`, using the specified Python with `-B`. For the proposed version, I removed exactly the assignment and following `if` in memory, preserving module future settings and bindings, then restored the method.

These are the outgoing `Authorization` values captured by the transport; “absent” means no header:

| Case | Current | Proposed |
|---|---|---|
| 1. URL credentials; no client/request auth | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | absent |
| 2. URL credentials + client auth; request auth omitted | `Basic Y2xpZW50LXVzZXI6Y2xpZW50LXBhc3M=` | `Basic Y2xpZW50LXVzZXI6Y2xpZW50LXBhc3M=` |
| 3. Same URL/client + request auth tuple | `Basic cmVxdWVzdC11c2VyOnJlcXVlc3QtcGFzcw==` | `Basic cmVxdWVzdC11c2VyOnJlcXVlc3QtcGFzcw==` |
| 4. Same URL/client + explicit `auth=None` | `Basic dXJsLXVzZXI6dXJsLXBhc3M=` | absent |
| 5. URL without credentials + client auth + explicit `auth=None` | absent | absent |

Omitted auth uses `USE_CLIENT_DEFAULT`, selecting the client’s authentication. Explicit `None` instead resolves to no selected auth, bypassing the client setting. **Currently, that still permits URL-userinfo fallback**, explaining case 4. With no URL credentials, it reaches `Auth()`, explaining case 5. These observations establish header emission only, not server-side acceptance.

Current necessity is supported by both execution and existing tests:

- [_build_request_auth](project/httpx/_client.py#L457) is called by synchronous `send` at line 912 and asynchronous `send` at line 1627. Its fallback returns `BasicAuth`, which writes the header.
- [test_basic_auth_in_url](project/tests/client/test_auth.py#L195) explicitly expects a URL-derived Basic header.
- [test_auth_disable_per_request](project/tests/client/test_auth.py#L289) verifies explicit `None` with a credential-free URL; it does not establish that `None` suppresses URL credentials.

Local history distinguishes attribution from introduction. All commits below were verified as ancestors of pinned HEAD:

- **`00e150f6` (2019-11-27), “Client handles redirect + auth”** owns blame for the username/password assignment and condition. Its patch moves URL authentication from middleware into `Client.authenticate`.
- Its actual parent, **`206c5372`**, already contains the fallback in `httpx/client.py:324`:
  ```python
  if request.url.username or request.url.password:
      return BasicAuthMiddleware(
          username=request.url.username, password=request.url.password
      )
  ```
  Lines 296–305 select and execute that middleware; `httpx/middleware/basic_auth.py` constructs and writes the Basic header. This establishes earlier live behavior, not merely an unused text match. That ancestor treated `None` as client-default selection, so it does **not** establish today’s omitted-versus-`None` distinction.
- **`6c69e093` (2019-12-18), “No I/O auth”** changes immediate authentication into returning `BasicAuth(...)`, accounting for that return line’s attribution while retaining the fallback.
- **`cb620e67` (2020-08-17)** splits auth normalization from `_build_request_auth`; **`69409bb8` (2021-05-11)** replaces `UNSET` with `USE_CLIENT_DEFAULT`. Neither introduces URL fallback.

First-ever origin and intent remain unclaimed. The smallest next action is to reject this deletion as compatibility cleanup and retain the behavior. Changing it would require a separate policy decision.

No project files or installed resources were changed; no scratch files were created. HEAD and working-tree status remained unchanged, including the pre-existing untracked `.agents/` directory.
