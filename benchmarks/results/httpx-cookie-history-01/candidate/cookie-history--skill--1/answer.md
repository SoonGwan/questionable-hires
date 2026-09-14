I’ll use the necromancer skill to trace the current cookie handling and ancestor implementations, then compare all five cases with an in-memory removal. I’ll leave project files unchanged and use only local evidence.



The current path extracts response cookies before building the redirect, then supplies the updated jar to the new request. Blame attributes the removal line to a sync API refactor, but that commit’s parent already contains it. I’ll check the parent’s request construction and run the five comparisons.



**Retain the line. Removing only `headers.pop("Cookie", None)` is not behavior-preserving:** cases 1–3 change.

At pinned HEAD `26d48e0634e6ee9cdc0533996db289ce4b430177`, I ran ten actual `Client`/`MockTransport` exchanges using the specified Python with `-B`. Each used a fresh client, `trust_env=False`, `follow_redirects=True`, GET, and a 302 followed by 200. The proposed version removed exactly that statement in memory, preserving the module’s future settings and bindings.

In the table, **S** = `https://example.invalid/start`, **D** = `https://example.invalid/done`, **O** = `https://other.invalid/done`; “absent” means no Cookie header. Each request cell records **URL · Cookie**.

| Case | Current initial | Current redirected | Proposed initial | Proposed redirected |
|---|---|---|---|---|
| 1. Replace sid | S · `sid=old` | D · `sid=new` | S · `sid=old` | D · `sid=old` |
| 2. Delete sid | S · `sid=old` | D · absent | S · `sid=old` | D · `sid=old` |
| 3. Other domain | S · `sid=old` | O · absent | S · `sid=old` | O · `sid=old` |
| 4. Unchanged jar | S · `sid=old` | D · `sid=old` | S · `sid=old` | D · `sid=old` |
| 5. Initially empty jar | S · absent | D · `sid=new` | S · absent | D · `sid=new` |

The mechanism explains the difference:

- [`_send_single_request`](project/httpx/_client.py#L1022) extracts response cookies before redirect construction.
- [`_build_redirect_request`](project/httpx/_client.py#L475) copies the updated client jar and passes it alongside the redirected headers to `Request`.
- [`Request`](project/httpx/_models.py#L403) applies nonempty cookies through [`Cookies.set_cookie_header`](project/httpx/_models.py#L1110). That cookie-jar operation does not overwrite an existing Cookie header; the compatibility wrapper carries the copied headers into it.

Consequently, removing the pop preserves the stale header even when the jar contains `sid=new`, is empty after deletion, or excludes the destination domain. Cases 4–5 remain equivalent: the existing header already matches the applicable jar in case 4, and there is no existing header to obstruct generation in case 5.

The existing [`test_redirect_cookie_behavior`](project/tests/client/test_redirects.py#L403) also expresses the login/logout redirect contract, including cookie expiration. I inspected it; the executed probes used only your synthetic cookies.

Local history establishes earlier operational presence, **not first-ever origin**:

- Blame attributes the line to `ee37a762ef6378ed16681a3452f494a5640d98de`, **“Reintroduce sync API. (#735)”**, January 8, 2020. Its before/after change moves the existing redirect logic from `AsyncClient` into shared `BaseClient`. This attribution does not establish behavioral introduction.
- Its parent, `387f04732baa99ea472c6f78c905a9359b3d0e0e`, already contains the comment and exact pop in `httpx/client.py:500–502`.
- That parent’s operational path extracts cookies at line 693, constructs redirects at line 633, and builds the redirected request at lines 426–438 using:
  ```python
  cookies = Cookies(self.cookies)
  return Request(
      method=method, url=url, headers=headers, cookies=cookies, stream=stream
  )
  ```
  Its `httpx/models.py:604–606` applies those cookies after copying headers, delegating to `jar.add_cookie_header` at line 1053.

Both inspected commits were verified as ancestors of pinned HEAD. No first-introduction intent is claimed.

The smallest next action is to retain the statement. Any future simplification must preserve regeneration from the updated jar for the destination, including replacement, deletion, and domain filtering. These findings concern emitted requests only.

No files or installed resources were changed, no scratch was created, and no network was used. HEAD and working-tree status remain unchanged.
