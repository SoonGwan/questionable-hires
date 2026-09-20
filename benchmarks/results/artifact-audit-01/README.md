# Artifact audit 01: equal delivery, helper impact not established

2026-09-20. Launch `90e6aee`; original Con Artist `9c0c458`, candidate `7c96592`.
[Frozen protocol](../../ARTIFACT-AUDIT-01-PROTOCOL.md), [inputs and preflight](run.json),
[all reviewed observations](comparison.json).

One authored diagnostic task intentionally exercises pytest configuration and
native test strengthening. It is not an unbiased real-project sample. Three fresh
Astra medium sessions, one repeat each, fixed serial original/baseline/candidate
order, shared host/cache. Every scheduled session completed without timeout,
replacement or quota stop.

| Condition | Total tokens | Wall seconds | Shell commands | Native suite executions | Full task |
|---|---:|---:|---:|---:|---|
| No-skill baseline | 205,066 | 115.405 | 8 | 6 | Pass |
| Original skill | 103,932 | 86.939 | 6 | 4 | Pass |
| Candidate skill | 125,267 | 98.885 | 6 | 4 | Pass |

Input plus output, cached input counted once. Candidate uses **38.91% fewer tokens
and 14.31% less wall time than baseline**, but **20.53% more tokens and 13.74% more
time than original**. These are observations from one attempt per condition,
not a general efficiency estimate or reason to promote a headline chart.

Crucially, **neither skill session read or executed the changed helper/references**.
Both received the identical skill entry and wrote their own native comparison.
The experiment does not measure the causal effect of the pytest helper correction.
Do not claim that this patch saved 39%, or revert a tested correctness repair on
the basis of this candidate/original cost difference.

## Native evidence and delivered work

All three deliver byte-identical tests, also identical to the separately preflighted
author oracle: one decoded-JSON equality assertion added at the existing native
test path. Production/configuration/fixtures and both parametrizations remain.
No author test replay or model replacement was used to establish these outcomes.

Each session establishes four accepted native comparisons:

| Tests / implementation | Native outcome | Exit |
|---|---|---:|
| Original / correct | 3 passed | 0 |
| Original / digest-loss fault | 3 passed | 0 |
| Strengthened / correct | 3 passed | 0 |
| Strengthened / digest-loss fault | 2 failed, 1 passed | 1 |

The two failures compare empty digests with the required 64-character `a`, `b`
and `c` values. Names, duplicate Unicode names, order and counts remain intact;
the empty control remains passing. Twelve decisive same-process observations per
condition record actual expected/observed records and the loaded copied source.
Original uses an executing-frame observer; baseline/candidate use a native pytest
call observer with module/function binding evidence. All recorded source hashes
match the frozen correct implementation or the single specified mutation.

Baseline initially wrote an observer with an unclosed file, causing warning-as-error
failures in **two extra native runs**. It fixed its own observer and reran those
checks within the original session. All that time, tokens and initial failure
evidence remain included. These instrumentation failures are not mutant detection.
Both skill sessions avoid that specific rework; this n=1 observation does not prove
that either skill reliably prevents it.

Commands, CLI events, original answers, selected stored tool records, final source,
metadata, context summaries and reviews are retained for all three conditions.
Nineteen of twenty CLI command output/exit pairs match normalized stored responses.
Baseline `item_5`, the initial broken-observer runs, has a truncated stored response
at original line 38; omitted material stays unavailable. Its later accepted native
outputs (`item_6`, `item_9`) are complete exact matches. Original/candidate decisive
native outputs are both `item_6`, also exact matches. No rerun repaired a transcript.

Mechanical comparison and original cleanup commands confirm that only the allowed
test file changed, modes are 0644 throughout, HEAD/installed resources are unchanged,
and no extra files or owned scratch remain. Recorded initial context contains the
matching entry before the first tool in both skill sessions, not the baseline.
Private full instructions are excluded; unrelated catalog names are hashed.

## Decision

Retain the correctness repair and all observations, but make no new helper
performance claim or all-eight claim. More tests of exactly this task would not
fix the missing intervention. Future evaluation should distinguish whether the
changed capability was actually used, while allowing adequate native alternatives.
Do not force helper adoption or remove baseline repair cost to engineer a win.

한국어: 세 조건 모두 같은 테스트 한 줄을 추가하고 네 가지 정상/결함 대조를
충족했다. 수정 후 스킬은 무스킬보다 토큰 38.91%·시간 14.31% 적게 썼지만,
수정 전 스킬보다 토큰 20.53%·시간 13.74% 더 썼다. 두 스킬 세션 모두 바뀐
도우미를 사용하지 않아 이번 패치의 성능 효과로 해석할 수 없다. 무스킬이 만든
관찰 코드의 오류와 수정 비용도 포함했다. 단일 작성 과제이며 전체 성능이나
대표 그래프로 확대하지 않는다.
