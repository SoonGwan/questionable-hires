# Receipt direct-tool availability01 review — 2026-09-27

Same skill resource `b081240e`; execution `38ca7353`.
[Protocol](RECEIPT-TOOL-BRIDGE-01-PROTOCOL.md) freezes four serial Astra medium
cells on reused exposed single/multiple window-verification tasks. All four
complete without limit, timeout, failed instrumentation, retry or replacement.
Original [commands, outputs, answers and source excerpts](results/receipt-tool-bridge-01/)
and [counter/native/preservation review](results/receipt-tool-bridge-01/review.json)
retain the actual observations. No efficiency adoption or released bridge.

| Task | CLI whole tokens | Bridge whole tokens | CLI seconds | Bridge CLI seconds | Bridge CLI + lifecycle seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| windows-single |73,513|75,413|44.974|41.258|41.856|
| windows-multiple |75,602|80,570|44.059|55.351|55.873|
| Sum |149,115|155,983|89.033|96.609|97.729|

Whole input+output increases **4.61%**; CLI time increases **8.51%** and CLI plus
bridge lifecycle **9.77%**. Zero pairs reduce both costs. Cached input is included
in input, reasoning included in output, neither added again; no billed-credit
claim. Original per-response totals and final cumulative counters reconcile for
all four stored sessions; actual model/effort contexts match. Raw process time is
shown separately from bridge startup/shutdown. Collector export/inventory time
is not included in either timing metric. Thus lifecycle timing is not elapsed
for the entire benchmark harness.

## What actually happened

Both launch-owned HTTP servers initialize with the actual Codex model host and
receive `ListToolsRequest`; retained [server reading logs and original hashes](results/receipt-tool-bridge-01/server-log-identity.json)
show discovery and graceful settled shutdown. Neither receives `CallToolRequest`.
Neither bridge cell emits an MCP call/search result; both choose the existing
CLI guide and opt-in native comparison helper. All four cells read the Receipt
entry and Python guide, not the helper implementation. Bridge single separately
reads the README; native work otherwise matches the comparison targets.

The initial protocol states that full tool schemas are additional model input.
This was an **unverified assumption about exposure**: target schemas were returned
to the host, but the original session records do not expose the target tool name
or complete schema to establish what the model received. Discovery at the host
is not proof of full model schema exposure. Original usage includes every
recorded response regardless; do not attribute the token increase to schema
size or characterize these as actual model direct-tool executions. No favorable
outcome may be manufactured by relabeling existing CLI runs or forcing retries.

Single cells each run exactly two unchanged six-test native processes with
before1/after0: nested actual `[(1,3)]` versus expected `[(1,10)]` before, correct
`[(1,10)]` after. Touching/chain/disjoint/empty/input-preservation controls pass.
Multiple cells each run three six-test processes with exits1/1/0: oldest has
separate touching and nested failures, parent only nested, current allPASS.
Four neighboring controls remain passing across all requested versions.

All **ten native processes** have zero skips and seven actual complete v2
argument observations each, including the actual identity arguments/distinct
objects: **70 retained records**. Full committed revisions, identical current
assertions, declared copy-local native windows imports, proper owned interpreter,
complete suite results and scratch removal are captured. This is equal passing
argument observation work, unlike the earlier API01 comparison's inference gap.

Pre-model/final original project inventory and modes match for each cell;
Git indexes match before collector; installed manifests/digests match the same
frozen resource, and comparison guards cover Git/skill files. No final harness,
report or production/test modification remains. Bridge servers exit−15 after
settled SIGTERM shutdown. No active-shutdown, host-cancellation or hard-kill
claim is inferred. Private initial contexts/provider configuration are not
exported; stored session hashes support the local context/counter review.

## Decision and limits

Decline this availability-only configuration. Actual native correctness is
preserved, but offering a launch tool does not make the model choose it and
adds no demonstrated efficiency benefit. The observed guide/CLI choice suggests
routing/discovery should be examined before another paid trial; it does not
prove that the guide caused the choice. Existing default guidance remains.
Do not repeat this same availability experiment without a distinct tested
mechanism. The adapter stays a dated experimental resource, not a global
registration or ordinary skill dependency.

Reused authored related tasks, n=1, alternating but shared host/cache, slight
equal local-facility prompt clarification and unequal optional reads preclude
independent/general or causal claims. This is a tool-profile experiment, not a
new skill-version gain. [Earlier API01 adverse model result](RECEIPT-ASSERTION-API-01-REVIEW.md),
[unavailable HTTP interrupted outcomes](TOOL-BRIDGE-HTTP-EXIT-01.md) and
[declined forced stdio exit](TOOL-BRIDGE-FORCED-EXIT-01.md) remain unchanged.
Whole-task improvement across all eight skills and independent runtime gates
remain unmet. No featured benchmark/chart/landing/deployment changes.

한국어: 같은 Receipt 리소스의 직접 도구 제공 비교 네 세션은 합계 토큰4.61%,
CLI 시간8.51%, 서버 시작·종료 포함 시간9.77% 증가로 채택하지 않는다. 호스트는
도구 목록을 받았지만 두 모델 모두 기존 CLI를 사용했다. 모델의 전체 도구 스키마
노출은 검증하지 않았으므로 증가 원인으로 단정하지 않는다. 실제10개 네이티브
실행·70개 인자 관찰·원본/인덱스/리소스 보존은 확인했으며 전체8개 개선은 미달이다.
