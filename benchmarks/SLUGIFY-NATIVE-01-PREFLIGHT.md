# Slugify native transfer preparation — 2026-09-21

**Author preflight only. No model sessions or efficiency claim.** Helper resource
`a7dcbd8`. This prepares evaluation of the [existing-test recipe correction](AUDIT-NATIVE-RECIPE-02.md)
on a different project after [dateutil](DATEUTIL-NATIVE-01.md) showed adoption but
increased total tokens. A frozen model task/schedule is still required.

## Selection and provenance

History/protocol search found no preceding slugify or Sorted Containers audit
experiment. Sorted Containers v2.4.0 (`a1f52d6713dd2c2713a881d4f4d86ed68ff71cab`)
was inspected first, but its relevant tests are pytest functions, not native
unittest methods. No model calls or source adaptation were made for that candidate.

Selected upstream is [python-slugify v8.0.4, immutable revision
f85f9488520148d5f6899b5639199882b605e30a](https://github.com/un33k/python-slugify/tree/f85f9488520148d5f6899b5639199882b605e30a).
Keep all six package files (including `py.typed`), unchanged `test.py` and MIT
`LICENSE`. Fixed Git blob identities and checkout revision are checked before
execution. These are complete selected files, not extracted functions or rewritten
tests. Source is fetched into ignored local storage, not vendored by this checkpoint.

A separate ignored Python3.11 environment installs only `text-unidecode==1.3`
for the runtime dependency. The frozen dateutil environment is untouched.
No network, installation or model calls occur inside the preparation script:

```sh
/path/to/venv/bin/python -B benchmarks/preflight_slugify_native_01.py \
  --checkout /path/to/slugify-checkout \
  --output /path/to/new-preflight.json
```

Output creation is exclusive. Temporary projects are under `benchmarks/local-runs`
and removed after execution. [Retained observations](results/slugify-native-01-preflight.json)
include native assertions, dependency/interpreter identity and helper evidence.

## Genuine assertion controls

Selected upstream methods: `TestSlugify.test_non_word_characters` and
`test_max_length`. Witnesses: `test_custom_separator` and `test_save_order`.
All test bodies remain unchanged. Deliberate author faults are confined to
`slugify()`; they are not claims about bugs in the upstream release.

| Variant | Non-word characters | Max length | Custom separator | Save order |
| --- | --- | --- | --- | --- |
| Original | Pass | Pass | Pass | Pass |
| Omit final custom separator conversion | Pass | Pass | Assertion failure | Pass |
| Pass False instead of requested save_order to truncation | Pass | Pass | Pass | Assertion failure |
| Omit requested truncation | Pass | Assertion failure | Pass | Assertion failure |
| Equivalent `0 < max_length` comparison | Pass | Pass | Pass | Pass |

Twenty direct native unittest processes establish that matrix. Failures contain
actual differing string values, not support/import errors. Note that omitted
truncation also fails the save-order witness; do not misattribute that failure
to the independent save-order fault.

The production helper separately uses five batch entries: the two selected
methods as a suite against each of three faults, then the appropriate existing
witness against each surviving-gap fault. One correct selected suite is reused
twice; each mutant executes. The two witnesses have separate correct/faulty
pairs. Eight native processes execute12 methods and reproduce the required
outcomes. Same-process prechecks verify the actual test module's imported
`slugify` function binding to the copied implementation. Native assertions,
suite counts, original bytes/modes and owned scratch removal are checked.

**28 native processes /32 method executions total; zero model sessions.**
This is setup/correctness evidence, not a measured token/time saving. No complete
upstream suite, hosted validation, blind holdout or all-eight result is claimed.
The first preflight execution passed without fixture repair. Offline source
identity tests pass on Python3.9/3.11: original bytes accepted, modified bytes,
wrong revision and same-content symlink rejected.

## Next comparison gate

Use prior resource `387c53b` versus candidate `a7dcbd8`, plus a contemporary
no-skill control, to isolate the recipe change. Freeze task criteria, interpreter,
resources, schedule and limits before execution. Do not force helper adoption or
include author patch answers in the task. Keep every scheduled attempt and all
discovery/setup/repair costs. Existing upstream witnesses are available to every
arm. This task exercises existing-witness routing in a root package, not `src/`
layout guidance. It is an author-inspected development case, not independent
blind validation. Dateutil's adverse result and the featured graph remain intact.

한국어: 다른 실제 프로젝트의 원본 테스트로 정상·동등 코드와 결함3종의 결과를
검증했다. 직접 실행과 스킬 도구 결과가 일치하고 복사본 정리도 확인했다.
아직 모델 비교는 하지 않았으므로 실행 횟수를 토큰·시간 개선 수치로 사용하지
않는다. pytest 후보를 unittest로 바꿔 끼우지 않고 원래 unittest인 과제를 골랐다.
