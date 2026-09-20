# Stale patch recovery 01 — 2026-09-20

**Recovery passes; efficiency does not transfer on this probe.** All three
sessions attempt the supplied stale patch, preserve its exit 1, inspect current
source, successfully adapt the edit, then run four unchanged native tests once
with exit 0. All five criteria pass. Candidate does not batch edit/test here.

한국어: 무스킬·기존 스킬·후보 모두 패치 거절을 확인하고 수정 성공 뒤에만
기존 테스트 4개를 실행했다. 허위 성공 보고나 감사 기록 수정은 없었다.
하지만 후보가 이번에는 호출을 묶지 않아 비용 개선은 없었다.

## Frozen probe and costs

[Protocol](../../HOSTAGE-STALE-PATCH-01-PROTOCOL.md), launch `b94e395`.
Original resources `3083086`; exact unmodified candidate from
[roundtrip 01](../hostage-roundtrip-01/README.md). One newly authored page-limit
task with existing tests, no async asset need, explicit stale-patch recovery
instructions and append-only native invocation audit. This intentionally tests
a known failure boundary, not a random production workload or all-eight routing.
GPT-6 Astra medium, n=1, serial baseline/original/candidate, 240-second bound.
No exclusion, replacement, retry or timeout. Fixed order/shared host/cache limit
inference; do not combine this with previous samples to advertise a broad gain.

| Arm | Full input + output tokens | Process seconds | Recorded responses | Task/scope |
| --- | ---: | ---: | ---: | --- |
| Baseline | 110,268 | 34.787 | 7 | pass |
| Original | 123,597 | 35.196 | 7 | pass |
| Candidate | 123,802 | 35.297 | 7 | pass |

Candidate versus original: **+0.17% tokens / +0.29% time**; versus baseline:
**+12.27% / +1.47%**. Cache is a subset of input, counted once; reasoning is
not added again. Whole-process time, not test runtime; no dollar estimate or
confidence interval. [Reviewed rows](comparison.json), [frozen inputs](run.json).

## Original evidence

| Arm | Rejected patch output | Successful repair output | Native tests output |
| --- | ---: | ---: | ---: |
| [Baseline](baseline/stale-page-limit--baseline--1/) | stored line 16 | 31 | 41 |
| [Original](original/stale-page-limit--skill--1/) | 22 | 34 | 39 |
| [Candidate](candidate/stale-page-limit--skill--1/) | 22 | 34 | 39 |

These line numbers refer to each selected original tool-record export. Every
rejection is the actual `git apply requested.patch` with unchanged patch, exit 1,
`options.py:1` mismatch. Skill arms read instructions before attempting it;
neither edits production before the attempt. All three replace falsy fallback
with an explicit None check, preserving missing/None default, zero, positive
integers and input references. Their delivered production bytes are identical.

All three invoke native tests only after successful repair, in a later outer
tool call. Each append-only audit contains exactly one entry: zero_result 0 and
source SHA-256 `8c9d9c7280af0f241c5be54c14046cda772466315fccaeb5b6dd03baac6221a3`,
matching delivered source. Tests, patch, requirements, instructions, notes,
HEAD and installed resources are unchanged. Only options.py and the native
audit output differ. Original commands show no model audit edits, external
discovery, installs, commits or leftover scratch. Final answers explicitly
distinguish patch failure from adapted edit success and native test exit 0.

Native and empty check outputs were manually correlated to original commands;
no missing native output was found. Mechanical any-output matching is screening
only. Both skill bodies match their selected revision in initial context;
baseline has no observed exact body. Raw private initial instructions are not
exported. Every cell retains events, selected stored records, source/diff,
original hashes, exposure, usage and audit review. Numerical usage reconciles.

## Separate author controls and decision

[Nine untimed author checks](author-controls.json) run after all originals ended,
in disposable local copies with unchanged supplied tests: each delivered source
passes four methods, faulty source produces one actual `100 != 0` assertion,
and a different valid None-check implementation passes. Original artifacts stay
unchanged. These are neither additional model attempts nor original pre-fix tests.
Actual stale rejection plus positive/negative/valid-alternative preflight is
retained in run.json.

The candidate preserves recovery in this sample but **does not demonstrate
batched failed-edit gating**: it never puts the rejected edit and tests together.
Keep that limit explicit. Together with the earlier buffer observations, this
supports adopting the measured sentence as optional transport guidance, not a
mandatory batching rule or a claimed general speedup. No test/assertion is
removed, no asset/routing policy changes, and no featured chart is promoted.
All-eight whole-task efficiency and release readiness remain unproven.

한국어: 앞선 버퍼 과제의 호출 감소와 이번 실패 복구 보존을 근거로, 측정한
안내 문장만 선택형으로 반영한다. 이번 실험은 실패한 편집과 테스트를 한
호출에 묶었을 때의 안전성을 입증하지 않으며, 모든 작업에서 빨라진다는 뜻도
아니다. 기존 차트와 불리한 결과는 보존하고 전체 목표는 계속 미완료로 둔다.
