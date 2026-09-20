I’m using the exorcist skill to test where replay behavior diverges. I’ll run one offline probe through the real client and multipart redirect path, capture both bodies for each control, then remove the scratch files and verify Git state is unchanged.


The code shows a likely distinction: `MockTransport` calls `request.read()`, which replaces the multipart stream with buffered bytes. A 307 preserves both POST and the current stream. I’ll test whether direct consumption leaves the multipart encoder replaying an exhausted file, with seekable and pre-buffered uploads as controls.


Reproduced offline using the specified interpreter and this checkout’s actual `Client`, multipart encoder, and redirect handling. Captured output contains complete body byte representations, methods, stream types, headers, and response histories.

All paths sent **POST → POST** through one same-origin `/start` → `/end` redirect and returned **200 with history [307]**:

| Upload / transport | Body lengths | Replay equal? |
|---|---:|---|
| One-pass / MockTransport | 171 → 171 | Yes |
| One-pass / direct-stream transport | 171 → 152 | **No** |
| Seekable / direct-stream transport | 171 → 171 | Yes |
| Explicitly buffered one-pass / direct-stream transport | 171 → 171 | Yes |

Initial bodies were byte-identical. The failing replay lost exactly the **19-byte file payload**, retaining multipart headers and boundaries.

The implementation explains the discrepancy:

- `httpx/_transports/mock.py`: `MockTransport` calls `request.read()` before its handler.
- `httpx/_models.py:468`: that call buffers the complete body and replaces `MultipartStream` with replayable `ByteStream`.
- `httpx/_client.py:494,573`: 307 preserves POST and reuses the current stream.
- `httpx/_multipart.py:203`: file rendering attempts `seek(0)`, tolerates `UnsupportedOperation`, then reads. On replay, the one-pass upload is already exhausted. The seekable control rewinds successfully.

`MultipartStream` can be iterated again without ensuring its files can replay; the generator-consumption guard in `IteratorByteStream` does not protect this path.

One-pass cases retained `Transfer-Encoding: chunked`, including after buffering; the seekable case used `Content-Length: 171`. All retained the fixed multipart content type.

For bounded uploads, build the request, call **`request.read()` before the first send**, then send with redirects enabled. This costs memory proportional to the encoded body and delays sending until buffering finishes. For larger uploads, spool to a seekable file and keep it open and unchanged through redirects. If replay storage is unacceptable, disable automatic redirects and handle them explicitly using a fresh source.

This establishes local stream exhaustion and MockTransport’s buffering effect. No cache or method conversion is needed to reproduce it. Actual network framing, server behavior, and the reporter’s production transport remain untested.

Repository file hashes and Git status were unchanged. No scratch files, installs, network calls, or library edits were made.
