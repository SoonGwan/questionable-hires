I’m using the exorcist skill to compare the three paths in one offline probe, recording response state and underlying stream closure to test the pooled-connection hypothesis.

The code distinguishes consuming the stream from caching the body: `read()` stores the bytes for reuse, while `iter_bytes()` alone does not. I’ll test whether all three paths close their underlying streams despite differing on later reads. The probe uses a recording `SyncByteStream` through `MockTransport`, so it needs no network or connection pool.

Reproduced offline with repository HTTPX 0.28.1, actual `Client`/`MockTransport`, and a recording `SyncByteStream`, using the specified interpreter. All three received `b'preview-body: hello world'` in two chunks.

State below is `(consumed, closed, underlying close calls)`:

| Path | Before preview | Preview bytes | After preview | Later `read()` |
|---|---|---|---|---|
| `stream()` + `iter_bytes()` | `(False, False, 0)` | Full body | `(True, True, 1)` | `StreamConsumed` |
| `stream()` + `read()` | `(False, False, 0)` | Full body | `(True, True, 1)` | Full body |
| `get()` + `iter_bytes()` | `(True, True, 1)` | Full body | `(True, True, 1)` | Full body |

Later reads and context exits left those states unchanged. Every underlying stream recorded two yields, exhaustion, then exactly one `close()`.

The distinguishing boundary is **whether HTTPX cached the response body**:

- [`read()`](project/httpx/_models.py#L876) consumes and stores `_content`; subsequent reads reuse it.
- [`iter_bytes()`](project/httpx/_models.py#L884) reuses cached content when available, but consuming an uncached stream does not populate that cache.
- Ordinary [`Client.send()`](project/httpx/_client.py#L920) calls `response.read()` before returning when streaming is disabled, explaining the `get()` result.

The consumption guard correctly rejects a second raw-stream read. Context-manager cleanup releases resources; it does not make consumed bytes replayable.

Premature pooled-connection closure is unnecessary for this reproduction: there was no pool, and closure occurred after exhaustion in every path. This does not establish what happened to any production connection.

Safe next action: change the logging design to use `response.read()` when full buffering is acceptable, then log a bounded slice. Buffering retains the entire decoded body in memory—even if the logged preview is short—and joining chunks can temporarily require additional memory. For large or unbounded bodies, capture a bounded preview during the application’s single streaming pass.

All assertions passed. No network, installs, existing-file changes, or diagnostic artifacts were created.
