# Dateutil native-audit transfer preparation — 2026-09-21

Status: **author preflight only; no model sessions, no efficiency claim**.
Helper resource: `387c53b`. This prepares a different real-source task after
the [edit audit](EDIT-AUDIT-01.md) did not establish helper adoption or savings.
Do not treat this preparation as a frozen model protocol or independent holdout.

## Source and reproducibility

Upstream is [dateutil 2.9.0.post0, immutable revision
1ae807774053c071acc9e7d3d27778fba0a7773e](https://github.com/dateutil/dateutil/tree/1ae807774053c071acc9e7d3d27778fba0a7773e).
Six complete unchanged Python files are selected: the `src/dateutil` package
initializer, `_common.py`, `relativedelta.py`, and the `tests` initializer,
`_common.py`, `test_relativedelta.py`. Keep upstream `LICENSE` and `AUTHORS.md`
alongside those files. This is a selected source tree, not the whole repository.
No upstream source files are vendored by this checkpoint. The preparation script
checks the checkout revision and fixed Git blob identities before executing code.

Use a dedicated Python3.11 environment with `pytest==8.3.5`, `six==1.17.0`,
`iniconfig==2.3.0`, `packaging==26.3`, `pluggy==1.6.0`. Pytest is an import
dependency of the upstream tests; actual execution here uses unittest.
An initial check of the existing development environment found `six` missing;
dependencies were installed only in a new ignored experiment-local virtualenv.
No source/test modifications were used to work around imports.

```sh
/path/to/venv/bin/python -B benchmarks/preflight_dateutil_native_01.py \
  --checkout /path/to/dateutil-checkout \
  --output /path/to/new-preflight.json
```

Output creation is exclusive. The script performs no network calls or model
calls. Its temporary project resides under `benchmarks/local-runs`, and is
removed after all checks. The checked-in [observations](results/dateutil-native-01-preflight.json)
retain assertions, native commands, dependency versions and redacted paths.

## Controls and outcomes

Both selected methods are unchanged upstream tests:
`RelativeDeltaTest.testNextMonth` and `testNextFriday`.
Author-selected faults are not claims about bugs in upstream dateutil.

| Variant | Next month | Next Friday | Targeted unchanged upstream witness |
| --- | --- | --- | --- |
| Original | Pass | Pass | All three pass |
| Cap resulting day at 28 for every month | Pass | Pass | Leap-year February end fails: February28 versus29 |
| Force same-weekday selection to next week | Pass | Pass | Same Wednesday fails: September24 versus17 |
| Ignore relative-month addition | Fail | Pass | Next month fails: September17 versus October17 |
| Equivalent explicit month addition | Pass | Pass | All three pass |

The direct native controls run both selected tests plus all three witness
selections on every variant:25 processes. Duplicate `testNextMonth` selection
is intentional (selected coverage and targeted witness); this is not25 unique
test methods. All failures are actual `AssertionError` outcomes, not import or
support errors. These direct controls do not independently prove in-process
binding; their environment points at the selected local source tree.

The production helper separately runs six fault/selection pairs with `src`
import roots, actual `python -B -m unittest`, and a same-process identity check
of the test module's imported `relativedelta` class. It executes two correct
observations and six mutants:8 processes. Four later correct observations are
explicit references to the first two, not new executions. Results match the
direct selected-test matrix; native suite counts are1 with no skips; preserved
original file bytes/modes and owned-copy removal are checked.

**33 native executions total; zero model sessions.** The helper's8 executions
are not a whole-task performance result or an established saving against any
model baseline. The native witnesses were tested directly, not through helper
probe mode in this preparation. No stronger-assertion capability is newly claimed.
The preparation passed its first execution without fixture repair.

Offline source-identity regression checks:3/3 pass on Python3.9 and Python3.11
(original accepted, modified bytes/revision rejected, symlink rejected).
Repository validation, featured synchronization check and whitespace check pass.
The evidence privacy-pattern scan has no hits; it is not a security certificate.
No full-suite or hosted-CI rerun is claimed at this checkpoint.

## Next gate

Before any model call, freeze the model-visible task, scored obligations,
permitted dependency/interpreter setup, resource snapshots, order and settings.
Use `1fa230c` versus `387c53b` to isolate discovery changes while holding native
helper capability constant; retain a contemporary no-skill control. No forced
helper use, no author witness answers in the task, no discarded unfavorable
attempts. One selected upstream project is not broad generalization. These
author-inspected cases are development evaluation, not a blind holdout.

한국어: 실제 dateutil 원본 테스트와 스킬 도구의 실행 결과 일치를 확인했다.
정상·동등 구현과 의도적으로 만든 결함을 구분했고 임시 파일 정리도 확인했다.
모델 비교는 아직 실행하지 않았으므로 토큰·시간 개선이나 독립 평가 결과로
주장하지 않는다. 대표 그래프와 두 언어의 성능 수치는 변경하지 않았다.
