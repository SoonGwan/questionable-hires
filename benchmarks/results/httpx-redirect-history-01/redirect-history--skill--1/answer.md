I’ll use the necromancer skill to trace the current redirect path and ancestor history, then test each proposal independently with in-memory substitutions and MockTransport. I’ll keep the review read-only and local.

The current path uses both blocks: one removes body headers, and the other discards the body when the method changes to GET. Blame attributes both to the sync-API refactor, but its parent already contains equivalent behavior. I’ll verify the before/after details alongside the nine requested observations.

**Neither proposal is redundant; reject each independently.** Both change observable redirect behavior at pinned HEAD `26d48e0634e6ee9cdc0533996db289ce4b430177`.

I ran an actual `Client` with `MockTransport`, `follow_redirects=True`, and synthetic URLs `http://redirect.test/start` → `/target`. Each variant started from the original methods; substitutions existed only in memory.

The second requests contained these actual values (`None` means the header was absent):

| Variant | Original POST content | Redirect | Method | Body bytes | Content-Length | Transfer-Encoding |
|---|---|---|---|---|---|---|
| Current | `b"payload"` | 302 | GET | `b''` | `None` | `None` |
| Current | `iter([b"pay", b"load"])` | 302 | GET | `b''` | `None` | `None` |
| Current | `b"payload"` | 307 | POST | `b'payload'` | `'7'` | `None` |
| A-only | `b"payload"` | 302 | GET | `b''` | `'7'` | `None` |
| A-only | `iter([b"pay", b"load"])` | 302 | GET | `b''` | `None` | `'chunked'` |
| A-only | `b"payload"` | 307 | POST | `b'payload'` | `'7'` | `None` |
| B-only | `b"payload"` | 302 | GET | `b'payload'` | `None` | `None` |
| B-only | `iter([b"pay", b"load"])` | 302 | GET | `b'payload'` | `None` | `None` |
| B-only | `b"payload"` | 307 | POST | `b'payload'` | `'7'` | `None` |

The current call path is `Client.post` → `request` → `send` → authentication/redirect handling → `_build_redirect_request`. That builder independently selects the method, headers, and stream, then constructs a `Request`. See [the redirect builder and helpers](project/httpx/_client.py#L475). POST/302 becomes GET; POST/307 retains POST.

- **A: retain the header-removal block.** With body removal still active, deleting this block preserves the original body headers on an empty GET. `Request(stream=None)` creates empty content but does not remove those supplied headers. Thus A changes header compatibility independently of body handling.
- **B: retain the stream early return.** With header removal still active, deleting this return carries the POST payload into the GET. Explicit `Request(stream=...)` does not automatically regenerate content headers, explaining the payload with neither header. This changes body compatibility independently of header handling.

Those constructor rules are visible in [Request](project/httpx/_models.py#L406). Existing [redirect tests](project/tests/client/test_redirects.py#L314) also assert body preservation for 308 and removal of both body and Content-Length for 303.

**The claimed introduction by the sync-API refactor is refuted for both behaviors.** Local blame attributes both guards to `ee37a762ef6378ed16681a3452f494a5640d98de`, “Reintroduce sync API. (#735).” Its before/after change moves the helpers into `BaseClient`:

| Behavior | Parent `387f04732baa99ea472c6f78c905a9359b3d0e0e` | Refactor `ee37a762` |
|---|---|---|
| Drop both body headers on GET change | `AsyncClient.redirect_headers`, `httpx/client.py:482` | `BaseClient.redirect_headers`, line 344 |
| Return `None` on GET change | `AsyncClient.redirect_stream`, `httpx/client.py:506` | `BaseClient.redirect_stream`, line 368 |

The parent’s redirect builder already calls both helpers. Both guards are unchanged across this move: this is line attribution/code movement, not behavioral introduction. Both revisions were verified as ancestors of pinned HEAD. This establishes earlier presence, without asserting first-ever origin or undocumented intent.

These observations concern request objects, **not actual network framing**. MockTransport reads requests before invoking its handler; that read buffers the iterator into a replayable byte stream.

The smallest next action is to decline each removal. No files or installed resources were changed, no scratch was retained, and the original untracked `.agents/` status remained unchanged.
