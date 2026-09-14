I’ll use the necromancer skill to trace the current redirect behavior and ancestor implementations, then run the five comparisons without changing project files.

The current code rebuilds redirect cookies from the updated client jar. Keeping the original `Cookie` header appears to prevent that rebuild from taking effect; the five request probes will verify the consequences. The blamed commit also moved substantial redirect code, so I’m checking its ancestors before attributing the behavior to it.

**Retain the line. Removing only `headers.pop("Cookie", None)` is not behavior-preserving:** cases 1–3 change.

Pinned HEAD: `26d48e0634e6ee9cdc0533996db289ce4b430177`.

I ran all ten comparisons using the specified Python with `-B`, the repository’s actual `Client` and `MockTransport`, and a fresh client for each run with `trust_env=False` and `follow_redirects=True`. Each `/start` returned 302 and its destination returned 200. The proposed version removed exactly that statement in memory, preserving the module’s future settings.

In the table, `S` = `https://example.invalid/start`, `D` = `https://example.invalid/done`, `O` = `https://other.invalid/done`; `—` means no Cookie header. Each entry records **URL [Cookie] → URL [Cookie]**.

| Case | Current | Proposed removal |
|---|---|---|
| 1. Replace cookie: `sid=new; Path=/;` | S [`sid=old`] → D [`sid=new`] | S [`sid=old`] → D [`sid=old`] |
| 2. Delete cookie: `sid=gone; Path=/; Max-Age=0;` | S [`sid=old`] → D [—] | S [`sid=old`] → D [`sid=old`] |
| 3. Other host, no Set-Cookie | S [`sid=old`] → O [—] | S [`sid=old`] → O [`sid=old`] |
| 4. Same host, no Set-Cookie | S [`sid=old`] → D [`sid=old`] | S [`sid=old`] → D [`sid=old`] |
| 5. Empty initial jar, set `sid=new; Path=/` | S [—] → D [`sid=new`] | S [—] → D [`sid=new`] |

Cases 1–4 used exactly `sid=old`, domain `example.invalid`, path `/`. All recorded requests were GETs.

The mechanism explains these results:

- Response cookies enter the client jar before redirect construction at [httpx/_client.py:1022](project/httpx/_client.py#L1022).
- [_build_redirect_request](project/httpx/_client.py#L475) copies the updated jar and passes it alongside the redirect headers to `Request`.
- [Request](project/httpx/_models.py#L402) applies a nonempty jar through `Cookies.set_cookie_header`. The locally inspected `CookieJar.add_cookie_header` adds Cookie only when no Cookie header already exists; it does not replace or remove an inherited header.

Thus removal preserves a stale header after replacement, retains it after deletion even though the jar is empty, and forwards it to `other.invalid` despite jar domain filtering. Case 4 happens to retain the correct value. Case 5 remains equivalent because there is no initial header blocking generation.

The existing [test_redirect_cookie_behavior](project/tests/client/test_redirects.py#L403) also expresses the cookie-expiration-on-redirect contract. I inspected it; the executed comparisons used only the requested synthetic cookies.

Local history establishes earlier operational presence:

- Blame attributes today’s line to `ee37a762ef6378ed16681a3452f494a5640d98de` (2020-01-08, “Reintroduce sync API”). Its diff removes and re-adds the cookie-stripping block while reorganizing `AsyncClient` into shared `BaseClient` logic. Its parent already contains both stripping and jar-based redirect construction. **This attribution is code movement, not behavioral introduction.**
- `00e150f6a5f8d295faeadc34cfe53de254b3f264` (2019-11-27, “Client handles redirect + auth”) moves the logic from redirect middleware into the client.
- Actual ancestor `206c5372a60cb2511cf5ac39c963ff76953c569f`, that commit’s parent, already has `headers.pop("Cookie", None)` in `httpx/middleware/redirect.py:118`. Its redirect builder at line 46 constructs:
  ```python
  cookies = Cookies(self.cookies)
  return Request(
      method=method, url=url, headers=headers, data=content, cookies=cookies
  )
  ```
  This was wired into operation: `httpx/client.py:293` supplies `self.cookies` to `RedirectMiddleware`, and line 271 extracts response cookies before returning to it. The ancestor’s `Request` also applies cookies through `set_cookie_header`.

All inspected revisions are ancestors of pinned HEAD. These findings establish earlier presence, not first-ever origin or undocumented intent.

The smallest next action is to reject this removal-only cleanup. Preserve regeneration from the updated jar for the destination URL, including replacement, expiration, and domain filtering. Project files and installed resources were unchanged; no scratch files, network access, installs, or commits were used.
