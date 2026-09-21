# Dateutil native01 — frozen model comparison

2026-09-21. One verified-audit request on a selected unchanged dateutil source
tree at `1ae807774053c071acc9e7d3d27778fba0a7773e`. Three Astra medium sessions,
n=1, serial order prior/baseline/current,360s each, shared host/cache.
Prior resources `1fa230c`; current `387c53b`. Both have identical native helper
implementation; current changes entrypoint discovery and adds a native recipe.
Baseline has no installed task skill. This is development evaluation on an
author-inspected upstream subset, not a blind holdout or full-repository test.

Hypothesis: naming supported native execution and linking a complete recipe can
reduce custom orchestration through voluntary adoption. The prompt does not
name or require the helper; equivalent native execution is valid. Retain unused
helper results, inspection, repairs, extra work, failures and timeouts in cost.
The runner's common suffix calls prepared fixtures a "synthetic project";
task AGENTS explicitly identifies the unchanged selected upstream tree.

See [preflight](DATEUTIL-NATIVE-01-PREFLIGHT.md) for source identities, license,
dependencies, exact faults and direct/helper controls. Preparation repeats those
controls before freezing. Both selected tests, all six fault/test combinations,
same-process class bindings, correct controls, actual stronger assertions for
both surviving gaps, preservation and scratch cleanup are explicit model-visible
obligations. Existing upstream witness methods may be reused. No dependencies
may be installed or modified; all arms use the same scoped interpreter.

Five criteria are in the frozen case. Expected selected exits for independent
day-cap/strict-weekday/omitted-month faults are `[0,0]`, `[0,0]`, `[1,0]`.
Leap-year February-end and same-day Wednesday assertions must pass correct code
and genuinely fail matching faults, not error during setup. Exact author patch
strings and expected matrices are not appended to model inputs. Unchanged
upstream tests naturally contain witness examples available to every arm.

Freeze fixture, protocol, runner/test identities, interpreter, resource digests
and order before the first model call. Exclusive marker prevents reruns;
recognized account limits stop remaining scheduling without replacements.
No author tests run concurrently with timed cells. No candidate edits, repeat
selection, exclusions, post-hoc obligation changes or favorable-only promotion.

Review original tool evidence, initial skill exposure, actual native executions,
assertions, source scope and cleanup. Preserve private raw sessions; export only
reviewed/redacted records. Distinguish any capture gaps from author replay.
Report total input+output tokens (cached subset not added twice), wall time,
response counts and unequal work. A successful small checkpoint does not establish
all-eight20–30% gains and does not replace the featured graph.

한국어: 동일한 실제 소스 과제1개를 이전·무스킬·현재의3개 세션으로 비교한다.
도구 구현은 같고 안내만 다르다. 도구 미사용, 복구 비용과 추가 작업도 포함하며
정상·결함 판별과 원본 보존을 먼저 검토한다. 독립 평가나 전체 성능 향상으로
확대하지 않고 대표 그래프는 유지한다.
