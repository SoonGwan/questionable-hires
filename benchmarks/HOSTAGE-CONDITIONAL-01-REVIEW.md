# Conditional Hostage 01 — rejected after full review

2026-09-21. Launch `1b26f9d`; prior/candidate resources `a1f420e`.
[Frozen protocol](HOSTAGE-CONDITIONAL-01-PROTOCOL.md),
[all six original attempts](results/hostage-conditional-01/run.json),
[criterion and capture review](results/hostage-conditional-01/comparison.json).
Production and the featured benchmark remain unchanged.

## Outcomes and cost

| Task | Arm | Criteria met | Task success | Total tokens | Wall seconds | Final native tests |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| Selection | Prior | 5/5 | Yes | 90783 | 54.256 | 7 passed |
| Selection | Baseline | 5/5 | Yes | 62605 | 43.651 | 6 passed |
| Selection | Candidate | 5/5 | Yes | 88901 | 54.622 | 7 passed |
| Shared fetch | Candidate | 4/5 | No | 117980 | 107.225 | 6 passed |
| Shared fetch | Baseline | 5/5 | Yes | 122875 | 121.619 | 7 passed |
| Shared fetch | Prior | 3/5 | No | 123861 | 118.823 | 8 passed |

Tokens include cached input and output, every response, repair and resource read.
Native-test counts are recorded model-session outcomes, not comprehensive contract
success. All six attempts completed without timeout/account limit. No repeats or
excluded attempts. Two authored synthetic tasks, n=1, fixed order, shared host/cache
and unblinded author review do not establish causal or general performance.

The conditional guide was read for async work and not for the synchronous task.
Routing worked, but this alone did not satisfy the adoption gate. The candidate's
async cost was lower than prior/baseline while a required behavior was wrong.
Synchronous candidate cost still exceeded baseline. No aggregate saving claim.

## Review and newly exposed boundary

All selection deliveries preserve None/empty/one-shot iterable/zero-ID semantics,
archive controls, stable duplicate order, object identity and original inputs.
Their native assertions exercise the delivered local implementation.

All async deliveries shield the actual shared fetch, let late callers join active
work after cancellation, observe orphan failures, preserve result/error identity,
and test independent keys with bounded waits and owned cleanup. However, prior and
candidate treat a completed task awaiting its cleanup callback as active work.
A caller scheduled in this window receives the previous completed result instead
of starting a fresh fetch. Baseline checks `task.done()` and handles the boundary.

The task's frozen criterion 3 already forbids completed-result caching. The
[post-run author probe](probe_completed_fetch_gap.py) and
[separate observations](results/hostage-conditional-01-author-gap.json) therefore
make this criterion fail for both skill deliveries. The frozen author preflight
reference has the same omission: its green checks were incomplete. It remains
unchanged, and the original model outputs are not patched or rerun.

Prior's final answer explicitly says completed results are not cached. This is
also incorrect, so report criterion 5 fails for prior. Its scope is nevertheless
preserved; `scope_pass` is recorded separately, not inferred from that compound
criterion. Candidate reports its genuine native-test results without the explicit
no-cache claim. Neither receives full task-success credit.

## Failures, evidence and preservation

Async candidate first had one failing retained-reference assertion; prior had two.
Both removed cancelled-caller references retained by their test harness and then
passed. Baseline first passed seven tests, strengthened its abandoned-failure check
with weak-reference collection, observed one failure, corrected retained caller
references and passed again. These are original attempts, not author repairs, and
all their costs and outputs are included.

All 28 native shell outputs match the original same-session capture exactly; none
are unresolved. Initial existing test methods, AGENTS instructions, file modes,
repository HEAD and installed resources are preserved. Saved pre-collection index
entries match the initial tree; a pre-session binary index was not captured.
Delivered tests import the actual local modules, with no replacement implementation
in their assertions. Export includes source, edits, answers, original tool records,
usage and resource-exposure evidence. Private initial instruction text and private
rollout files are excluded; the public evidence privacy-pattern scan passes.

## Decision

Reject this candidate for production promotion. Keep both the unfavorable model
outcomes and the author-preflight limitation visible. Do not tune/repeat these
exposed cases into a favorable replacement or overwrite historical charts. A future
change needs a distinct hypothesis and fresh transfer evidence; this result does
not establish an all-eight gain or readiness for a performance-led release.

한국어: 조건부 안내를 읽는 분기는 작동했지만 후보를 채택하지 않는다. 완료 직후
다시 호출되는 경계에서 기존 스킬과 후보 모두 요구사항을 놓쳤고 무스킬 구현은
통과했다. 작성자 사전 대조 코드에도 같은 누락이 있었다. 테스트 통과 수와 실제
요구 충족을 구분하고 실패·수정 비용을 모두 공개했다. 배포 스킬과 대표 그래프는
변경하지 않으며, 이 결과를 전체 성능 향상으로 홍보하지 않는다.
