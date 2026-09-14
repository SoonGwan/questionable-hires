# Friday native row assertions — 2026-09-15

Feature source `cb7cba1`, test-first parent `eaf4b63`.
This is **capability and local regression evidence, not a model efficiency gain**.

The retained [earlier model command](results/friday-core-guide-model-01/rolling-schema--skill--1/commands.json)
repeated completion, success, truncation, column and row guards after collecting
the SQL matrix. This motivates an optional reusable assertion, not a claim that
the model's original checks were wrong or that every release needs this helper.

`assert_rows(result, phase_index, check, columns=..., rows=...)` checks one selected
native observation. It does not execute SQL, modify results, sort rows, merge
duplicate columns or claim deployment readiness. Complete sequence, successful
selected reader and untruncated rows are required before ordered labels/values
are compared. Errors identify phase/check and expected/observed values. Explicit
raises remain active under Python optimization. Native BLOB bytes are retained;
comparison uses Python value equality, not SQLite storage-type proof.

Expected SQL failures and unselected observations still require their own review.
No new skill-entry instructions, automatic helper adoption, CLI result changes,
application-writer simulation or external actions are introduced. The mode guide
offers the assertion only after a result is already collected.

## Validation

- Before implementation, six new tests produce nine `AttributeError` entries
  because the API does not exist. This is an unmet feature, not nine runtime bugs.
- Final eight feature checks pass / 0.132s: actual old/new values, failure
  diagnostics, no SQL rerun or result mutation, BLOB/duplicate/empty columns,
  actual SQL failure, truncated prefixes, incomplete sequences, unrun checks,
  index/shape/order rejection and a real `python -O` mismatch exit.
- All 42 existing matrix checks pass / 0.434s. Intermediate placement of the
  concrete example inside the generic execution snippet broke two documentation
  tests; moving it into its own optional example restores their existing tests.
  A Markdown-link false positive was avoided by assigning the callable to a
  named local before invocation. No failed checks were weakened or skipped.
- The documented optional example is separately executed against an actual
  successful native result, then a deliberately altered value; it passes and
  rejects the mismatch with expected `old` / observed `wrong` evidence.
- Full source `cb7cba1` local system-Python suite: **651 discovered / 648 passed /
  3 explicit pytest-environment skips / 98.235s**. No claim that skipped checks
  passed. A separate run of `test_audit_pytest_replacements.py` in the existing
  Python 3.9.6 / pytest 8.3.4 environment passes all three / 3.160s. This does not
  relabel the system-Python skips or claim a full-suite run in the second runtime.

Metadata/local-link, featured synchronization and whitespace checks pass. Existing
featured charts and historical measurements stay unchanged. No hosted CI, Linux,
model adoption or whole-task cost claim is made.

한국어: 기존 모델 실행에서 반복 작성하던 SQL 결과 검증을 선택적 API로 추가했다.
완료 여부·오류·잘림·컬럼·값을 확인하며 SQL을 다시 실행하거나 결과를 바꾸지 않는다.
새 기능 검사 8개와 기존 행렬 검사 42개가 통과했다. 전체 기본 Python 검사는
651개 중 648개 통과·pytest 환경 부족 3개 생략이다. 생략된 3개는 기존 pytest
환경에서 별도로 모두 통과했다(3.160초). 중간 문서 예제 실패도
수정했고 기록했다. 모델 성능 개선율이나 배포 안전성을 입증한 것은 아니다.
