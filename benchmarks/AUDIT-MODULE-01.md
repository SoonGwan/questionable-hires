# Con Artist native unittest invocation — 2026-09-21

Parent `04bf934`. Capability validation, not a model efficiency experiment.

## Why this change

The prior helper only launched a Python `-c` bootstrap calling `unittest.main`.
The frozen planner tasks require `python -B -m unittest` from each copy root.
Thus the helper did not meet that invocation requirement, regardless of its
baseline-cache optimization. This does not prove the model's reason for not using
it. Neither the old tasks nor their recorded sessions/results are changed.

`invocation: module` now runs the actual module command. An owned startup adapter
preserves conventional interpreter customization, removes itself from child
lookup/environment, and wraps the real TestProgram execution to verify copied
imports/prechecks and retain completed-suite counts. It does not replace the CLI
with `unittest.main`. This is instrumented execution, not untouched startup.

Default bootstrap remains unchanged. The optional mode supports native test and
probe files, selected import roots, project guards and batch baseline reuse.
Mode changes invalidate cached correct observations. Inline assertion probes and
pytest reject the module mode; selected project startup customization is rejected
rather than overwritten. Custom runner identities and hostile observation-file
forgery are not supported. Native exits remain separately recorded when empty
suites or missing completion evidence map to incomplete status.

## Executed controls

`tests/test_audit_module_invocation.py`: all **12 methods pass** on Python3.11.16
(3.033s) and Python3.9.6 (2.603s), no skips. They exercise:

- Actual `unittest.__main__` identity and native argv, correct pass / real faulty
  `AssertionError: 0 != 1`, copied imports and same-process binding precheck.
- Native stronger probes, repeated baseline references, and eight alternating
  selections executing all eight mutants in ten processes.
- Empty/all-skipped suites, help-only, early zero exit, failed precheck and timeout.
- Cache invalidation between bootstrap/module, invalid mode/runner/probe rejection,
  rejection of project startup replacement, source-root and escaped-import checks.
- Interpreter site/user hooks running once in order, no adapter in child processes,
  and hook failure retained as incomplete rather than silent success.
- Built bundle from a path containing spaces, actual CLI execution and cleanup.
- The existing frozen planner fixture in a separate author-owned project: six
  native mutant checks yield `[0, 0, 0, 0, 0, 1]`, with two normal observations,
  all eight real `-m unittest` processes and original project inventory preserved.

The planner control is reused development evidence, **not independent validation**
or a new model session. Ten rather than sixteen checks in the alternating-selection
control demonstrates existing reuse working under module invocation; it is not
a measured model token/time reduction, and equivalent manual orchestration may
also reuse baselines. The native planner control itself needs eight processes,
not a saving over the already-efficient eight-process model implementations.

An intermediate fixture incorrectly expected argv to retain the `__main__.py`
path; Python rewrites it to `<executable> -m unittest`. Four initial test failures
were due to this expectation. A later source-root fixture initially retained the
old mutation target path and failed setup. Both author test mistakes were corrected
before the green results; no model attempt was excluded or replaced.

The intermediate audit-family run passed 101 methods (14.283s), build tests passed
13 (2.964s), and legacy mutation helper tests passed 80 (15.277s). Those checkpoints
precede the final planner-control method. Final whole-suite verification is recorded
separately when completed. Skill instructions remain unchanged at the entrypoint;
the conditional reference documents mode-specific limits.

First whole-suite run: 1,035 methods in176.773s, **one failure**, not a green run.
Standalone packaging invokes every advertised CLI script with `--help`; placing
the internal startup template under `scripts/` incorrectly exposed it as a CLI.
Moved that copied template to `assets/` and updated its lookup. The template is
still packaged and covered by actual installed/bundled execution controls; the
standalone CLI check is unchanged rather than weakened to ignore the failure.

Final checkout at `c258570`: **1,035 tests pass in175.415s**, no failures/skips,
Python3.11.16 (`python -B -m unittest discover -s tests`). The focused standalone
archive suite also passes all4 tests (1.125s), and the12 module controls pass again
(2.917s) after relocation. Repository validation, skill quick validation, whitespace
and featured localization checks pass. This does not establish hosted CI success,
an archive-wide 1,035-test invocation, model performance or public-release approval.

한국어: 요구된 `-m unittest` 방식에서도 복사본 출처 확인, 실제 테스트 결과,
보강 테스트와 배치 재사용을 제공한다. 내부 관찰 코드가 개입하므로 순수한
시작 과정과 동일하다고 주장하지 않는다. 기존 과제의 검증 코드를 재사용한
기능 검사이며 모델 비용 절감을 입증하지 않았다. 대표 그래프는 변경하지 않는다.
