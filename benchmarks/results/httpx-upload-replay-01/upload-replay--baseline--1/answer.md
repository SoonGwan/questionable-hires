I’ll inspect the multipart and redirect code, then run an offline reproduction with both transports and the two controls. I’ll capture exact body bytes and remove any diagnostic scratch files afterward.

The code points to a buffering difference: `MockTransport` calls `request.read()`, which replaces the multipart stream with a buffered `ByteStream`. The 307 path preserves POST and reuses the request’s current stream. I’ll compare the bytes sent on both hops and check the seekable and explicitly buffered controls.

Reproduced offline using the specified interpreter and this checkout’s HTTPX 0.28.1, actual `Client`, multipart encoder, and redirect handling. Full body bytes, headers, stream types, and response histories are captured above.

Fresh uploads contained identical 13-byte binary content, with boundary `replay-boundary` and one same-origin `/start` → `/end` redirect.

| Path | Methods | Body lengths | Replay equal? |
|---|---|---|---|
| MockTransport, one-pass upload | POST → POST | 165 → 165 | Yes |
| Direct-stream BaseTransport, one-pass upload | POST → POST | 165 → 152 | **No** |
| Direct-stream, seekable upload | POST → POST | 165 → 165 | Yes |
| Direct-stream, explicitly buffered request | POST → POST | 165 → 165 | Yes |

Every path returned **200 with history [307]**. The failing replay retained multipart framing but lost exactly the file’s 13 bytes.

The cause is request buffering:

- `httpx/_transports/mock.py` calls `request.read()` before invoking the handler.
- `httpx/_models.py:468` caches the complete body and replaces `MultipartStream` with replayable `ByteStream`.
- `httpx/_client.py:494` preserves POST for 307; `_redirect_stream` reuses the current stream.
- `FileField.render_data()` in `httpx/_multipart.py` rewinds seekable files. The one-pass upload cannot rewind, so its second read returns EOF.

The direct transport retained `MultipartStream` across both hops. The seekable control successfully rewound; the buffered control used `ByteStream` throughout sending.

All requests retained the fixed multipart Content-Type. The seekable control used `Content-Length: 165`; the other paths used `Transfer-Encoding: chunked` without Content-Length on both hops. Explicit `request.read()` did not recalculate headers.

This establishes a local replayability issue, not method conversion or evidence of a transport/cache malfunction. The default transport passes `request.stream` to httpcore, but no network behavior was tested; server timing and actual wire consumption remain unknown.

For callers, buffer a bounded request **before its first send** using `build_request()`, `request.read()`, then `client.send()`. This costs memory proportional to the complete encoded body and delays sending. For larger uploads, use a stable seekable source or spool to disk, accepting storage/I/O costs. If replay cannot be supported, disable automatic redirects and recreate the source before deliberately resending; an exhausted upload cannot recover its bytes.

No files were modified or artifacts created. Git remained clean.
