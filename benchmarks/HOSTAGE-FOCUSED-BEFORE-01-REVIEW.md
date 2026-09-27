# Hostage focused before01 — decline, 2026-09-28

Previous resource **`eef44470`**, candidate/execution **`73b9f4db`**.
[Protocol](HOSTAGE-FOCUSED-BEFORE-01-PROTOCOL.md),
[all four original cells](results/hostage-focused-before-01/run.json),
[costs](results/hostage-focused-before-01/comparison.json),
[response arithmetic](results/hostage-focused-before-01/response-cost.json), and
[original source/native review](results/hostage-focused-before-01/original-review.json).

**Do not adopt.** The narrower before-check was observed, but both tasks used more
whole-task tokens. The defect task also took longer. The candidate stays isolated;
ordinary skills, personal installation, downloads and featured charts are unchanged.

| Task | Previous tokens | Candidate tokens | Previous seconds | Candidate seconds |
| --- | ---: | ---: | ---: | ---: |
| Defect, refresh-owner-a | 116,950 | 133,379 | 98.506 | 106.009 |
| Valid code, refresh-owner-b | 93,875 | 111,816 | 106.221 | 99.428 |
| Sum | 210,825 | 245,195 | 204.727 | 205.437 |

Tokens **+16.30%**, CLI elapsed **+0.35%**. Response counts rise6→7 on a and5→6 on b.
Original per-response usage reconciles with each final CLI counter, counting cached
input once. All four sessions complete without timeout, limit, retry or replacement.
These are exposed authored development cases, with n=1, fixed balanced order,
shared host/cache and unequal optional work. This is neither a causal estimate nor
an all-eight or no-skill comparison.

## Mechanism and original verification

On a, previous runs all five methods before repair: five failing subtests in three
methods, with `False is not True` at the pending-state boundary. Two methods pass.
It then changes only the existing-generation guard around `finally` cleanup and
all five methods pass. Candidate first runs only
`test_earlier_success_while_latest_pending`: one actual pending-state assertion
failure, exit1. It makes the same production guard change, then all eight authored
methods pass, exit0. Both suites were authored before their before-check; visible
subsequent edits change only production. Neither a run omits actual reproduction.
Candidate's seven other methods are unrun before repair, not proven failing.

The before CLI output is4,738 versus1,743 characters. This is observed output size,
not a token saving estimate. Both full after suites retain real Preview calls,
independent overlapping callbacks, both success orders, earlier failure/cancellation,
latest failure/cancellation and retry, synchronous failure, result/error identity,
prior display and instance isolation. Previous groups several scenarios in
subtests; five versus eight method names does not establish less coverage.

On b, both preserve the valid production file exactly and run eight passing native
methods. They exercise the same major required boundaries with different details:
previous completes older success during retry after latest failure/cancellation;
candidate settles older success before that retry, and uses older failure during
retry after synchronous failure. Instance-isolation scenarios also differ. This is
not assertion-by-assertion identical work or exhaustive state-space validation.

All four copy the unchanged ControlledCall/OwnedTasks asset exactly, use actual
callback-entry gates, cooperative bounded task waits and cleanup registered before
starting tasks. No async override of synchronous unittest methods was found by
static scan. No timing sleeps or replacement production simulation appears in the
reviewed suites. Correct execution is established by original native output; no
author replay, capture-recovery run or model rerun was performed.

Each original native command has complete method headers, summary and its own exit.
Previous a additionally repeats copy-integrity and diff checks after an earlier
combined check. Candidate a separately reads the helper and repeats discovery.
All four read the exact entry body and full Python asset; candidate entry size is
5,441 bytes versus5,061. Costs cannot be attributed just to the narrower selection.
A shorter failure transcript did not remove a model response in these attempts.

Owner notes/requirements, all other supplied files, installed resources, HEAD and
captured index bytes/modes are preserved. Only a's authorized guard and new native
tests/support change. Those final inventories and captured Git boundaries are not
proof about every transient action or external effect.

Before model timing, native fixture controls produced the expected six-method
correct pass and three actual pending-state failures on the broken implementation.
Four synthetic scheduler/packaging controls passed from a fresh Git-free archive.
These are author validation, not model evidence. No author tests or source edits
ran during the four model sessions.

Retire this unchanged candidate. The existing native-capture and full regression
requirements remain. Do not promote smaller output as whole-task savings, retry for
a favorable pair, or relabel historical integration06. The all-eight goal is unmet.

한국어: 수정 전 재현 범위를 좁히는 후보는 채택하지 않는다. 실제로 결함 과제에서
수정 전 1개 검사를 실패시키고 수정 후 전체8개를 통과했지만, 두 과제 모두 누적
토큰이 늘었다. 합계 토큰은16.30%, 시간은0.35% 증가했고 모델 응답도 각각1회
늘었다. 정상 코드 과제는 두 실행 모두 구현을 보존했고8개 검사를 통과했다.
시나리오 구성과 추가 탐색·검사에는 차이가 있다. 실패 출력이 줄었다는 사실을
같은 작업의 토큰 절감으로 해석하지 않는다. 기본 스킬·설치본·공개 수치는
유지하며, 전체8개 품질·토큰·시간 목표는 아직 미달이다.
