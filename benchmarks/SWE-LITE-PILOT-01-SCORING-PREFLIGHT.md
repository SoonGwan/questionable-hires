# Scoring preflight: offline environment is not ready

2026-09-21, parent`0f534b3`. Two fixed external issues, no model sessions and no
skill edits. This author check executes the frozen dataset evaluation scripts
against original and gold-patched source in separate original official images.
Neither task is accepted as ready for the baseline/skill comparison.

## Observations, including unsuccessful preparation

[Attempt01 aggregates](results/swe-lite-pilot-01-scoring/attempt-01.json): all four
containers stop before tests because copied private files are unreadable; original
variants exit126, gold variants exit128. No test labels are observed. This is not
four model failures or a scored task result.

Attempt02 keeps host input files0600 in a0700 directory, but transfers their bytes
via an archive with explicit readable modes inside each isolated grader container.
Same images, source, patches, scripts and test lists; no favorable case replacement.
[Aggregate observations](results/swe-lite-pilot-01-scoring/attempt-02.json):

| Project / source | Required fail-to-pass group | Required pass-to-pass group |
| --- | --- | --- |
| pytest original |1 failed|77 passed|
| pytest gold |1 passed|77 passed|
| Requests original |8 failed|81 passed /52 failed|
| Requests gold |8 failed|81 passed /52 failed|

All labels in these two groups are observed; no missing/error/skip labels are
silently credited as passes. Nevertheless **both environments fail preflight**:

- pytest's evaluation script attempts an isolated editable reinstall. Both
  variants cannot obtain `setuptools>=40.0` offline. Subsequent tests run against
  the existing editable environment and show the expected transition, but that
  does not establish successful declared setup or complete scoring reproducibility.
- Requests reinstall succeeds, but both variants retain60 failed tests and many
  DNS-resolution errors with networking disabled. The gold patch cannot satisfy
  its regression contract in this environment. Do not remove52 controls, count
  those failures as skill defects, or replace the selected task to improve a score.

Every attempt02 container exits0 because the evaluation scripts continue after
test/install failures and finish with a successful Git checkout. **Shell exit0 is
not a passing grade.** Decisions use bounded native output and explicit label
status counts, not the final exit code. No performance graph changes.

## Execution and evidence boundaries

The [executed attempt02 driver](results/swe-lite-pilot-01-scoring/preflight-driver.py)
uses network-disabled, unmounted, capability-restricted disposable containers,
2GB/2CPU/256PID limits and a180-second command ceiling. Four cells per attempt,
serial. All eight containers are terminal; no timeouts or live model work remain.
Official gold source is applied only in grader containers. Raw logs contain
solution/test material and stay in ignored private storage; public aggregates
retain original log hashes instead of exposing those contents to later solvers.
No task row, gold patch, hidden-test label or raw evaluation script is exported.

Parsing uses unchanged AST-selected functions and TestStatus from official harness
revision`02e7a74ffd0b707aab73d203fe87bdc7c76afc8e`; parser source SHA-256
`cd56156414f8327221e525665ace9b184f7d73e83b272d9eb3f545fb17c2d9bc`.
Requests maps to `parse_log_pytest_options`, pytest to `parse_log_pytest`. The
unused TestSpec annotation is bound to `object`. Synthetic pass/fail/error/empty
log controls execute first. This is **not an execution of the complete official
grading harness**, an independent parser audit or a leaderboard submission.

The coordinator inspected evaluation command heads before heredoc redaction, which
exposed fragmentary test-source tokens, then inspected only redacted outer commands
and setup errors. Full solution patches were not displayed. Do not describe this
author investigation as blind; fresh solver sessions must not receive this context
or scoring artifacts. Public benchmark training contamination also remains unknown.

## Next gate

Reproduce required installation and test services without changing source/tasks or
dropping controls. Pin any added build dependencies/service runtime and preserve
these adverse attempts. Keep grader data inaccessible to the solver-facing runtime;
same-process package provenance and complete access review are still pending.
Only then freeze model execution settings and launch the four-cell comparison.

한국어: 채점 환경 확인에서 pytest는 원본 실패1개가 기준 패치로 통과했지만 재설치
실패가 남았다. Requests는 네트워크 차단 상태에서 기준 패치도 필수 검사들을
통과하지 못했다. 환경 검증 실패로 기록하며 스킬 성능으로 계산하지 않는다.
모델 호출·테스트 제외·과제 교체·그래프 수치 변경은 하지 않았다.
