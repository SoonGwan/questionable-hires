# Receipt supplied-tool routing01 review — 2026-09-27

Previous `08a18aed`, candidate `44c4ff5e`, execution `02313209`.
[Protocol](RECEIPT-TOOL-ROUTING-01-PROTOCOL.md) freezes four fresh serial Astra
medium cells with the same supplied local tool. Only the Receipt entry changes.
All four finish without timeout/limit/retry/replacement; original
[commands, native outputs, failed calls, answers and sources](results/receipt-tool-routing-01/)
and [counter/resource/preservation review](results/receipt-tool-routing-01/review.json)
are retained. **Declined; entry restored byte-for-byte to the previous resource.**

| Task | Previous whole tokens | Candidate whole tokens | Previous CLI seconds | Candidate CLI seconds | Previous + lifecycle seconds | Candidate + lifecycle seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| windows-single |59,590|124,586|40.241|77.129|40.830|77.655|
| windows-multiple |79,913|149,520|42.218|82.484|42.756|82.948|
| Sum |139,503|274,106|82.459|159.613|83.586|160.603|

Whole input+output **+96.49%**, CLI time **+93.57%**, CLI plus measured owned
server startup/shutdown **+92.14%**. Both pairs are worse in both measures.
Original per-response counters/final cumulative totals reconcile and actual
stored model/effort contexts match. Cached input and reasoning are not added
again. No billing claim; neither time metric includes collector post-processing.
All failed discovery/call responses and later recovery are charged; none is
subtracted or rescored as free setup.

## Observed host restriction, not successful direct execution

Previous cells use the native CLI guide/helper directly. Candidate cells attempt
the launch tool before helper guides, so the instruction changes observable
selection. Both attempted `receipt_compare` calls fail at the **Codex host**, with:

> MCP tool call requires approval, but approval policy is never

The error is an approval-policy restriction, not an actual native test failure
or SDK/server comparison result. No native tool request reaches either candidate
server: retained [server logs/identities](results/receipt-tool-routing-01/log-identity.json)
show `ListToolsRequest` but zero `CallToolRequest`. The actual attempted recipes
are retained; because never executed, their compatibility is not established.
No approval, provider/account setting or tool annotation was altered to make
them run. No attempt is reclassified as direct-tool success.

Candidate single first uses resource/template discovery returning empty lists,
then the blocked comparison, then reads the Python guide and runs the CLI.
Candidate multiple similarly performs local server resource/template discovery,
tries comparison, then reads the Python guide **plus native-preservation and
comparison-details references**, and runs the CLI. These extra interactions
and unequal reference reads explain observed work differences; the n=1 record
does not isolate a causal cost for any one instruction or host restriction.
Single candidate's project-local AGENTS search also exits1 for no matches;
this is not defective native behavior or a failed observer run.

The [no-model host native checkpoint](TOOL-BRIDGE-HOST-NATIVE-01.md) remains
actual host API execution evidence. Its direct client API invocation does not
exercise the model's tool-approval gate. It therefore was too indirect to prove
that the same tool would be executable by these noninteractive model turns.
This distinction is now established by actual failed model tool calls. Do not
repeat a paid routing trial while that same restriction remains. Do not falsely
mark the arbitrary-native-test tool read-only to evade its approval requirement.

## Native CLI recovery and preservation

All four complete their verification through the unchanged CLI helper under the
specified owned Python3.11.6. Single cells each retain six-test before1/after0;
multiple cells each retain six-test oldest1/parent1/current0. Before nested
actual `[(1,3)]` differs from expected `[(1,10)]`; oldest touching yields
`[(1,3),(3,5)]` instead of `[(1,5)]`. Current values are correct; neighboring
chain/disjoint/empty/input-preservation controls remain passing.

Ten native processes, zero skips, seven actual complete v2 assertion argument
observations each: **70 records**, including passing control/identity arguments.
All actual revisions and copied windows imports are retained. No observer
repair, rewritten tests or extra current-version native run replaces the
comparison. Pre-model/final original inventories and modes match, Git indexes
match before collection, installed resources match their frozen arm, scratch
is gone and final project production/tests are unchanged. Settled servers exit−15;
this is not host active-cancellation or hard-kill proof.

## Decision

Restore the previous entry and both capability descriptions. No general adapter
registration, bundled runtime dependency, efficiency adoption, featured/chart/
landing deployment or all-eight update follows. The SDK adapter remains a dated
experimental resource; native CLI support remains usable. Earlier
[availability01 adverse costs](RECEIPT-TOOL-BRIDGE-01-REVIEW.md),
[API01 costs](RECEIPT-ASSERTION-API-01-REVIEW.md), unavailable shutdown outcomes
and forced stdio failure are unchanged and accessible.

This repeated exposed authored n=1 diagnostic shares host/cache and unequal
optional work. Model schema availability was not fully captured; actual calls
now demonstrate selection but not native model-tool execution. Independent and
all-eight quality/token/time requirements remain unmet. Other safe native and
independent-validation work remains possible; this is not a global goal blocker.

한국어: 새 안내는 두 모델의 도구 호출을 유도했지만 호스트가 `never` 승인
정책으로 거절했다. 실제 서버 실행 없이 CLI로 복구했고, 실패·추가 읽기 비용을
모두 포함한 합계 토큰96.49%, CLI 시간93.57%, 서버 시작·종료 포함92.14% 증가다.
안내와 한·영 capability 설명을 복원했다. 네이티브10회·인자70개·원본/인덱스/
리소스 보존은 확인했으며 승인 설정을 변경하거나 실패를 성공으로 처리하지 않았다.
전체8개 개선 목표는 아직 미달이다.
