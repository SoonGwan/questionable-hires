# HTTPX upload replay comparison — frozen before execution

2026-09-21. One new author-selected diagnosis in actual HTTPX checkout
`26d48e0634e6ee9cdc0533996db289ce4b430177`. Current Exorcist resource `9c03f56`
versus no skill, one fresh session each. There is no instruction candidate yet:
an observed weakness must precede any proposed change. This is a prompted,
author-designed task after source inspection, not an independent holdout.

## Frozen request and execution

The `upload-replay-diagnosis` profile in `run_httpx.py` owns the exact model request.
It describes one-pass multipart uploads apparently replaying through MockTransport
but losing content through a stream-consuming transport. It explicitly asks for
four paths, fresh nonempty uploads, fixed boundaries, full byte evidence, methods,
headers, stream types, response status/history, source mechanism, caller tradeoffs
and unchanged originals. It does not include the author preflight, correct answer,
expected byte counts or a skill-specific helper requirement.

Run `run_httpx.py --profile upload-replay-diagnosis --arms baseline skill
--repeats 1 --skill-revision 9c03f56 --persist-session`, with the clean pinned
checkout, recorded interpreter and a new output directory. Existing seeded schedule
is **skill then baseline**, serial, GPT-6 Astra medium, 360 seconds each. Do not
change defaults for historical profiles. Keep all attempts; no retries, input
changes, replacement cells or favorable-outcome selection. Stop on account limits
and retain unattempted cells. No external project writes or production changes.

Use the dedicated Python 3.11 environment and exact installed versions in
`httpx-upload-replay-requirements-01.txt` for both conditions. Models may not install
dependencies. Runner records effective interpreter, dependency freeze, skill files,
revision and each cell's actual usage/evidence. All scratch must remain local to
the model project and be removed; final captured output is sufficient.

## Five review criteria

1. Execute actual Client/multipart/307 redirect paths offline using MockTransport
   and a stream-consuming BaseTransport without premature `request.read`; fresh
   identical input plus seekable and explicitly buffered controls. No fake client
   implementation or status-only proof.
2. Retain full/lossless first and replay body evidence, lengths, methods, headers,
   stream types and response history/status for all four paths. Correctly identify
   payload loss versus exact replay, preserving framing and method distinctions.
3. Trace the observed difference to actual MockTransport buffering, Request.read's
   stream replacement, method-preserving redirect stream reuse and multipart
   rewind/exhaustion. Distinguish evidence from speculative cache/network causes.
4. Recommend a scoped caller strategy with replayability/memory tradeoffs; separate
   local transport observations from real network behavior and avoid an unrequested
   library fix or blanket claim that all mocks are invalid.
5. Preserve original files, Git HEAD/index and installed resources, no leftover
   scratch, dependencies, external services, commits or publication. Required
   evidence comes from original execution, not a later author replacement.

## Preflight and limitations

[Author controls](HTTPX-UPLOAD-REPLAY-01.md) and retained JSON establish all four
native paths and an actual false-equality assertion failure. Relevant upstream
tests `test_multipart_encode_non_seekable_filelike` and `test_multipart_rewinds_files`
both pass in 0.03 seconds in the new environment. Runner profile/schedule tests:
22 pass. These checks are not model successes or an efficiency result.

The two former temporary HTTPX environments no longer provided pytest. Both native
test launch attempts failed before collection; no model was launched. A new
repository-local environment was created, with the eight direct package versions
selected from earlier environment records and resolved transitive versions frozen
separately. The four-path preflight was rerun successfully there. This is not the
same complete environment as historical runs; never compare wall times as if it were.
No existing environment or upstream source was modified.

Inspect every original command/output and full criterion evidence before scoring.
Reconcile token counters with retained sessions; input includes cache once. Review
exact initial skill exposure privately and export no private initial messages.
Report total tokens, wall time, response count, success/scope, extra work and any
capture gaps. n=1, shared host/cache and unblinded review do not establish a broad
20–30% gain. Even a faster correct pair needs separate generalization evidence.
No featured graph update follows automatically from this diagnostic comparison.

한국어: 실제 HTTPX 업로드 재전송 진단을 현재 스킬·무스킬 각 1회 비교한다.
요구사항과 다섯 판정 기준을 미리 고정하고, 바뀐 환경을 과거 측정과 혼동하지
않는다. 필요한 실제 검증을 생략한 절감은 성과로 보지 않으며, 실패·추가 작업도
그대로 남긴다. 아직 새 모델 결과나 스킬 수정은 없다.
