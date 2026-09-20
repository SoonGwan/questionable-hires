# Hostage mode disclosure: mixed behavior, candidate not promoted

2026-09-20 · launch `3632225` · original resources `79678f2` · GPT-6 Astra medium.
[Protocol](../../HOSTAGE-MODES-01-PROTOCOL.md), [frozen manifest](run.json),
[review](review.json), [separate author controls](author-controls.json).

Six fresh sessions completed: two exposed authored development tasks ×
baseline/original/candidate, n=1, serial. No timeouts, quota stops, excluded attempts
or replacement sessions. All functional criteria and project-only scope pass.
This does not erase an original-arm test overconstraint or candidate repair cost.

The isolated candidate relocates stateful guidance intact into a conditional
reference. Entry bytes fall from 4,362 to 3,065; the reference adds 1,590 bytes.
Runtime assets, metadata and evidence-delivery rules are unchanged. **This is
not token savings accounting. Production Hostage remains unchanged.**

| Task | Arm | Input + output¹ | Seconds | Recorded responses |
|---|---|---:|---:|---:|
| Label / optional redesign | baseline | 60,939 | 23.596 | 4 |
| Label / optional redesign | original | 67,659 | 24.084 | 4 |
| Label / optional redesign | candidate | 65,894 | 23.361 | 4 |
| Overlapping refresh | baseline | 103,035 | 103.658 | 6 |
| Overlapping refresh | original | 117,430 | 98.791 | 6 |
| Overlapping refresh | candidate | 141,655 | 117.094 | 7 |

¹ Cached input counted once within input. Per-response, cumulative and CLI final
usage reconcile. No dollar estimate. Task order partly balances arm order but is
not randomized; shared host/cache and n=1 prevent causal/general claims.

Candidate versus original: label −2.61% tokens / −3.00% time; refresh +20.63% /
+18.53%. Summed tasks: **+12.13% tokens / +14.31% time**. All repair work remains
included. No representative chart is updated from either favorable task or sum.

## What the original records show

- All label edits change only the requested text, preserve submit behavior and
  state.js, and do not undertake the optional redesign. Candidate does not read
  its stateful reference here.
- Both skill refresh sessions read their actual complete entry. Candidate reads
  the stateful reference with the initial application files in the first outer
  call—there is no observed extra response just to load that reference.
- Original copies and checks the provided controlled-call asset. Candidate writes
  its own support and initially gets two native test errors: its async `fail`
  helper shadows unittest's assertion method while a cancellation-identity
  assertion fails. It repairs both within the original session and then obtains
  eight native passes. Those first errors and tokens/time are retained.
- All final refresh implementations make the same scoped ownership fix. Each
  final native suite has eight passing tests and an observed exit 0. Baseline
  reruns after changing tests, not an unexplained duplicate of unchanged checks.
- All 24 original CLI command outputs/exits match normalized stored tool results;
  no missing, unmatched or duplicate tool outputs. Working HEAD, requirements,
  owner notes and installed resource bytes/modes remain unchanged.

## Separate delivered-test controls

After all sessions ended, copies of each delivered project were exercised under
four variants. No original model workspace changed and no missing original result
was reconstructed. All delivered suites pass their delivered implementation and
fail the broken-owner implementation. All delivered implementations pass the
independent six-test author oracle.

The valid alternative increments the internal generation by two rather than one,
without changing the specified externally observable behavior. Baseline and
candidate tests pass it; original tests reject it because they assert an incidental
`generation + 1` value in the synchronous-failure path. This is a **test
overconstraint**, not a failure of the delivered production fix. Keep it separate
from the original task-completion score and from timing evidence.

## Decision

Do not promote the disclosure candidate on these results: it has no demonstrated
overall cost advantage. Nor do the results establish the original as universally
better—the overconstraint matters. Next changes should address demonstrated
test-construction failures without forcing helper adoption or repeatedly rerunning
these exposed tasks until a favorable number appears. No 20–30% or all-eight claim.

한국어: 문서를 분리한 후보는 단순 수정에서 조금 저렴했지만 비동기 수정에서
오히려 비쌌다. 두 과제 합계 토큰 +12.13%, 시간 +14.31%여서 배포용 스킬에
반영하지 않았다. 최종 기능·범위 기준은 모두 충족했지만, 후보의 최초 테스트
오류 2개와 복구 비용을 보존했다. 별도 대조에서는 기존 스킬의 테스트가 내부
카운터에 과도하게 묶여 정상 대안을 거절했다. 정상 구현·테스트 견고성·비용을
분리해 보고하며 이전 수치나 대표 그래프를 바꾸지 않는다.
