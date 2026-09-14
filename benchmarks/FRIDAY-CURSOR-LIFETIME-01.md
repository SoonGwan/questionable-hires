# Friday bounded-reader cursor lifetime — 2026-09-15

Parent source: `be44fb9`. This is a local helper correctness regression, not a
model benchmark or a token/time improvement claim.

## Reproduced failure

The matrix reads at most 21 rows to report 20 rows plus a truncation flag. It left
the last cursor open. When rows remained, a subsequent `DROP TABLE` on that same
table failed with `database table is locked`. The lock came from the helper's own
observation, not a demonstrated incompatibility in the release being reviewed.
An intervening invalid reader could leave the previous cursor alive too.

Three new test methods in `tests/test_friday_matrix.py` exercise actual SQLite:

- Table replacement after 20, 21, 22 and 100 rows, with and without an intervening
  invalid-column reader: eight boundary/control combinations. Preserve the first
  20 observed values and truncation flag; require the next phase to return 101.
- A genuinely invalid migration after dropping the table: retain the actual
  missing-table error, leave checks empty and do not execute the third phase.
- The public CLI: require exit 0, truncated initial observations and the new value
  after successful replacement.

Before the fix, the 42-test helper suite reported **six assertion failures**:
four 22/100-row combinations, CLI exit 1 instead of 0, and the real migration
error masked by the helper's lock. The 20/21-row combinations passed. These are
assertion failures against actual results, not unavailable dependencies or setup
exceptions. Representative original output:

```text
AssertionError: False is not true
replacement: checks={}, migration_error='database table is locked'
AssertionError: 1 != 0
AssertionError: 'no such table: missing' not found in 'database table is locked'
```

## Correction and validation

Close each check cursor in `finally`, including when fetching fails or no result
set is produced. No draining of the remaining rows, larger result cap, automatic
retry, SQL rewriting, suppression of errors or new instruction text. Later phases
still execute their own SQL and observations; the input and output schema stay
unchanged. Database cleanup remains in the existing outer `finally`.

After the fix: **42 helper tests pass**, including all eight boundary/control
combinations and the genuine-failure/CLI tests. Skill validation, repository
metadata/local links and featured synchronization checks pass.

Reproduce with:

```sh
python3 -B -m unittest discover -s tests -p test_friday_matrix.py
```

This prevents a specific tool-induced false blocker. It does not establish real
deployment safety, complete equality of truncated results, all-eight skill
performance, or a 20–30% gain. No model sessions were run for this correction;
frozen benchmark values and charts remain unchanged.

## 한국어

Friday의 SQLite 도우미가 긴 조회 결과를 일부만 읽고 커서를 닫지 않아,
다음 테이블 교체를 자체 잠금 오류로 막는 문제를 실제로 재현했다. 20·21행은
통과하지만 22·100행에서 실패하며, 중간에 잘못된 조회가 있어도 재현된다.
커서를 매번 정리하도록 수정해 관련 42개 검사가 통과했다. 실제 마이그레이션
오류는 그대로 드러나고 이후 단계는 실행하지 않는다. 조회 제한을 늘리거나
실패를 무시한 것이 아니다. 도구가 만든 잘못된 차단을 고친 결과이며, 모델의
토큰·시간 절감이나 전체 스킬 성능 향상률은 이번에 측정하지 않았다.
