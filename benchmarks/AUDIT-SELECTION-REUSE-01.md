# Non-adjacent baseline reuse opportunity — 2026-09-21

Resource: production Con Artist at parent `4e99345` (unchanged since `2753915`).
[Native probe](probe_audit_selection_reuse.py) and
[all original observations](results/audit-selection-reuse-01.json).
No production edit or model session in this checkpoint.

The existing batch cache keeps the most recent successful normal baseline.
Different test arguments correctly force their own checks, but returning to an
earlier unchanged selection executes that baseline again. This is actual process
work, not an inferred count from repeated output strings.

| Selection sequence | Correct-code executions | Mutant executions | Total |
| --- | ---: | ---: | ---: |
| A, A, B | 2 | 3 | 5 |
| A, B, A | 3 | 3 | 6 |
| A, B, A, B, A, B, A, B | 8 | 8 | 16 |

Three authored native cases, Python3.9.6, one invocation each. A checks an
acknowledgment and misses a removed write; B checks stored values and detects it.
Every correct check passes, every A mutant passes, every B mutant fails with an
actual assertion, all native outputs contain one test, and no output is truncated.
Original files remain intact and each owned scratch directory is removed. The
test wrapper records native execution; it does not replace or mock test results.

This deliberately alternating synthetic recipe demonstrates cache topology, not
prevalence in real work or wasted verification for arbitrary external-state tests.
No new cache exists yet, so no realized token/time/execution reduction is claimed.
The full eight-skill task-level objective remains unmet.

## Implementation gate

Consider a batch-local map of successful normal observations by test selection,
with one shared input identity. Revalidate current bytes/modes, imports, ordered
roots, runner, interpreter, timeout, environment and guard state before reuse.
Any relevant context change invalidates the map. Do not retain a separate20 MB
source snapshot per selection. Preserve input budgets and bound cached metadata.

Keep requested mutation order, fresh mutant copies, per-mutant assertions,
conditional-probe rules and stop-on-incomplete behavior. Reused output must point
directly to the actual earlier executed observation, not a different selection or
reference chain. No cache crosses invocations. External services/flakiness remain
unsupported for reuse; separate baselines are still necessary when freshness is
part of the request. Validate invalidation, interleaving and memory behavior before
adoption. Probe-result caching can remain unchanged rather than expanding scope.

한국어: 같은 배치에서 A→B→A로 테스트 선택이 돌아오면 이미 성공한 A의 정상
검사를 다시 실행하는 것을 확인했다. 변형 코드 검사를 줄이자는 뜻은 아니다.
입력 재검사와 실행 증거 연결을 유지하는 캐시 개선 후보이며, 아직 수정 후
절감 수치나 실제 모델 성능 향상을 측정한 것은 아니다.
