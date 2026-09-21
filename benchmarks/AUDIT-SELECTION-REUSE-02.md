# Batch-local non-adjacent reuse implemented — 2026-09-21

Parent `51a4f5a`. Con Artist now reuses successful normal observations when a
previous test selection returns within the same batch. Mutation order, fresh
mutant execution, native results and original-file checks remain unchanged.
This is a helper execution-count improvement, **not model-token/time evidence**.

| Frozen authored selection sequence | Before normal / mutant | After normal / mutant | Total before → after |
| --- | ---: | ---: | ---: |
| A, A, B | 2 / 3 | 2 / 3 | 5 → 5 |
| A, B, A | 3 / 3 | 2 / 3 | 6 → 5 |
| A, B alternating eight times | 8 / 8 | 2 / 8 | 16 → 10 |

The last fixture executes37.5% fewer total check processes; the adjacent control
does not improve. This is neither37.5% lower latency nor37.5% fewer model tokens.
Cases deliberately expose this cache pattern; its real-world frequency is unknown.
All required mutant executions remain, acknowledgment-only tests still miss the
lost write, stored-value tests still detect it, and source/scratch checks pass.

[Before](results/audit-selection-reuse-01.json),
[first revised run](results/audit-selection-reuse-02.json), and
[final source run](results/audit-selection-reuse-03.json) retain all native outputs,
helper identities, test selection order and counters. Sources/assertions and Python
3.9 interpreter are unchanged. The final run follows a reference-lookup correction
for per-entry tests without common test arguments; it has the same counts as the
first revision. Nothing was discarded. These are native author checks, not model
retries. The original profile's generic limitation saying “No proposed cache” is
stale in both after records; the helper hashes and executions are the measurements.
The profile text is corrected for future runs, without rewriting original records.

## Reuse boundaries

One shared normal-baseline context holds selected bytes/modes, imports, ordered
roots, precheck, runner, interpreter, timeout, environment and optional guard state.
Every audit still rereads current inputs. A context change clears all normal
entries; exact test-argument tuples select among at most eight successful results.
Slots hold a result and execution index, **not another source snapshot**. Reused
references point directly to that executed observation even across A-B-A-B order.
No cache crosses batch calls. Existing single-most-recent probe caching is unchanged.
The current input snapshot, probe identity and guard inventories still consume
memory; this is not a total-process memory limit or concurrent filesystem snapshot.

Five new [native regression tests](../tests/test_audit_selection_cache.py) verify
two independent alternating batches, direct references, unchanged mutant assertions,
input/mode/import/precheck/timeout/environment/guard invalidation, one retained
source context across eight selections with a1 MB asset, failed-baseline stopping,
and per-entry test arguments without common arguments. Memory validation checks
retained context ownership, not an RSS or allocation-time performance claim.

Validation on final helper bytes: Python3.11.16 passes79 audit tests,80 mutation
helper tests and13 build tests. Python3.9 passes the79 audit-test discovery with10
pytest-dependent skips; all five new cache tests execute and pass. Skill validation,
repository validation, localized featured synchronization and diff checks pass.
These targeted local checks do not supersede the earlier whole-suite checkpoint
or claim that hosted CI has recovered.

Freshness-dependent external services and flaky tests remain outside the reuse
guarantee. Use separate audits when fresh correct-code execution is required.
The guide and both capability rows are synchronized. Entry instructions, featured
charts and the unproven all-eight efficiency conclusion remain unchanged.

한국어: A→B→A 같은 배치에서 이미 성공한 정상 결과를 입력 재검사 후 재사용한다.
8회 교차 예제의 실제 검사 프로세스는16회에서10회로 줄었고 변형 검사8회는
그대로다.37.5%는 이 예제의 실행 횟수 감소이지 토큰·시간이나 전체 스킬 성능
개선율이 아니다. 정상 선택이 연속되는 대조 예제는5회로 변화가 없다.
