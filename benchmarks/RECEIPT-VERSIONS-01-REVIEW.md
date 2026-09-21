# Receipt versions01: actual adoption, mixed resource costs

Reviewed2026-09-22. [Preparation and criteria](RECEIPT-VERSIONS-01-PREPARATION.md),
runner `f76aec0`; Receipt predecessor `efc1439`, current `e075bdb`.
Two correlated authored development requests, three conditions, one session per
cell: six serial GPT-6 Astra medium sessions. All completed; no timeouts, detected
limits, replacements, retries or exclusions. Explicit Receipt invocation is not
automatic-routing evidence. [Evidence index](results/receipt-versions-01/README.md).

| Request | Condition | Input + output tokens | Process seconds |
| --- | --- | ---: | ---: |
| Single historical version | Baseline |82,254|61.141|
| Single historical version | Predecessor |111,439|49.292|
| Single historical version | Current |68,000|64.346|
| Multiple historical versions | Baseline |84,218|68.999|
| Multiple historical versions | Predecessor |105,446|81.877|
| Multiple historical versions | Current |98,996|47.878|

Current versus baseline: single **tokens−17.33%,time+5.24%**; multiple
**tokens+17.55%,time−30.61%**. Summed tokens166,472→166,996 (**+0.31%**),
time130.140→112.224seconds (**−13.77%**). Versus predecessor: single
tokens−38.98%/time+30.54%; multiple tokens−6.12%/time−41.52%.
Original stored usage counters reconcile with CLI final usage in all six cells.
Input includes cached input once; reasoning is not added again to output.
These are process times, not billing or native-test speed measurements.

## Requested behavior and actual approaches

All six execute the unchanged six-test native suite on each requested revision
using the specified interpreter, with copied source imports in each native
process. Each requested revision executes once: two native processes for single,
three for multiple, in **every condition**. Actual outcomes match:

| Revision | Touching windows | Nested windows | Native result/exit |
| --- | --- | --- | --- |
| `HEAD~2` (multiple task only) | `[(1, 3), (3, 5)]` instead of `[(1, 5)]` | `[(1, 3)]` instead of `[(1, 10)]` |4pass/2fail, exit1|
| `HEAD^` | Pass | Same nested failure |5pass/1fail, exit1|
| `HEAD` | Pass | Pass |6pass, exit0|

Chain, disjoint, empty and input-preservation controls pass throughout. The
historical failures are actual assertions, not startup/collection errors. Full
commits, fixed-test hashes and copy-local imports are retained. Project source
bytes/modes/file set, installed resources and HEAD match original inputs; captured
before-model/pre-collector index bytes/modes match. Owned scratch is removed.
No out-of-scope command was observed except the explicitly supplied interpreter.

The two baselines and current/single construct custom `runpy` unittest runners
with assertion tracing/profiling. Predecessor/multiple constructs a three-version
native module runner with copy-local `sitecustomize`, verifies the test function
binding, and reuses the Receipt inventory function for preservation. It does
**not** run two pairwise comparisons or redundantly test current twice.

Predecessor/single uses the old pairwise helper. Current/multiple reads the guide
and helper implementation, then uses `additional_before` and module invocation
to capture all three versions with the new helper. This demonstrates adoption in
one authored case, **not a reduction in executed test count versus either arm**.
Current/single reads only the unchanged skill body, so its lower token count
cannot be attributed to the uninvoked new API. Both multiple skill cells read
the complete implementation; no causal saving from avoiding source inspection
is claimed.

The custom runners also trace passing assertion values, whereas helper runs
retain native failure values and passing test identities. Both meet the frozen
defect/control criteria; instrumentation and output volume are not identical.
Do not attribute all cost differences to the optional parameter.

## Capture and limitations

[Measurements](results/receipt-versions-01/measurements.json) include exact-body
exposure observations, original rollout hashes and complete tool-call/output
identity checks. Both baseline records have no observed exact Receipt body;
all four skill records contain body reads. This is not proof of absence of other
hidden context. Private initial instructions and raw rollouts remain local.
Redacted original tool records are retained separately from CLI records: some
CLI command outputs omit leading native output (notably current/single's old
version), while matching original tool output retains it. No author replay is
substituted for the original observations, and no missing prefix is inferred
from a final answer. The private source hashes identify the original evidence.

This is unblinded author review, n=1 per task/condition, shared host/cache, fixed
order and two variants of one small synthetic project. It does not establish
causality, robustness, independent generalization or broad quality superiority.
Preservation checks are endpoint observations, not proof against all transient
effects. Export pattern scan has zero findings; that is not a secrets audit.

## Decision

Keep the supported optional capability, but **do not promote an efficiency
claim or replace featured graphs**. Total token cost is essentially unchanged;
each task trades one metric against the other versus baseline. The broad20–30%+
goal remains unmet. Do not rerun these exposed tasks until favorable or force
helper adoption. Any next optimization needs evidence of avoidable work, not
generic instruction compression or removal of required assertions/provenance.

한국어:6회 모두 요청한 검증을 수행했고 다중 버전 기능도 실제 사용됐다. 하지만
기본 모델 대비 합계 토큰은0.31% 늘고 시간은13.77% 줄었다. 단일 과제는 토큰이
줄고 시간이 늘었으며, 다중 과제는 그 반대다. 이전 스킬과 기본 모델도 현재
버전을 한 번만 실행했으므로 실행 횟수 감소를 실측 성과로 주장하지 않는다.
전체 성능 향상이나 대표 그래프 교체 근거로 채택하지 않고 모든 결과를 보존한다.
