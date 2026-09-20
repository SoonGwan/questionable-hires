# Original-session usage profile 01

2026-09-20. Diagnostic analysis of all ten unchanged korean-auto-01 sessions,
resource `2990f44`, launch `ad3fbdb`. No model executions or changed measurements.
[Numeric records](results/korean-auto-01/usage-profile.json),
[original outcomes/limitations](results/korean-auto-01/README.md),
[profiler](profile_session_usage.py).

## Verified accounting

Each local original rollout is matched to its CLI thread ID. Unique recorded
response usage sums to cumulative token-count events and the CLI's final usage
for input, cached input and output in all ten sessions. The export contains only
usage, source hashes, record line numbers and session identity—not private context.
Duplicate response identities are counted once only when identical; conflicting
duplicates, decreasing counters, impossible cache counts and mismatched totals
fail validation. Missing response-level records remain null, not estimated.

Across 45 recorded responses: **730,880 input + 9,435 output = 740,315 total**.
Cached input is 641,152, a subset of input; uncached input is 89,728. Input is
98.73% of the reported total. This is **not** a monetary or latency attribution.
Reasoning is not added again to output, nor cache added again to input.

| Case | Recorded responses | Input | Cached input | Output |
|---|---:|---:|---:|---:|
| Age fix | 5 | 84,500 | 77,952 | 712 |
| Formatter review | 4 | 64,706 | 55,808 | 622 |
| History | 5 | 81,143 | 68,224 | 806 |
| Label with optional redesign | 4 | 64,425 | 55,424 | 422 |
| Persistence audit | 5 | 82,343 | 71,552 | 1,443 |
| Plain label | 4 | 61,630 | 54,656 | 326 |
| README typo | 3 | 45,918 | 42,240 | 214 |
| Rolling schema | 5 | 81,137 | 71,552 | 1,230 |
| Search diagnosis | 5 | 81,841 | 72,704 | 1,757 |
| Interaction QA | 5 | 83,237 | 71,040 | 1,903 |

The first recorded response consumes 15,101–15,148 input tokens across cases.
In all eight positive cases, its usage record precedes the first observed full
skill-body output. Thus this initial consumption cannot be attributed to the
later body read. Catalog/runtime/task context remains; no claim isolates its
individual components. Even the two controls with no observed body exposure
consume 46,132 and 61,956 total tokens.

## What changes the next decision

Shorter final answers alone target only a small part of these totals. Investigate
unnecessary model/tool round trips and repeated context loading, while preserving
the actual task checks. This is an optimization hypothesis—not a counterfactual
claim that deleting one command saves one full response. Several shell commands
can share one outer call/response, and subsequent context/work can change.

The age fix reads Receipt and Hostage together in one outer output: removing the
extra body does **not** automatically remove a response. All positive sessions
already obtain their intended body during the first outer tool call. Rewriting
body instructions cannot retroactively govern that first call. Existing batching
experiments and mixed results remain relevant; do not keep adding stronger generic
batching rules or claim document-byte reduction equals token savings.

Next candidate comparisons should inspect recorded response counts and required
work alongside total tokens. Target a demonstrated redundant post-load step,
reusable execution support or context acquisition that removes actual work. Never
drop regression controls, hide failed attempts, modify private runtime guidance,
or alter task difficulty just to reach a percentage. No current skill or featured
chart is changed by this diagnostic pass. All-eight efficiency remains unproven.

한국어: 기존 10개 원본의 응답별 사용량·누적값·CLI 최종값을 대조했다. 전체
740,315토큰 중 입력이 98.73%였고, 출력은 9,435토큰이다. 캐시 입력은 입력의
부분집합이며 비용·시간 비율과 같지 않다. 추가 스킬 문서는 같은 도구 응답에
포함돼 있었으므로 문서를 없애면 호출 하나가 줄어든다고 계산할 수 없다.
이 분석은 불필요한 왕복·반복 작업을 줄이는 후보를 우선 검토할 근거이지,
성능 개선 결과가 아니다. 모델 재실행·기존 결과 변경·대표 그래프 변경은 없다.
