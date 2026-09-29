# Receipt Path observation01 review — 2026-09-27

Previous resource `1d0e92ac`; derived candidate and execution `8dbbb08a`.
[Protocol](RECEIPT-PATH-OBSERVATION-01-PROTOCOL.md),
[all four original costs](results/receipt-path-observation-01/comparison.json),
[response-counter reconciliation](results/receipt-path-observation-01/response-cost-analysis.json),
[original native review](results/receipt-path-observation-01/original-review.json).
All four fresh serial Astra medium sessions completed; no timeout, account-limit
stop, replacement or model retry. Recovery inside original sessions stays charged.

| Task | Previous tokens / seconds | Candidate tokens / seconds |
| --- | ---: | ---: |
| Complete ledger fix | 96,913 / 42.990 | 95,799 / 35.571 |
| Return-only partial fix | 96,407 / 49.077 | 93,352 / 39.709 |
| Sum | 193,320 / 92.067 | 189,151 / 75.280 |

Summed tokens **−2.16%**, CLI elapsed **−18.23%**; both observed pairs decrease
both metrics. These are matching-skill predecessor/candidate conditions, not a
no-skill comparison. Exposed related tasks, n=1, fixed order and shared host/cache
preclude general savings or all-eight completion claims.

## What actually changed in the original executions

Both previous cells enabled optional observation, received incomplete v2 reports
because Path-valued setup checks were unavailable, and reran the comparison with
observation disabled. Their initial suites and error exits remain preserved.

Candidate **a** enables v3 and completes the comparison once. Each before/after
suite records 14 assertion argument pairs, including five typed native POSIX Path
pairs. Before has the two expected retry failures; after passes all five tests.
The helper repair is actually exercised in this cell.

Candidate **b** compares once with observation disabled. It validly reports the
remaining defect: both revisions have two retry failures and three passing controls;
the return-only fix still doubles balances. This is not v3 runtime adoption and
cannot establish Path-observer efficacy in that model cell. An initial author audit
incorrectly required optional adoption in both candidates and stopped on that
assertion. Inspection corrected the audit, not the task, model run or score; no
replacement model call occurred. Both original routes remain visible.

All final comparisons run the unchanged five current tests and schema in isolated
copies, with real SQLite writes and fresh-connection balance reads. Native-process
copied-import evidence, actual exit codes and no skips are verified. Source file
inventories, installed resources, helper preservation reports and scratch cleanup
are checked against original captures. Final answers correctly distinguish a
complete fix from a return-only incomplete fix. No implementation was requested
or performed in the benchmark projects.

The separate [native candidate controls](RECEIPT-PATH-OBSERVATION-01.md) cover both
invocation modes, actual Path argument support, overlong/custom values, failure
preservation and Git-free source execution. Native Windows is not covered.
Known private-path/credential-pattern scans passed; they are not universal secret
detection. Full private initial contexts and session files are not exported.

Decision: the scoped functional repair and its first actual v3 use are supported.
Ordinary integration still requires coordinated v3 guide/consumer tests and the
relevant regression checks. Do not market the two-cell aggregate as an all-eight
or generally reliable efficiency improvement; integration06 token regression and
all prior adverse comparisons remain accessible.

한국어: 기존 대비 후보의 두 과제 합계는 토큰2.16%, 시간18.23% 감소했고 두 쌍
모두 두 지표가 낮았다. 다만 후보a만 실제 v3 Path 기록을 사용했고 후보b는 옵션을
끄고 정상 비교했으므로 둘 다 도구 효능의 증거라고 주장하지 않는다. 두 버전의
필수5개 테스트·실제 SQLite 효과·복사본 import·실패·정상 수정과 불완전 수정
구분·원본 보존을 확인했다. 노출된 관련 과제 각1회로 전체8개 개선을 뜻하지 않는다.
기본 스킬 통합과 회귀 검증은 아직 남아 있다.
