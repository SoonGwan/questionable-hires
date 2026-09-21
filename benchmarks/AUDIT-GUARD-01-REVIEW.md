# Audit guard 01 — 2026-09-21

Resource comparison: prior `f157b76`, current `f6f2980`; launch `aa5fa00`.
[Frozen protocol](AUDIT-GUARD-01-PROTOCOL.md), [original evidence](results/audit-guard-01/README.md).
One authored SQLite task, three fresh GPT-6 Astra medium sessions, fixed serial
order prior/baseline/current. All scheduled attempts retained; no repairs, retries,
timeouts or excluded cells. No concurrent author regression suite.

| Condition | Total tokens | Wall seconds | Responses / shell commands | Reviewed criteria |
| --- | ---: | ---: | ---: | ---: |
| Prior | 56,323 | 68.410 | 3 / 3 | 5/5 |
| No skill | 67,272 | 78.327 | 4 / 3 | 5/5 |
| Current | 57,589 | 74.884 | 3 / 3 | 5/5 |

Input includes cached input once; output includes reasoning once. Current uses
14.39% fewer tokens than baseline, but 2.25% more than prior. Wall time is 4.40%
below baseline and 9.46% above prior. These are descriptive differences, not
established improvements: **none of the three uses the helper or new guard**.
The two skill entrypoints are identical. Current reads the entrypoint but neither
guide nor implementation; the new option remains undiscovered in this attempt.
Both skill arms batch initial discovery and reading into one response; baseline
uses two responses. This observation does not establish the cause of cost changes.

## Native evidence

All three introduce a commit after each SQLite insert. Original two native tests
pass correct and faulty code. Each supplies the same two strengthened tests to
both implementations: four pass correct, two fail faulty on actual persisted
rows after a duplicate-key exception; existing success/empty controls still pass.
Exception assertions succeed before persisted-state assertions reject partial
commits. All use real SQLite, not a simulated replacement.

Prior/current profile actual function calls and verify copy-local function/module
and test bindings. Baseline verifies module identities in the native unittest
process. Prior uses 30-second child deadlines, current 60-second deadlines,
baseline only the outer 360-second limit. Row selections and tracing differ, so
native work is not identical. No assertion repair occurs.

Every arm authors its own copy/run/whole-root inventory/cleanup driver. Independent
artifact checks find no changed originals, new files, HEAD or staged-entry changes,
or changed resources. Pre-session binary index bytes were not independently
captured; staged entries are checked separately. Owned scratch is removed.

CLI native output tails are shorter than original recordings in all three arms
(prior 3,792/4,394 characters, baseline 4,024/4,829, current 4,763/6,312). Complete
original tool records are retained; no replay replaces them. Skill-body exposure
is recorded separately without publishing private initial messages.

## Decision and limits

Retain the locally verified optional guard, but do not claim model adoption or
efficiency from it. Correct the stale entrypoint routing separately; that change
will be unmeasured, not retroactively credited here. Do not rerun this now-exposed
fixture until favorable. No featured chart promotion or release approval.

This is an authored capability-targeting task, n=1 per arm, not an organic issue
or independent holdout. Fixed order, shared host/cache, unequal workflows and
unblinded author review prevent causal/general efficiency claims. Whole-task
performance across all eight skills remains unproven.

한국어: 세 조건 모두 요구사항을 충족했다. 현재 버전은 무스킬보다 토큰을
14.39% 적게 썼지만 이전 버전보다 2.25% 더 썼다. 새 도우미는 한 번도 사용되지
않았으므로 새 기능의 성능 개선으로 해석하지 않는다. 진입 안내의 누락은 별도로
고치고, 이번 결과와 불리한 수치까지 보존한다. 대표 그래프는 바꾸지 않는다.
