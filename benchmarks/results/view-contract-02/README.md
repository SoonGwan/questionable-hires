# Friday discovery follow-up — 2026-09-15

Launch `04bfb78`; original Friday `45a2741`, entry-only candidate `dbbbba0`.
[Protocol](../../VIEW-CONTRACT-02-PROTOCOL.md), [comparison](comparison.json).
Same exposed synthetic fixture as screen 01, not a fresh real-project holdout.
Candidate then original, one fresh persisted GPT-6 Astra / medium session each,
serial cells, 240-second cap; no retries or concurrent author test runs.

| Observation | Original | Candidate |
| --- | ---: | ---: |
| Total input + output tokens, cache counted once | 74,767 | 103,215 |
| Process time | 68.476s | 62.031s |
| Shell commands / outer tool calls | 4 / 3 | 4 / 4 |
| First call reads supplied release note | No | Yes |
| Matrix helper used | No | Yes |
| New `assert_rows` API used | No | No |

Candidate changes the targeted first-call pattern but **does not achieve a cost
win**: +38.05% tokens / −9.41% time. It combines inventory and release/entry reads,
then reads SQL/readers plus the matrix guide, separately reads the helper's full
implementation, and executes one matrix. Original lists first, batches two source
reads in one outer call, and executes native SQLite. Extra guide/implementation
context and the fourth outer call offset the initial batching opportunity.
This is an observed execution difference, not a causal estimate from one pair.

## Reviewed original work

Both execute actual supplied SQL and both literal queries at all five checkpoints,
compare ordered labels/full rows/native BLOB bytes, identify phase 2's active OLD
column mismatch and distinguish inactive NEW errors. Both show code-only rollback
is insufficient and down preserves updated/unchanged/inserted rows and all bytes.
Candidate explicitly checks matrix completion, all ten results, no truncation,
expected native rows and columns; it does not merely trust helper CLI success.

Original additionally checks underlying table states. Mitigations differ but
remain scoped recommendations: original suggests retaining the old view and
adapting NEW, or a non-overlapping cutover if contracts stay fixed; candidate
suggests an explicit OLD projection plus a dual-alias transitional view for
coexistence. Neither modifies the proposal or claims to have executed mitigation.

All **eight shell output/exit pairs** exactly match original stored responses
after path/newline normalization, including the candidate's implementation read
and full decisive matrix result. No missing, unmatched or duplicate outer IDs.
Both exact frozen entry bodies were injected before the first tool; per-cell
`initial-context.json` records hashes and catalog names without private text.
Catalog mentions are not proof of executable availability or disable enforcement.

Actual inventories contain only the six supplied files outside Git/skills. All
project files and installed resources remain unchanged; no scratch remains and
neither creates a persistent database. Both use SQLite 3.51.0. This review is
original model evidence, not an author rerun. Full private rollouts stay local.

## Decision and limits

Retain the optional native-path clarification without a performance claim. Stop
tuning this exposed task: first-call behavior changed, but optimizing that step
alone did not reduce total tokens. Do not force helpers or add another convenience
API from this result. Further work should target actual end-to-end bottlenecks and
unfinished distribution checks. No new skill edit, chart promotion or all-eight
claim. Fixed order, shared host/cache, n=1 and reused targeted task remain limits.

한국어: 수정본이 첫 탐색과 문서 읽기를 묶기는 했지만, 이후 도우미 문서·구현
읽기가 추가돼 토큰 38.05% 증가·시간 9.41% 감소였다. 전체 비용 개선으로
인정하지 않는다. 양쪽 모두 필수 열 번의 관측과 정확한 판정·원본 보존을 확인했고,
원본 응답 여덟 개와 초기 스킬 주입도 검증했다. 이 과제의 문구 튜닝은 멈추며,
불리한 결과를 보존하고 대표 그래프는 바꾸지 않는다.
