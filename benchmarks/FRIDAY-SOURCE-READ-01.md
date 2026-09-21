# Friday source reads — replacement rejection

2026-09-21, predecessor `71068c0`. Local tool reliability correction, not model
token/time evidence or a replacement for the adverse performance comparisons.

The matrix inspected SQL files and literal-reader Python modules, then used a
separate blocking path open. Deterministic replacement immediately before that
open showed two defects in both paths: a FIFO waited for a writer beyond the
two-second probe deadline, while a different regular file or symlink was read as
the inspected source. Source preparation precedes the helper's SQL deadline.

The [regression probe](../tests/test_sqlite_read_races.py) uses actual temporary
files and the actual matrix module. It hooks the open boundary, retains the original
inode, and records whether SQLite is ever opened. The final corrected probe failed
before the fix with two process timeouts and four accepted-replacement failures;
the normal UTF-8/CRLF control passed. An earlier harness attempt missed the macOS
resolved-path alias and was corrected before attributing the FIFO behavior.

## Correction

Both source kinds now share a bounded read that validates the inspected file and
the opened descriptor's regular type, device/inode identity and size. Supported
nonblocking/no-follow open flags prevent a replacement FIFO from waiting or a
replacement final symlink from being followed. Descriptor ownership stays inside
the stream context, including rejection paths. Existing byte budgets, reader-cache
scope, raw-byte hashes, SQL behavior and missing-file ValueError remain intact.

The six replacement scenarios now reject before SQLite opens. The two new tests
(six replacement subcases plus stable-byte/native-result control) pass Python3.9
and3.11. The existing77 Friday tests pass on both runtimes. Their file-open counting
and growth mocks were moved to the descriptor I/O boundary without relaxing
expected read counts, byte limits, parse caching or the no-SQL-before-rejection
assertions. An initial implementation name collision and missing-file exception
regression were detected and corrected before this checkpoint.
Build13 and installation20 tests also pass on Python3.9; repository, skill
frontmatter and localized featured-pointer checks pass. These are local checks,
not hosted CI or new whole-suite/model results.

## Limits

The POSIX replacement probe does not certify all operating systems. Platforms
without the relevant flags have weaker replacement behavior. Same-inode writes,
parent-directory races and consistent multi-file snapshots remain outside scope.
Recipe file/stdin reading is unchanged; this is not a universal process deadline
or filesystem sandbox. No production database, upstream project or billing setting
was changed. Skill entry instructions are unchanged; detail stays in the existing
conditional reference. No model rerun or featured-chart update was performed.

한국어: Friday 도구가 검사한 파일 대신 교체된 파일을 읽거나 FIFO에서 멈추는
문제를 재현하고 수정했다. 정상 파일의 결과·해시·입력 한도는 유지했다. 로컬
신뢰성 개선이며, 모델 토큰·시간 절감이나 전체 스킬 성능 향상의 증거는 아니다.
