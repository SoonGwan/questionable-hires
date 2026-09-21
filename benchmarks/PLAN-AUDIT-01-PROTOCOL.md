# Dependency-plan audit01 — fresh authored transfer task

2026-09-21. Prepared after `0a7256e`, before model execution. This new authored
dependency-planner fixture differs from the exposed cachetools task; it is still
author-selected, synthetic and unblinded, **not independent holdout evidence**.
No third-party source or upstream bug claim is involved.

## Frozen contract and author controls

`build_plan.plan` takes a dict of unique string IDs to lists of unique prerequisite
IDs present as keys. Return all IDs once, prerequisites before dependents, with
any valid independent-node order. Empty graph returns[]; cycles raise ValueError
with the specified message. Caller dict/lists must survive both success and error.
Concurrency, invalid inputs and large-graph speed are outside this contract.

Audit two existing methods: chain checks cardinality/membership but not order or
input preservation; cycle checks the actual error. Three isolated regressions:
reverse successful output, clear caller lists after constructing internal sets,
and return partial output instead of raising on a cycle. Author correct and
equivalent variants pass all three existing tests plus focused witnesses.
Each fault has an actual assertion-failing witness, not an import/setup error.
The six selected fault/test outcomes are five passes and one detected cycle fault.
Preservation-on-cycle checks distinguish a mutation assertion failure from the
separate missing-ValueError failure. Author patches/witnesses are never model inputs.

Two requests use identical initial files:

1. Audit the six outcomes and suggest concrete missing assertions. Extra execution
   is allowed, not a scoring failure, and remains in complete task cost.
2. Same audit, plus actual correct/faulty stronger-assertion verification for order
   and input preservation on acyclic and cyclic graphs. Unexecuted suggestions
   cannot fulfill this additional request. Original test bodies remain unchanged;
   extra checks belong in disposable project-local copies that must be removed.

`plan_audit_cases.py` defines five/six model-visible obligations before execution.
Its native preflight is retained at
[plan-audit-01-preflight.json](results/plan-audit-01-preflight.json).
Python3.9/3.11 fixture checks pass. Preparation is not a model result.

## Intended six original sessions

Freeze a runner and prepared manifest before any launch. Compare no-skill,
prior Con Artist`740948e`, current Con Artist`a3dee3b` (entry change`e17e13d`).
Only this skill is installed in the skill arms; helpers are unchanged between
prior/current. GPT-6 Astra medium,360 seconds/cell,n=1,serial, no heavy concurrent
author tests. Order: proposal baseline→prior→current; verified current→prior→baseline.
Native tool choice/grouping are unrestricted; no required helper use.

Reject task/resource/settings drift and duplicate execution. Persist originals;
retain every scheduled cell, timeout, repair and adverse result. Stop on account
limits without substituting another attempt. No favorable retry or exclusion.

Review semantic fault locality, copied runtime bindings, unchanged native test
bodies, actual assertion paths, reused observations, final answers, scope,
original bytes/modes and owned-copy cleanup. The verified request needs actual
stronger normal passes and intended fault failures for all three obligations;
cycles must still raise while the preservation assertion detects input mutation.
Shell success, model statements or later author replay are insufficient evidence.

Report each request/arm separately with full input+output tokens (cache once),
process wall time, native process counts, extra work and actual skill exposure.
A useful transfer signal is less optional work on proposal-only while keeping
required verification, without token/time regressions. No favorable threshold is
guaranteed; lower cost with weaker evidence is not a win. n=1, shared host/cache,
fixed order and this small authored project limit conclusions. Do not promote
this screen to all-eight superiority, release approval or the featured graph.

한국어: 새로 작성한 의존성 계획 과제로 제안과 입증의 구분을 확인한다. 기존
캐시 사례 재사용은 아니지만 작성자 선정·소규모 합성 과제이므로 독립 평가라고
부르지 않는다. 정상·결함 대조와 순환 오류 때 입력 보존까지 실제로 확인했다.
6회 실행 전 입력·기준을 고정하고 불리한 결과나 추가 작업도 모두 보존한다.
