I’ll inspect the current redirect path and local history, then run the three variants through `Client` and `MockTransport` using in-memory substitutions.

Both blocks are still active in the redirect path. Git blame attributes them to the sync-API refactor, but that commit’s diff also removes the same blocks from the earlier implementation, indicating code movement. The probe hit an annotation issue in the supplied Python; I’ll rerun it with the module’s postponed-annotation setting.

Neither proposal is redundant. **Keep A’s header-removal block and B’s stream early return independently.** Each removal changes current behavior.

Reviewed pinned HEAD `26d48e0634e6ee9cdc0533996db289ce4b430177`. I ran the checkout through the specified Python with `-B`, using `Client(follow_redirects=True, trust_env=False)` and `MockTransport`, redirecting `http://redirect.test/start` to `/target`. Each proposal was applied separately in memory.

Actual second-request observations (`None` means the header was absent):

| Variant | Initial POST content / redirect | Method | Body bytes | Content-Length | Transfer-Encoding |
|---|---|---|---|---|---|
| Current | `b"payload"` / 302 | GET | `b''` | `None` | `None` |
| Current | `iter([b"pay", b"load"])` / 302 | GET | `b''` | `None` | `None` |
| Current | `b"payload"` / 307 | POST | `b'payload'` | `'7'` | `None` |
| A-only | `b"payload"` / 302 | GET | `b''` | `'7'` | `None` |
| A-only | `iter([b"pay", b"load"])` / 302 | GET | `b''` | `None` | `'chunked'` |
| A-only | `b"payload"` / 307 | POST | `b'payload'` | `'7'` | `None` |
| B-only | `b"payload"` / 302 | GET | `b'payload'` | `None` | `None` |
| B-only | `iter([b"pay", b"load"])` / 302 | GET | `b'payload'` | `None` | `None` |
| B-only | `b"payload"` / 307 | POST | `b'payload'` | `'7'` | `None` |

The current call path is `Client._send_handling_redirects` → `BaseClient._build_redirect_request` → `_redirect_method`, `_redirect_headers`, `_redirect_stream` → `Request(...)` (`httpx/_client.py:964`, `:475`). A POST receiving 302 becomes GET; 307 preserves POST.

- **A: retain the block** (`httpx/_client.py:561`). B’s unchanged early return discards the body, but `Request(stream=None)` does not remove copied headers. Its preparation uses `setdefault`, preserving the stale `'7'` or `'chunked'` (`httpx/_models.py:406–462`). Removing A therefore changes header compatibility, including advertising seven bytes alongside an empty body.
- **B: retain the early return** (`httpx/_client.py:579`). A’s unchanged block removes both headers, but passing `request.stream` preserves the payload. Explicit `Request(stream=...)` bypasses automatic content-header generation (`httpx/_models.py:427`). Removing B therefore changes the established bodyless redirected GET into a GET carrying the original payload at the transport interface.

`MockTransport.handle_request` calls `request.read()` before invoking the handler (`httpx/_transports/mock.py:23`). That read buffers iterator content and replaces its stream with a replayable `ByteStream` (`httpx/_models.py:468`). This explains B-only’s iterator result. **These are request-object observations, not evidence of actual network framing or general streaming replay behavior.**

Local history refutes the claimed introduction date for **both** behaviors:

- `git blame HEAD` attributes both conditions to `ee37a762ef6378ed16681a3452f494a5640d98de`, **“Reintroduce sync API. (#735)”**, dated January 8, 2020.
- Inspecting that change shows the same blocks removed from `AsyncClient` and added to the shared `BaseClient`.
- Its parent, `387f04732baa99ea472c6f78c905a9359b3d0e0e`, already contains header stripping in `httpx/client.py:494–498` and the GET-change `return None` in `:512–513`. They are connected to redirect handling through `build_redirect_request` at `:426–438` and its call at `:633`; they were already executable behavior.
- Subsequent changes renamed `client.py` to `_client.py` (`82dc6f32`) and added the methods’ leading underscores (`e107e0f8`).

Thus the sync refactor explains line attribution and movement into shared code, not behavioral introduction. This establishes earlier presence, without claiming first-ever origin or undocumented intent.

All history examined was ancestral to HEAD. No network, installs, or file edits were used; the working tree remains clean.
