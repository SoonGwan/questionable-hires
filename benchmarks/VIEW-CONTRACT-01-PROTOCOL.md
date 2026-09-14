# View contract development screen — 2026-09-15

Freeze FILES/TASK in `cases_view_contract.py` before model calls. New authored
SQL-only fixture, not an independent real-project holdout. It deliberately exercises
column/value checks targeted by the recent optional API; no broad claim follows.

Compare Friday original `c5eddbc` and candidate `45a2741`. Their entry is identical;
candidate adds `assert_rows` and its optional mode documentation. Do not force
matrix/helper adoption, give the author solution or score helper use as success.
Two fresh persisted GPT-6 Astra / medium sessions, original then candidate, one
each, serial, 240 seconds per cell. Freeze exact task, source revisions and resource
digests before the first call. Stop on account limits; no retries or outcome-driven
changes. Retain both results and original tool responses.

Required work: actual supplied migrations and literal queries at five specified
checkpoints; ten reader observations including inactive failures; ordered labels,
complete ordered values and BLOB bytes; active-vs-inactive classification, first
blocker, rollback data survival and scoped mitigation. SQL-only contract explicitly
excludes application writers/concurrency/crash recovery. No source edits or
publication; any scratch stays project-local and is removed.

Author preflight `preflight_view_contract.py` executes all ten checks. OLD SELECT
succeeds but returns title rather than required label in phases 2–4; a real
column assertion fails. NEW fails only while inactive in phases 1/5. Normal rows
and updated/inserted BLOB rows are checked through rollback. Author preflight and
expected findings are not copied into model projects. No test-support exception
is credited as a production incompatibility.

Review original stored tool responses, capture completeness, source/resource
preservation and scratch inventory, alongside final findings. Compare required
work, helper adoption, generated orchestration, total input+output (cache included
once) and whole-process time. n=1, fixed order, synthetic targeted task and shared
host/cache limit attribution. No chart promotion or all-eight performance claim.

한국어: 컬럼명과 BLOB 값까지 확인해야 하는 SQL 배포 검토용 합성 과제다. 실제
SELECT 성공이 소비자 호환성을 보장하지 않는 상황을 사전 검증했다. 기존·수정
스킬을 각 한 번 실행하며 도우미 사용은 강제하지 않는다. 필요한 열 번의 관측과
원본 보존·정리·판정을 확인하고, 독립 실전 검증이나 일반 성능 향상으로 포장하지 않는다.
