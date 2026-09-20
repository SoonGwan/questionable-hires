# HTTPX upload replay: author preflight — 2026-09-21

**No model result or skill improvement claim.** A new diagnostic boundary in pinned
HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, selected after source inspection.
It is not a blind holdout or reported production incident. Existing HTTPX preview,
query and audit tasks are not rerun or rescored.

`preflight_httpx_upload_replay.py` uses actual Client, multipart construction and
307 redirect handling, without network. A recording BaseTransport consumes the
request stream directly, while MockTransport reads/buffers it before invoking its
handler. Four fresh uploads carry identical bytes and fixed multipart boundaries.
[Original author observations](httpx-upload-replay-preflight-01.json) retain complete
body bytes, methods, paths, stream types and content/transfer headers.

| Path | First body bytes | Redirected body bytes | Exact replay |
|---|---:|---:|---|
| MockTransport, one-pass upload | 156 | 156 | Yes |
| Stream-consuming transport, one-pass upload | 156 | 138 | No; file payload absent |
| Stream-consuming transport, seekable upload | 156 | 156 | Yes |
| Stream-consuming transport, explicitly buffered request | 156 | 156 | Yes |

All paths finish with status 200 and one 307 in response history. That status is
not proof of body preservation. Methods remain POST. The one-pass failure retains
multipart framing but loses all 18 payload bytes on replay. Seekable Content-Length
matches both complete bodies; one-pass variants use chunked transfer headers.

## Mechanism and limits

In this pinned source, `MockTransport.handle_request` calls `request.read()`.
`Request.read` buffers the content and replaces a streaming body with ByteStream.
`Client._redirect_stream` reuses the stream for a method-preserving redirect.
`FileField.render_data` attempts a rewind but continues on UnsupportedOperation;
the exhausted one-pass file then yields no payload. A test using MockTransport can
therefore hide this stream-replay distinction. Recording the already-buffered
handler content cannot establish what an unbuffered stream would replay.

This is an actual-library/local-transport observation, **not an on-wire transport,
server, connection-pool, asynchronous or current-release claim**. It does not prove
every mock is unsuitable. Explicit buffering trades replayability for memory;
seekable/reopenable sources or a carefully scoped redirect decision are different
possible caller strategies. No upstream fix, test modification, install, network
request or publication outside this repository occurred.

## Validation and reproducibility

Run with the existing HTTPX dependency environment, a clean pinned checkout and
bytecode disabled:

```sh
<httpx-python> -B benchmarks/preflight_httpx_upload_replay.py --source <httpx-checkout>
```

The preflight checks revision, clean checkout and imported HTTPX binding, then all
four outcomes, methods, paths, redirect history and known Content-Length values.
It deliberately asserts false exact replay for the one-pass stream and retains
the expected/observed assertion failure. Source file hashes remain unchanged;
uploads/clients close normally and no scratch is created. This negative check is
not a model failure. Full assertion differences are retained, not truncated.

Two setup attempts failed before observation: an exported project snapshot was
not a Git checkout of the pinned revision; the generic receipt environment lacked
`idna`. Switching to the existing pinned HTTPX workspace/dependency environment
allowed the native controls to run. No dependencies were installed, no model
attempt started, and no success was substituted for a measured model failure.

## Next decision boundary

Use this as a new actual-checkout diagnostic workload only after freezing the
model-visible report and criteria. Ask models to explain apparently safe mocked
redirects versus missing unbuffered upload data, with ordinary and replayable
controls, original preservation and no network. Supply input/behavior obligations,
not this oracle or exact expected mechanism. Compare baseline and current Exorcist
before changing instructions; only an observed weakness justifies a candidate.
Do not force helper usage or turn this one task into a mandatory mock audit for
every bug. The user's representative real project remains preferable if supplied.

한국어: 실제 HTTPX에서 모의 전송의 자동 버퍼링이 재전송 불가능한 업로드를
정상처럼 보이게 하는 차이를 확인했다. 네 가지 경로와 틀린 주장에 대한 실제
assertion 실패를 보존했다. 아직 모델 비교나 스킬 개선 성과가 아니며, 네트워크
실험이나 최신 HTTPX 전체의 동작으로 일반화하지 않는다.
