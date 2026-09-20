# Real repository regression boundary — 2026-09-21

This prepares a different development workflow after the rejected path-discovery
candidate. It does not rerun the exposed eight-task screen or claim a new skill
win. The issue is an actual bug repaired in this repository: the async component
probe waited for callback entry after the component had already returned, raised,
or cancelled. The fix retains failure reasons and terminates incomplete execution.

## Verified author replay

[Reproduction script](check_sequence_entry_repository.py) and
[native outputs, selected test identities and source hashes](sequence-entry-repository-preflight-01.json).

- Original implementation: `8804ee4`; corrected implementation: `ec4a538`.
- Both use byte-identical real test files from `87513cb`, without test rewriting.
- Eight selected existing tests: six entry/lifecycle checks and two normal/stale
  ownership controls. This excludes the CLI temporary-directory test and is not
  the full repository suite.
- Before: native exit 1, eight tests, four errors caused by expired async waits.
  These are the observed bug paths, not missing imports or setup errors.
- After: native exit 0, all eight pass. No timeout/retry or replacement replay.
- The native test process asserts and prints the actual loaded component path
  inside its own disposable copy. Files/modes remain unchanged and both copies
  are removed. The source checkout is not patched or reset.

Reproduce with Python3.11 and a **new** output path:

```sh
python3 -B benchmarks/check_sequence_entry_repository.py --output /path/to/new-report.json
```

The script needs this repository's pinned Git history. It is an optional author
replay, not an archive-only unit test or a new mandatory skill operation.

## Next whole-task boundary

A useful next model task is retrospective verification of this already-present
fix with the same current tests and controls, loaded-code evidence, preservation
and cleanup. It should not ask the model to reinvent the already-reviewed fix or
add unrelated tests. Give identical known paths and requirements to no-skill and
Receipt arms; use isolated fresh sessions and freeze the complete project inputs,
scope criteria, schedule and resources before launching either arm.

Evaluate complete work, including reading, setup, failed attempts and final checks.
Do not count a setup exception as the expected regression, relax preservation to
reduce cost, or infer token savings from the helper's runtime profile. Retain both
arms even if the skill costs more. A pilot can determine whether the support is
adopted and which work dominates; one known, author-inspected issue cannot establish
a broad 20–30% gain or held-out generalization. No model session is launched or
resource candidate adopted by this preparation.

한국어: 합성 과제를 다시 맞추는 대신 이 저장소에서 실제 수정한 요청 진입 전
종료 버그를 대조했다. 동일한 기존 테스트 8개에서 수정 전에는 실제 타임아웃
오류 4개가 나고, 수정 후에는 모두 통과한다. 로드 경로·원본 보존·복사본 정리를
검증했다. 다음 모델 비교를 위한 작성자 측 준비이며 토큰 절감이나 스킬 전체
우위를 입증한 결과는 아니다. 이미 알려진 한 이슈라는 한계도 유지한다.
