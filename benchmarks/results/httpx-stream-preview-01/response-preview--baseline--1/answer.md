I’ll inspect the local HTTPX code and run all three paths with `Client` and `MockTransport`, tracking stream state and close calls. I’ll preserve the existing files and remove any temporary probes.

Reproduced all three paths offline using repository HTTPX 0.28.1, the specified interpreter, real `Client`/`MockTransport`, and a tracking `SyncByteStream`. Each response supplied the same body in two chunks: `b'alpha-beta-gamma'`.

State below is **(consumed, closed, underlying close calls)**:

| Path | Before preview | Preview bytes | After preview | Later `read()` |
|---|---|---|---|---|
| `client.stream()` → `iter_bytes()` | `(False, False, 0)` | `b'alpha-beta-gamma'` | `(True, True, 1)` | `StreamConsumed` |
| `client.stream()` → `read()` | `(False, False, 0)` | `b'alpha-beta-gamma'` | `(True, True, 1)` | `b'alpha-beta-gamma'` |
| `client.get()` → `iter_bytes()` | `(True, True, 1)` | `b'alpha-beta-gamma'` | `(True, True, 1)` | `b'alpha-beta-gamma'` |

Later reads and context exits left those states unchanged. Each underlying stream was iterated exactly once and closed exactly once.

**The distinguishing boundary is whether HTTPX has cached the response body.** In `httpx/_models.py:876`, `read()` joins `iter_bytes()` and stores the result as `_content`. Exhausting `iter_bytes()` directly consumes and closes the stream without populating that cache—even if the logger joins the bytes into its own variable. A subsequent `read()` attempts another stream iteration and raises `StreamConsumed`.

Ordinary `client.get()` calls `response.read()` before returning (`httpx/_client.py:921`), so its preview and later read both use cached bytes.

This reproduces the failure without any connection pool. Closure occurs normally after body exhaustion; these results do not support premature pooled-connection closure as the cause.

The safe next action is to adjust the logging approach: for bodies small enough to buffer, use `response.read()` and log a slice of the returned bytes. This retains the entire decoded body in memory, with possible temporary allocation overhead; slicing the preview does not limit buffering. For large or unbounded responses, capture a bounded preview during the application’s single streaming pass, or log metadata only.

No existing files changed, no dependencies installed, and no network used. The probe ran through stdin with bytecode writing disabled, leaving no diagnostic artifacts; Git remained clean.
