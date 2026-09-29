# Token reduction target — 2026-09-27

Measured resource `75183f2f`, integration05, eight tasks, one run per condition.
Source: [existing per-response arithmetic](../benchmarks/results/all-eight-current-05/input-cost-analysis.json).
This defines the next optimization target; it is not an implementation or measured saving.

Total input/output increased by 112,392 tokens: 606,355 → 718,747.
Arithmetic decomposition: initial-input term +32,773; response-count term +14,515;
later-input term +65,531; output term −427. These terms reconcile exactly but
are not causal attribution. Initial input includes other context, and later input
includes prior messages/tool results. Neither term is wholly removable overhead.

`refresh-owner-a` contributes +63,734 and `history-invoice-boundary` +26,435.
Their combined +90,169 is 80.23% of net cohort growth; other tasks include
negative deltas. Prioritize these workflows instead of editing all eight blindly.
The dated [scoped review](../benchmarks/ALL-EIGHT-CURRENT-05-REVIEW.md) preserves
required before/after checks, recovery and unequal work. Do not remove necessary
checks or pretend an unexplained source read is unnecessary.

Before adoption, freeze a concrete mechanism and distinct representative inputs,
retain every scheduled run, assess the same required outcomes and preservation,
and compare full input/output usage and elapsed time. A ratio above 100% remains
an adverse result; an aggregate decrease alone does not establish every skill's
benefit. Failed or incomplete runs remain charged and visible. No favorable-pair
promotion, cached-input subtraction, chart rewriting or unsupported saving claim.

The existing guide-first and same-revision reuse approaches already have dated
reviews; do not repeat them as new candidates. Actual prospective guest-model
execution still needs [a legitimately authorized environment](../benchmarks/SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md).
This target does not waive that boundary or declare all host-model routes unavailable.

한국어: 현재 합계는112,392토큰 증가했다. 후속 입력 항65,531이 가장 크지만
불필요한 작업이라는 인과 증거는 아니다. 상위 두 과제의 증가90,169가 순증가분의
80.23%이므로 이 워크플로를 우선 점검한다. 동일한 필수 결과·검증을 유지한
새 실험에서 전체 입력+출력과 시간을 측정해야 한다. 아직 절감을 구현·입증한
상태가 아니며 기존 불리한 수치와 그래프를 유지한다.
