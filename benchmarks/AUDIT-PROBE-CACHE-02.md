# Non-adjacent stronger-probe reuse — 2026-09-21

Parent `cb9cde1`. The [earlier probe cache](CON-ARTIST-PROBE-REUSE-01.md)
retained only the last successful correct-code stronger check, unlike the
[normal-test selection cache](AUDIT-SELECTION-REUSE-02.md). This change extends
reuse to returning identical probes within a batch. It does not change fault
selection, skip mutants, or claim model adoption or whole-task savings.

## Reproduction and execution counts

[Native regression controls](../tests/test_audit_probe_cache.py) use a real
acknowledgment-only unittest that survives an omitted list append, and stronger
probes that assert the stored value. The following sequences were exercised
twice each, in separate batches, before and after the runtime edit:

| Authored probe sequence | Before processes | After processes |
| --- | ---: | ---: |
| A,A,B (adjacent control) | 9 | 9 |
| A,B,A | 10 | 9 |
| A,B,A,B,A,B,A,B | 25 | 19 |

Before the fix, the new expected-count test failed four subcases with actual
counts10/25 rather than9/19; both adjacent controls passed. These are deliberate
failing-first optimization controls, not a discovered incorrect native result.
Those four subcases stopped at the count assertion, so their later native-output
assertions did not execute. After the fix all subcases verify every mutant's
surviving weak test and actual stronger `AssertionError`, no timeout/truncation,
unchanged original bytes/modes, scratch removal, and direct references to the
first executed correct probe. Separate batches execute their own baselines.

The alternating case removes six of25 processes (24%). This is an intentionally
cache-shaped authored example, **not24% less model time/tokens** or evidence of
how often developers encounter this pattern. No timing comparison was collected.
Eight mutant tests and eight mutant probes still execute in the largest case.

## Invalidation and retention

The probe cache keeps one selected-input context. Bytes/modes, imports, normal
test arguments, ordered import roots, precheck, runner/invocation, interpreter,
timeout, environment and optional project guard must still match. A change
clears all probe entries. Each entry additionally requires exact inline probe,
new-file bytes, replacement bytes and stronger-test arguments. No cross-call
cache or external-state freshness is implied; use separate audits when freshness
is required. Existing permission/precheck/environment controls remain applicable.

At most eight successful probe entries and20 MB of retained probe text/file
contents are kept. Oldest entries are evicted as needed; over-budget probes are
not cached. These bounds exclude shared input data, result logs and Python
overhead and are not total-memory limits. Eviction causes a fresh correct run.
Only successful correct checks enter the cache; incomplete work still stops.
References always point directly to the original execution, not another reference.

Additional controls exercise real changed-input invalidation and alternating
native test-file replacements. Two mock-executor controls exercise content
budget eviction and entry/context ownership only; they are not native runs or
performance evidence. The implementation retains exact probe contents rather
than substituting a hash comparison for the previous identity contract.

## Validation and claims

Python3.11.16 audit discovery passed117 tests in21.766s before the final native
replacement-control method was added. All80 mutation-helper tests passed in
15.672s. The final five-method focused suite passes on Python3.11 and3.9;
repository/skill validation and featured synchronization pass. This is focused
local validation, not a new full release matrix or hosted CI pass.

Committed-source archive `b6df5f6`, with no Git/local-run directory, passes all118
audit tests in21.587s on Python3.11.16 (no skips). Archive repository validation
and featured synchronization also pass. The checkout's13 build tests pass in2.989s.
Final focused five-method suites: Python3.11.16,4.724s; Python3.9.6,4.060s.

Both capability rows and the batch guide are updated. Entry instructions,
frozen model measurements and featured graphs are unchanged. Broad cost benefit
remains unproven; this deterministic reduction applies only when the helper is
used and an identical stronger probe returns under unchanged conditions.

한국어: 동일한 강화 검사가 A→B→A로 돌아와도 성공한 정상 결과를 재사용한다.
교차8회 예제는 검사 프로세스25회에서19회로 줄었고 결함 검사16회는 유지했다.
24%는 이 예제의 실행 횟수 감소이지 모델 토큰·시간이나 전체 성능 개선율이 아니다.
입력 변경 시 전체 캐시를 비우며 저장 한도 초과 시 정상 검사를 다시 실행한다.
