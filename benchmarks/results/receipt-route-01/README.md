# Receipt support routing 01 — small mixed improvement, not adopted

2026-09-20, resources `ca668a4`, launch `5f05ae5`.
[Frozen protocol](../../RECEIPT-ROUTE-01-PROTOCOL.md),
[candidate](../../RECEIPT-ROUTE-CANDIDATE.md), [reviewed rows](comparison.json).
The candidate moves support-selection guidance to the entrypoint and removes
the relocated sentence from the routine guide. It does not include the rejected
read-order rewrite; all helper/runtime behavior is unchanged.

| Variant | Arm | Input + output tokens | Process seconds | Responses | Task / scope |
| --- | --- | ---: | ---: | ---: | --- |
| Complete (a) | Original | 89,848 | 43.705 | 4 | pass / pass |
| Complete (a) | Candidate | 97,980 | 39.931 | 5 | pass / pass |
| Partial (b) | Original | 90,474 | 39.450 | 4 | pass / pass |
| Partial (b) | Candidate | 79,316 | 38.415 | 4 | pass / pass |
| **Sum** | **Original** | **180,322** | **83.155** | **8** | **2 / 2** |
| **Sum** | **Candidate** | **177,296** | **78.346** | **9** | **2 / 2** |

Candidate sums are **−1.68% tokens / −5.78% time** versus original. Cache input
is counted once, reasoning tokens are not added again. These are ratios of sums,
not confidence intervals, causal estimates or a broad improvement guarantee.
Complete-case candidate uses more tokens, despite omitting helper source reads.
No fresh no-skill arm: historical baseline costs are not this experiment's
control. All four scheduled fresh GPT-6 Astra medium sessions completed; no
retry, timeout, exclusion or replacement. Shared host/cache, fixed reversed
order and n=1 remain limitations. These are two exposed variants of one authored
SQLite task, not held-out tasks or independent real projects.

## What changed in actual behavior

Both originals read the routine guide, detailed reference and full helper
implementation in a bulk command. Candidate a reads the routine guide then the
complete Preservation guards section; candidate b still reads the entire
detailed reference. Neither candidate reads helper implementation. This is
partial evidence of changed support selection, not perfect selective reading.
Candidate a adds a separate final review response; the others batch final
review with comparison. Less source text therefore does not guarantee fewer
responses or lower whole-task cost. All four use the same default absolute
interpreter without the prior experiment's xcodebuild warnings.

## Native outcomes and preservation

Manually reviewed original commands and their correlated outputs show identical
current five-test assertions/schema against fully identified revisions. All
use the unchanged helper's module invocation and real SQLite/fresh-connection
balance reads. Same native-process copy-local package, implementation and test
paths/PIDs are recorded. Before has two genuine retry failures and three passing
controls. Complete after passes all five; partial after retains two failures:
credit `(False, 250)` versus `(False, 125)`, debit `(False, -100)` versus
`(False, -50)`. Native exits are 1/0 for a and 1/1 for b. No setup failure,
skip, timeout or truncated native output substitutes for evidence.

Both partial-fix answers correctly reject the fix without repairing it. All
whole-tree guards and selected-original checks pass, comparison copies are
removed, final whitespace/diff/status exits are individually retained and zero.
Original files (including ignored cache and owner notes), HEAD and installed
resources are unchanged; no extra harness/report remains. All five frozen
criteria and scope pass in every cell. Selected original records support these
judgments; helper CLI exit 0 alone does not.

Author preflight, separately retained under `native_preflight` in [run.json](run.json),
executes both variants, real positive/negative native controls, preservation and
cleanup before launch. It is not a model sample or post-run replay. Exposure
reports verify the Receipt body in initial messages; later file reads are not
first exposure. Private initial instruction text is not exported.

## Capture exceptions

- Original a item 2 / stored line 22 and original b item 3 / stored line 23:
  bulk implementation reads are outer-truncated. Do not infer omitted source.
- Original a item 3 omits the leading `COMMAND:` line from CLI aggregation;
  stored line 29 retains it. Native JSON and separate exits remain complete.
- Candidate a item 3 omits the preceding preservation-section and `.gitignore`
  output from CLI aggregation; stored line 29 retains them. Native JSON is complete.
- Both b native comparisons are item 5 / stored line 32 and match CLI aggregation.
  Mechanical truncation hints can match `output_truncated:false` or reference
  prose; those flags do not establish actual truncation. All hints remain in
  exported review records rather than being silently overwritten.

Production Receipt and featured charts remain unchanged. Before considering
adoption, test a different workflow and a genuine compatibility/diagnosis case;
routine success does not prove necessary deeper inspection survives. Broad
all-eight/no-skill performance and release readiness remain unproven.

## 한국어 요약

자료 선택 안내를 먼저 주는 후보는 새 세션 4회에서 기존 대비 합산 토큰
**1.68%**, 시간 **5.78%** 감소를 관측했다. 모두 실제 테스트·수정 판정·원본
보존을 충족했다. 후보가 도우미 구현 전체를 읽지는 않았지만, 한 경우에는
마무리 응답이 추가돼 토큰이 오히려 늘었고 다른 경우에는 상세 문서 전체를
읽었다. 따라서 일관되거나 큰 성능 개선으로 주장하지 않는다.

이미 노출된 한 과제의 두 변형을 각 1회 비교했으며 새 무스킬 대조군은 없다.
원본 출력과 CLI 요약의 차이·구현 읽기 잘림도 보존했다. 다른 작업과 실제
호환성·진단 상황의 검증이 남아 있어 아직 실제 스킬에 반영하지 않는다.
공개용 그래프와 기존 성능 주장도 변경하지 않는다.
