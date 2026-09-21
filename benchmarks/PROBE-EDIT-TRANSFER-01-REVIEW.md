# Probe-edit transfer01: native success, no helper adoption or efficiency win

Reviewed2026-09-21. [Protocol](PROBE-EDIT-TRANSFER-01-PROTOCOL.md), launch`f2f657a`;
predecessor Con Artist`23f06d2`, current`aed8a27`, no-skill baseline.
Two correlated authored tasks, one session per condition/task, six serial Astra
medium cells. All completed, no timeout, account-limit stop, retry or exclusion.
Original contexts confirm actual model/effort. [All evidence](results/probe-edit-transfer-01/README.md)
and [measurements/preservation checks](results/probe-edit-transfer-01/measurements.json)
retain every condition, not just the favorable token comparison.

| Test-file size | Condition | Input + output tokens | Seconds |
| --- | --- | ---: | ---: |
| Full upstream file | Baseline |92,596|86.041|
| Full upstream file | Predecessor |79,871|107.355|
| Full upstream file | Current |85,305|143.934|
| Prefix control | Baseline |73,637|79.142|
| Prefix control | Predecessor |81,225|72.969|
| Prefix control | Current |81,321|79.728|

Current versus baseline: full **tokens−7.87%,time+67.29%**; prefix
**tokens+10.43%,time+0.74%**. Current versus predecessor: full
**tokens+6.80%,time+34.07%**; prefix **tokens+0.12%,time+9.26%**.
Input includes cached input once; reasoning is not added again to output.
Original usage counters agree with emitted totals. Process wall time is not
native-test time or a billing estimate. Shared host/cache and fixed order remain
confounds; these single observations do not establish causal regressions either.

## Actual requested work

All six execute four actual native pytest processes in fresh project-local copies,
without reusing observations. Every session preserves the requested selected test,
parameterization and native arguments, verifies copy-local package/test paths and
the executing test's Specifier binding, and reports actual outcomes:

| Phase | Native result | Exit |
| --- | --- | ---: |
| Existing test / correct code |9pass|0|
| Existing test / specified fault |9pass, survives|0|
| Strengthened test / correct code |9pass|0|
| Strengthened test / specified fault |9assertion failures|1|

The proposed change is the same one-line replacement in every session:
`Specifier(specifier)` → `assert str(Specifier(specifier)) == specifier`.
Faulty values are empty strings rather than each of the nine supplied strings;
correct strings equal the supplied values. Failures are actual assertions, not
setup/collection errors. Command code and original output were reviewed, not just
the final answers. The baseline succeeds too; this is not a quality advantage.
The selected constructor smoke test was never claimed to cover the full upstream
suite's serialization behavior; later unselected tests already exercise it.

## What the new resource did not do

Both predecessor sessions and both current sessions read the identical top-level
skill body. Neither reads a support guide or invokes `audit.py`; every session
writes a custom pytest bootstrap. Thus `probe_edits` is unused and its shorter
author-preflight JSON is **not a measured saving in this experiment**. Original
baseline records have no observed exact skill body, not proof of absent hidden
context. Full resource manifests verify that each condition had its pinned files.

Instrumentation differs despite equivalent requested assertion obligations:

- Baseline/full prints call outcomes and string values; predecessor/full prints
  provenance and values at collection. Current/full emits individual setup,
  call and teardown reports as well as values, yielding much larger native output.
- Prefix skill sessions also emit individual phase reports; predecessor includes
  failure text in those records. Prefix/baseline emits aggregate report counts.
- Current/full and prefix/baseline disable plugin autoload and remove
  `PYTEST_ADDOPTS`/`PYTEST_PLUGINS` in child environments. Current/prefix disables
  autoload and removes `PYTEST_ADDOPTS`; predecessor cells and full/baseline do
  not make those same removals. They preserve the supplied project configuration
  and requested pytest arguments, but runtime handling is not identical across arms.

These differences cannot be silently attributed to the uninvoked helper or treated
as a controlled comparison of its API. Nor does this justify removing required
same-process provenance or assertion evidence to manufacture lower costs.

## Capture and preservation

All21 original shell outputs reconcile with CLI records at equal exits; no missing,
duplicate or unmatched original calls/outputs and no unresolved capture matches.
Five last-command CLI records omit leading output: they match an exact nonempty
suffix of their complete original output. Original records retain the beginning;
no author replay fills a gap. The predecessor/prefix final output matches exactly.
Private initial instructions/raw rollouts and binary indexes remain local.

All six original source/test/license bytes and modes match the task inputs;
no extra project files remain. Installed resources match frozen copies and their
before/after manifests. HEAD and before-model/pre-collector index bytes/modes
remain identical. In-model inventories and cleanup assertions also pass. These
observations are not atomic snapshots or proof of every transient effect.
No out-of-project command was observed except the explicitly supplied interpreter.

The first author export attempt used system Python instead of the frozen
preinstalled interpreter, so the environment-equality guard stopped it before
creating exports. Using the original interpreter allowed export; no model rerun,
source correction or frozen-record rewrite occurred. Capture-stage
`quality_review: Pending...` fields remain historical; this is the subsequent review.

## Decision

No efficiency promotion. The new optional API has native correctness evidence,
but no demonstrated model adoption or cost benefit here. Do not force its use,
repeat these exposed tasks until favorable, or interpret lower full-task token
usage versus baseline while hiding the elapsed-time increase. Keep the negative
six-cell outcome alongside the author preflight. No featured graph or headline
performance claim changes; broad20–30%+ improvement remains unproven.

한국어:6회 모두 실제 네 단계 검증을 완료했지만 현재 스킬은 이전 스킬보다 두
과제 모두 토큰·시간이 늘었다. 기본 모델 대비 큰 파일의 토큰은 줄었으나 시간은
크게 늘었고, 작은 파일은 둘 다 늘었다. 새 부분 수정 기능은 사용되지 않았으므로
입력 JSON 감소를 실측 성과로 볼 수 없다. 불리한 결과와 환경·출력 차이를 보존하며
대표 그래프나 전체 성능 향상 주장으로 채택하지 않는다.
