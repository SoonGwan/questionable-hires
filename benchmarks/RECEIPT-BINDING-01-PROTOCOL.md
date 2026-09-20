# Receipt binding transfer pilot 01 — frozen before model execution

2026-09-21. Two authored tasks, three conditions, one session per condition/task:
six fresh serial sessions, GPT-6 Astra medium, 360 seconds each. This tests a
capability-gap intervention, not overall superiority of the eight skills.

## Conditions and fixed order

- Baseline: no project skill installed by the runner.
- Old: Receipt resources from `ba6fedd`, before module-binding support.
- Current: Receipt resources from `253273d`, with module-binding support.

Order: dynamic baseline → dynamic old → dynamic current → ordinary current →
ordinary old → ordinary baseline. Use `run.py --case <id> --cases-file
benchmarks/receipt-binding-cases-01.json --arms <baseline|skill> --repeats 1
--jobs 1 --seed 0 --timeout 360 --model gpt-6-astra --effort medium
--persist-session`, distinct output directory for every cell, immutable extracted
resource roots. Old/current both use the runner's `skill` arm; directory condition
labels, resource revisions and hashes distinguish them. Baseline uses the current
resource root only as a runner input; verify actual exposure from original records.
No retry, replacement, exclusion, model-visible repair or candidate edit between
cells. Stop remaining work on an account limit; preserve all scheduled outcomes.

## Task and controls

`receipt_binding_case.py` authored the frozen JSON. It is not a real repository
issue, independently selected holdout or untouched production project. Assertions,
implementation history, task and criteria are identical across loader forms;
only current test module loading differs. Dynamic loading uses a module object
not registered in `sys.modules`; ordinary loading uses an import alias.
The behavior contract explicitly requires decimal half-cent ties away from zero.

Each task requires identical current four-test bytes/identities on both revisions,
real before failures and after results, full revision IDs, same-process exact
copy-local test-bound module evidence, original byte/mode/Git preservation and
scratch cleanup. All requirements are model-visible. Helper adoption is optional;
custom native verification is equally acceptable. No required output format,
implementation recipe, helper-specific API or hidden criterion is supplied.

The preflight uses an author-only bootstrap, not a model-visible solution. Both
prepared projects show the two exact positive/negative midpoint assertion failures
before, other controls pass, and all four pass after. Native paths, test identities,
exit codes and unchanged original inventory are checked; owned copies removed.
Retained `receipt-binding-preflight-01.json` is author evidence, not model evidence.
The ordinary-loader task is a transfer/control condition, not proof that the
intervention can only affect dynamic loading; exact bound-module checks may help
both. Do not describe any favorable difference as isolated causal attribution.

## Review and decisions

Review every frozen criterion against original tool output, final snapshots/modes,
native identities, revision/path evidence and cleanup. Reconcile response-level
input/output/cache counters, inspect initial skill exposure privately, retain
capture gaps and repairs. Never publish private initial instruction text.
Report per-cell tokens (cached input counted once), wall time, response count,
success/scope and helper adoption. Compare current to both old and baseline.
Lower cost with missing obligations is not accepted improvement; time-only gains
with more tokens remain mixed. n=1 per cell, shared host/cache, authored related
tasks and order effects prevent broad percentage claims. Do not tune on these
tasks after observing results or promote them to the featured chart.

한국어: 직접 작성한 두 과제에서 무스킬·이전 Receipt·개선 Receipt를 총 6회
비교한다. 실제 이슈나 독립 선정 테스트로 표현하지 않는다. 도구 사용을 정답으로
요구하지 않으며 같은 검증 의무와 원본 보존을 적용한다. 불리한 결과·추가 작업·
출력 누락도 남기고, 한 번씩의 비교를 전체 성능 향상이나 대표 그래프로 승격하지 않는다.
