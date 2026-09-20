# Friday output pilot 01 — reviewed 2026-09-21

**Candidate not adopted.** Launch `5d68166`, original resource `75f6b4f`, guide-only
candidate transformation `eaac566`. [Frozen protocol](../../FRIDAY-OUTPUT-01-PROTOCOL.md),
[all reviewed rows](comparison.json), [fixed schedule](schedule.json).
Two related authored SQL tasks × three conditions × one session, GPT-6 Astra medium.
No retries, timeouts, account-limit stops, excluded cells or changed model inputs.

| Requested output | Condition | Total tokens | Seconds | Recorded responses | Reviewed criteria |
|---|---|---:|---:|---:|---:|
| Contracts | Baseline | 80,694 | 60.689 | 5 | 5/5 |
| Contracts | Original | 70,176 | 60.958 | 4 | 5/5 |
| Contracts | Candidate | 70,460 | 60.303 | 4 | 5/5 |
| Raw observations | Candidate | 92,194 | 71.464 | 5 | 5/5 |
| Raw observations | Original | 104,526 | 82.473 | 5 | 5/5 |
| Raw observations | Baseline | 74,179 | 104.474 | 4 | 5/5 |

Total tokens are original input plus output, with cached input included once.
Summed baseline/original/candidate: **154,873 / 174,702 / 162,654 tokens** and
**165.163 / 143.431 / 131.767 seconds**. Candidate versus original is −6.90% tokens
and −8.13% time; versus baseline is **+5.02% tokens** and −20.22% time. These are
descriptive observations, **not the effect of this candidate**, causal savings or
evidence of a general 20% improvement. Same host/cache, unequal discovery, n=1.

## What was actually exercised

Every condition executes the supplied SQL in an in-memory database and both actual
literal readers at all five phases. Full ordered column/row comparisons retain the
zero-valued SKU. OLD's total-stock contract fails after reserved stock is written
at step 3 and remains broken at the no-SQL restart, despite unchanged column names.
Step 2 is the last compatible checkpoint for these data. Step-1 NEW errors are
inactive, not blockers. Base-table observations verify all quantities/reservations
survive down; all answers propose preserving OLD's total view without applying a fix.

Contract checks vary: baseline/candidate compare and print actual versus expected
reader values, with storage/preservation assertions; original additionally asserts
the complete ten-result status sequence. No test-method count or exit-only rule is
used for scoring. Successful comparisons and the known mismatches are reviewed from
their actual code and original output, not inferred from PASS prose.

All raw-output conditions emit parseable complete JSON with ten observations,
actual inactive error, columns/rows, completion/truncation and reader file/constant/
line/byte hash/exact SQL. Separately parsing those **original outputs**, without
rerunning SQL, matches all reader values, step-3/step-5 stored data and source
provenance. Baseline reports distinct source-file and SQL hashes; their labeled
scopes are retained, not conflated. Full row/error output was not suppressed.

## Why the candidate is not validated

Neither candidate's modified guide is observed as an exact full body in recorded
input messages or tool outputs. The original guide is observed only in raw-output
original (stored line 22); that run also reads the full helper, then writes its own
SQLite code rather than using it. All other runs write their own checks without
reading this guide; **none uses the matrix helper**. Optional helper adoption was
not a task requirement and non-use is not a quality failure. But costs of different
discovery paths cannot establish that an unread guide change helped.

Every skill condition has exact main-body initial-message exposure and a later
read, recorded in `skill-exposure.json`; baseline matching bodies are unobserved.
Guide exact-match hashes/locations are in `comparison.json`. Missing matches mean
unobserved, not proof all equivalent content was absent. Exposure does not prove
compliance. Private initial messages were inspected but are **not published**.

## Evidence integrity and limitations

Each numbered directory retains CLI events, commands/outputs, answer, metadata,
project files, source hashes, original tool records, usage profile and body-exposure
observations. Every original shell output/exit matches its CLI capture; no capture
omissions or ordering repairs. All usage counters reconcile. Original source modes
remain 0644; content, HEAD/index and installed resources are unchanged, with no
extra project files or scratch. No model or author post-run SQL execution substitutes
for the original observations. Preflight author matrices are separate protocol data.

Before launch, resource verification detected an omitted trailing blank line in
the copied UI metadata. It was restored before any model call; byte/mode validation
then passed. No frozen case or candidate changed. Privacy pattern scanning passed;
it is not a guarantee of universal privacy or task correctness.

These are small, related synthetic tasks, unblinded author review and single runs,
not independent real-project holdouts. Production remains unchanged; do not promote
this pilot to featured graphs or force helper adoption on the exposed tasks to
obtain a more favorable result. The proposed guide change remains unadopted.

한국어: 6개 실행 모두 요구한 SQL 검토와 출력·보존 기준을 충족했다. 하지만
후보는 수정 가이드의 전체 내용이 관측되지 않아 비용 차이를 수정 효과로 볼 수
없다. 후보 합계는 무스킬보다 시간은 짧고 토큰은 더 많았다. 원본 기록과 불리한
수치도 보존하며, 후보를 채택하거나 대표 그래프를 바꾸지 않는다.
