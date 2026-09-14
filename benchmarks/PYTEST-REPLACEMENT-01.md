# Native pytest replacements and source-archive repair — 2026-09-15

This is local compatibility/distribution evidence, not a model comparison.
Runtime capability remains `07a2575`; follow-up test/distribution source `df799cf`.

## Native pytest behavior

Three new tests run against existing Python **3.9.6 / pytest 8.3.4** (3.149s).
They use the real CLI/runner, an autouse fixture required by the implementation,
a two-value parametrized fixture, normal assertion rewriting, and copied pytest
configuration with warning errors. Tests are not pre-imported by the helper.

- Same-path proposed assertions: original correct/faulty checks and improved
  correct checks each pass both cases; improved faulty checks fail both with
  actual `[] == ['first']` assertion diagnostics, not missing fixtures.
- Syntax failure in proposed tests: correct probe exits 2 and is incomplete;
  there is no subsequent mutant-probe result to credit as fault detection.
- Changed `conftest.py` replacement: a new correct probe executes, the original
  test baseline alone is reused, and the mutant reports the changed parameter.
  Seven actual check processes execute across that two-entry batch.

The new tests explicitly skip when pytest is unavailable in the selected Python.
`requirements-dev.txt` now includes the tested `pytest==8.3.4`, so both existing
CI jobs' requirements-install step covers them. This is a configuration change,
not a claim that hosted CI has already passed. No host dependency install occurred.

## Discovered source-archive regression

The previous `32456fc` source archive had no ignored `benchmarks/local-runs`.
The seven new unittest replacement tests depended on that directory in `setUp`,
so the focused archive run produced **seven FileNotFoundError setup errors**.
These were test-support errors, not seven production defects or detected mutants.
Earlier full-worktree passes remain true but did not prove source-archive support.

Both replacement test modules and the retained store replay now allocate owned
temporary directories under the shipped `benchmarks` directory instead. They
remove their own temporary directories; they do not create a hidden global temp
configuration, rely on ignored state, or mutate original source.

A fresh unmodified `git archive df799cf` (no `.git`, no ignored runs, no file
overlays) passes all **10 focused replacement tests in 4.245s**, using the existing
pytest environment. Its author store replay also completes the four expected
native phases with two actual content assertion failures in the faulty improved
phase, unchanged seven original files and confirmed cleanup. This is author
execution, not a new model attempt or a rewritten earlier benchmark.

## Full archive run is not green

The same `df799cf` archive's full suite discovers **641 tests** and ends with
**nine failure entries in 101.218s**. It runs under the existing pytest virtualenv;
existing host PyYAML is exposed through process-local PYTHONPATH, without package
installation. Do not generalize the focused ten passes into a full archive pass.

Three historical-fixture comparisons mistake the containing checkout's available
commits for the archive's own history. `git rev-parse --show-toplevel` inside this
archive resolves to its containing worktree, not the archive root. The checks only
ask whether a commit exists; subsequent relative-path extraction gives different
content. This nested-archive history assumption needs correction, not altered
frozen fixtures. The existing CI archive job uses a temp root outside checkout;
that different location has not been reverified in this follow-up.

Six failure entries come from Receipt's user-site hook fixture expectations
(one configured-user-hook case, hook order, external-import fixture and three
hook-error subcases). This interpreter reports virtualenv true and
`site.ENABLE_USER_SITE == False`; its direct hook preflight also lacks the expected
marker. The diagnostics point to unavailable fixture activation, not proof that
the Receipt runtime ignored an active hook. These assumptions still need review
and regression correction; do not silently skip them or claim full virtualenv
compatibility. All adverse results remain part of this checkpoint.

한국어: 실제 pytest의 자동 fixture·매개변수화·assertion 재작성·수집 오류 처리를
검증했다. 추가로 이전 커밋의 깨끗한 압축본에서 새 검사 7개가 로컬 전용 폴더
때문에 시작하지 못하는 회귀를 발견했다. 배포본에 존재하는 경로 아래로 임시
폴더를 옮긴 뒤 새 압축본에서 관련 10개 검사와 실제 저장 테스트 재실행이
통과했다. CI용 개발 의존성에도 pytest를 추가했지만 호스팅 CI 통과나 모델
효율 개선을 주장하지는 않는다.
전체 압축본 검사는 641개 실행에서 실패 항목 9건으로 끝났다. 상위 Git 저장소를
자기 이력으로 오인하는 검사와 user site 비활성 가상환경에서 훅 활성화를 기대하는
검사의 가정을 추가로 검토해야 한다. 관련 10개 통과를 전체 배포 검증으로
확대하지 않고 미해결 실패를 그대로 남긴다.
