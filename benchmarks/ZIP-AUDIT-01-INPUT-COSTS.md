# ZIP audit01: remaining input-cost diagnosis

2026-09-21. Original resources prior`f7ecb45`, candidate`ac108f5`, launch`0807814`.
This reuses all six [reviewed sessions](ZIP-AUDIT-01.md), not new model calls.
[Recorded arithmetic and profile hashes](results/zip-audit-01/input-cost-analysis.json)
use the existing `analyze_response_costs.summarize` and `compare` functions.
They require actual response records and reconcile their sums with total usage.

| Task / arm | Recorded responses | First input | Total input | Output |
|---|---:|---:|---:|---:|
| Single / baseline |4|14,887|64,400|1,942|
| Single / prior |6|15,000|108,824|1,314|
| Single / candidate |5|15,000|84,346|1,857|
| Multiple / baseline |4|14,913|64,904|1,967|
| Multiple / prior |5|15,027|94,816|1,484|
| Multiple / candidate |5|15,027|95,606|1,520|

## Exact accounting, not causes

For each profile, input=`n*f+g`: recorded response count`n`, first input`f`,
and later input relative to that first input`g`. The symmetric difference is
`delta_n*mean(f) + delta_f*mean(n) + delta_g`, then add output difference.
Cache is counted once within input. None of these terms is a billable-cost
estimate, dispensable work or guaranteed recoverable saving.

| Candidate minus reference | Response-count term | First-input term | Later-input term | Output term | Total |
|---|---:|---:|---:|---:|---:|
| Single / baseline |14,943.5|508.5|4,494|−85|19,861|
| Single / prior |−15,000|0|−9,478|543|−23,935|
| Multiple / baseline |14,970|513|15,219|−447|30,255|
| Multiple / prior |0|0|790|36|826|

The candidate already emits fewer output tokens than baseline on both tasks.
Shortening its answer is therefore not supported as the principal intervention.
The first-input difference is only113/114 tokens, but that does **not** measure
the skill body's size: the actual body appears later in tool output. Initial
input also contains all other initial context. Later input includes source,
instructions, previous generated work and execution evidence.

## Behavior behind the counters

From original calls, not inferred from child-process counts:

- Single/prior reads the entrypoint, inventories files, reads project plus
  native-batch guide, reads probe guide, then executes its one-entry batch.
- Single/candidate reads the entrypoint/instruction discovery, inventories files,
  reads project source, then executes a direct native audit. It reads no helper
  reference. Therefore shortening batch documentation cannot remove this cell's
  remaining baseline gap.
- Multiple/prior and candidate both read the entrypoint, project/batch guide,
  requirements/probe guide and execute a batch. Both have5 recorded responses;
  candidate's slightly larger total is not an additional response in this pair.
- Baselines inventory, inspect source, and execute their direct comparisons.
  Their4 responses do not mean their evidence can be substituted into skill
  runs or that every skill read is avoidable.

The existing [discovery candidate](results/con-artist-discovery-01/README.md)
already tested known/unknown-path guidance and failed its frozen acceptance gate.
Do not repeat it unchanged because this smaller project also has an inventory
step. Nor should a helper be forced merely to reduce generated code: direct
single-fault work here is valid and cheaper than the prior helper session in
tokens, but slower in wall time. Both metrics and different extra checks remain.

## Next boundary

Do not launch a favorable retry of ZIP or claim that compact JSON repairs these
totals: that change postdates these resources and affects returned report
representation, not the initial required investigation. No new grouping API or
global instruction compression is justified by this accounting alone.

Current eight-role performance coverage remains stale: intervening role changes
mean the old all-eight result cannot describe today's bundle. Before promoting
any efficiency release, a current-resource cross-role regression comparison is
still needed, followed by separate unexposed validation for generalization. A
reused eight-task screen must be labeled exposed regression, retain all outcomes,
freeze source/settings first and never be represented as independent validation.
This diagnosis changes the next scope from another Con Artist wording tweak to
checking whole-bundle behavior; it does not itself launch or pass that screen.

한국어: 기존6회 기록의 비용을 분해했다. 수정본은 두 과제 모두 무스킬보다 응답이
1회 많지만 출력 토큰은 적다. 단일 과제는 도구 안내 문서를 읽지도 않았으므로
배치 안내 축소만으로 남은 비용 차이를 설명할 수 없다. 과거 탐색 안내 후보도
이미 실패해 같은 접근은 반복하지 않는다. 다음 전체 비교는 현재8개 스킬의
회귀 상태를 확인해야 하며, 기존 과제를 쓰면 독립 검증이 아님을 명시해야 한다.
