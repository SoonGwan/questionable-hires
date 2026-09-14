# Project-owned history and reachable hook fixtures — 2026-09-15

Follow-up to the [nine-entry archive failure](PYTEST-REPLACEMENT-01.md).
This corrects benchmark/test assumptions, not skill behavior or measured model
performance. Frozen fixtures and historical observations are unchanged.

## History ownership (`2d7ec8e`)

Pinned packaging export and frozen Friday preparation now require project-local
Git metadata and a resolved Git worktree root equal to the requested project.
An archive nested inside a checkout can no longer borrow parent history. Friday
refuses before creating output; packaging refuses instead of emitting an almost
empty fixture. Linked-worktree metadata files remain supported.

Two regression tests cover actual parent-Git discovery/refusal without output,
acceptance of a real owned checkout and mismatched root refusal. In the real
working checkout, three Friday and four packaging tests still pass. A fresh
unmodified `2d7ec8e` nested archive records three Friday tests with one explicit
history-only skip, four packaging tests with two history-only skips, and both
scope regressions passing. Archived behavior/scheduling checks continue to run.
Those three skips are unavailable own-history comparisons, not passing evidence.

## Reachable startup hooks (`6e99847`)

The active-hook fixture first queries the selected interpreter's native user-site
activation. When an ordinary isolated venv disables it, the tests create an owned
temporary runtime with `system_site_packages=True` and `with_pip=False`, then
verify activation before placing their hook fixture. No host/selected-venv config
is edited and no dependency is installed. The owned runtime is removed afterward.
Existing order, module identity, external-import rejection, exception handling,
child behavior and before-fail/after-pass assertions remain active.

The configured-user-hook check separately follows native activation: an active
hook still must be reported as incomplete; an inactive hook must remain inactive
while actual native before/after tests execute. Explicit PYTHONNOUSERSITE coverage
remains. No hook checks are skipped merely to turn a failure green.

Actual focused checks:

- Existing isolated Python 3.9.6 venv: four startup tests pass (1.688s), thirteen
  native-invocation tests pass (6.200s).
- System Python 3.9.6: four startup tests pass (1.617s), thirteen native-invocation
  tests pass (6.270s). Its controlled native user hook emits the expected startup
  warning while activation is queried; the helper's own incomplete result is
  separately asserted.

These are fixture/environment and source-distribution checks, not hosted CI or
20–30% model performance gains. Earlier full-archive failures remain visible.

The first full corrected `6e99847` archive run discovers **643 tests** and ends
with **two failures / three skips in 101.867s**. The previous nine failure entries
are absent. Two archive meta-tests still expected the old English skip reasons,
although their child processes returned success with the correct single skip.
They now assert the exact historical test's skipped result rather than prose;
native counts, successful child exit and behavior-test identities remain checked.
This intermediate failure is retained, not counted as a full pass.

## Fresh full archive verification (`b7b9da1`)

A new unmodified nested source archive passes the full suite: **643 discovered,
640 passed, three explicit history-only skips / 101.112s**. No `.git`, ignored-run
overlay, installed-package mutation or source overlays were supplied. It uses the
existing Python 3.9.6 / pytest 8.3.4 venv and process-local PYTHONPATH access to
existing host PyYAML, as in the earlier failed full run. All native hook tests now
execute successfully. The three skips are the own-history comparisons described
above, not credited as passes. This is local macOS archive evidence, not Linux or
hosted CI confirmation, and it does not establish model efficiency.

한국어 추가 검증: 새 `b7b9da1` 압축본 전체 검사에서 643개 중 640개 통과,
자체 이력이 필요한 3개만 명시적으로 생략됐다(101.112초). 앞선 실패 환경과 같은
기존 가상환경을 사용했고 원본 덮어쓰기나 의존성 설치는 없었다. Linux·호스팅 CI·
모델 성능 검증과는 구분한다.

한국어: 압축본이 상위 저장소 이력을 자기 것으로 사용하는 문제를 차단했다.
자체 이력이 없는 경우 이력 비교만 명시적으로 생략하고 실제 동작 검사는 유지한다.
사용자 site가 비활성인 가상환경에서는 활성 훅 검사를 별도의 테스트 소유 런타임에서
수행하며, 원래 가상환경의 비활성 동작도 따로 확인한다. 설정 변경·의존성 설치 없이
시스템 Python과 가상환경에서 관련 17개 검사가 각각 통과했다. 모델 성능 개선이나
호스팅 CI 통과로 확대 해석하지 않는다.
