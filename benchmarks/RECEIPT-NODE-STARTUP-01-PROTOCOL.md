# Receipt Node startup 01 — frozen before model execution

2026-09-21. Two related authored synthetic tasks, three conditions, one session
each: six serial GPT-6 Astra medium sessions, 360 seconds each. No-skill baseline,
prior Receipt `fcd523c`, guide candidate `107a0cf`. Only the Node reference guide
differs between the two skill resources; executables and entrypoint are identical.
This is not an independent holdout or a broad skill-performance estimate.

## Tasks and native controls

The [preflight](RECEIPT-NODE-STARTUP-PREFLIGHT-01.md) and
`receipt_node_startup_cases.py` define the complete cases. Both compare HEAD^/HEAD
with identical current tests for explicit zero, positive integer, omitted and null
retry settings. Before: three passes, one actual `3` versus `0` assertion failure.
After: all four pass. Test-bound copy-local origin/PID, full revisions, unchanged
original bytes/modes/HEAD/index/resources and scratch removal are explicit tasks.
The plain case supports the helper; the preloaded case requires the unchanged
native `NODE_OPTIONS='--import ./bootstrap.mjs'` startup. Dropping that setting
causes setup TypeErrors, not defect evidence. Helper adoption is never required.

## Fixed preparation and execution

Order: plain baseline → original → current; preloaded current → original → baseline.
Run `python3 -B benchmarks/run_receipt_node_startup_01.py` once to prepare native
controls, full cases, resource copies with exact modes/bytes, resource digests and
input hashes. Commit the runner/factory/protocol before `--execute`. Inspect the
prepared manifest before launch. An exclusive execution marker prohibits reruns;
observe live handles instead of restarting on an observation timeout. Preserve
every scheduled cell, including incomplete, failed and unattempted cells. Account
limits stop remaining calls. Do not adjust inputs or criteria after observing
results. The six-cell execution is sequential, not delegated agent work.

## Review and decision

Review all five case criteria from original commands, outputs and final artifacts:
equal native tests/startup, actual defect assertion, after results/mechanism,
revisions/test-bound identity, and preservation/cleanup. Missing setup, skipped
tests or incomplete work cannot earn efficiency credit. Diagnostic origin is not
tamper-proof attestation; load evidence alone is not dispatch or coverage.

Retain original session records privately, reconcile tool-output capture gaps, and
check recorded instruction exposure without exporting private initial messages.
Report input tokens (including cached input once) plus output, process wall time,
response/command counts and extra guide/code reads for every cell. Author replays
must be labeled separately and never replace original model evidence. Compare
current to both prior and baseline; report adverse results and per-case outcomes,
not just a favorable aggregate. With n=1, shared host/cache and unblinded review,
results are descriptive and cannot establish stable or causal percentage gains.

Accept shorter guidance as a measured candidate only if obligations remain met;
claim a cost win only for equal completed work and the actual measured metric.
Do not promote this pair into featured charts or rewrite historical measurements.
Further validation is needed before any broad release-performance claim.

한국어: 두 합성 과제를 무스킬·기존 안내·수정 안내로 총 6회 비교한다. 테스트나
필수 시작 설정을 생략한 실행은 비용이 작아도 개선이 아니다. 모든 원본 결과와
불리한 수치를 보존하며, 한 번씩의 실행을 전체 성능 향상으로 일반화하지 않는다.
