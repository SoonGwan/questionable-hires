# Contract audit transfer 01 — no demonstrated candidate benefit

2026-09-21. Launch `6daafcb`; prior Con Artist `903e7c8`, candidate `19d63ec`.
[Frozen protocol](CONTRACT-AUDIT-01-PROTOCOL.md),
[six original attempts](results/contract-audit-01/comparison.json).

| Task | Condition | Tokens | Wall seconds | Responses / shell commands |
| --- | --- | ---: | ---: | ---: |
| Response | Baseline | 67,474 | 86.745 | 4 / 3 |
| Response | Prior | 74,375 | 84.645 | 4 / 4 |
| Response | Candidate | 74,790 | 96.441 | 4 / 4 |
| Identity | Baseline | 67,674 | 94.500 | 4 / 3 |
| Identity | Prior | 73,931 | 80.822 | 4 / 4 |
| Identity | Candidate | 73,983 | 73.568 | 4 / 4 |

Every cell completes and meets all five reviewed obligations; no timeout or
account-limit interruption. Total input includes cache once, output includes
reasoning once. Token sums: baseline **135,148**, prior **148,306**, candidate
**148,773**. Candidate is **0.31% above prior and 10.08% above baseline**. Neither
task shows a token reduction against either comparator. All cells use custom
native workflows, no helper adoption, no assertion-repair phase.

**Wall time is not clean latency evidence.** Author checkout regression ran on
the same host during prior/response, candidate/response and candidate/identity;
completion observed at 02:11:54 UTC. This was not part of the frozen schedule.
The [execution note](results/contract-audit-01/execution-context.md) preserves
the limitation. Do not claim speed gains or rerun/drop cells to hide the overlap.
Two authored candidate-targeting tasks, n=1, fixed serial order, shared host/cache,
unequal native checks and unblinded review also preclude general/causal claims.

## Actual behavior

Response: all identify the keys-only nonempty assertion gap and retain exact
decoded content/order/duplicates, string return and empty controls without
requiring whitespace or mapping-key order. Baseline uses a sorting fault and
four added tests: correct4 pass/faulty1 failure. Prior returns an empty payload:
original2 plus one subtest method gives3 tests, correct pass/faulty4 subtest
failures. Candidate sorts/deduplicates, strengthens the existing assertion and
adds a subtest method:3 tests, correct pass/faulty4 assertion failures. Existing2
pass correct/faulty in every arm. No arbitrary representation constraint appears
in prior or baseline, so the candidate does not uniquely prevent an observed error.

Identity: all use the same actual shallow-copy return fault; original2 pass both.
Baseline's same4 added tests pass correct and produce3 faulty failures; prior and
candidate run original2 plus4 added tests (6 pass correct, respectively4 and6
faulty assertion failures including subtests). All retain required object identity,
shared edits, separate-key and missing-key checks. Some faulty assertions stop at
their first failure; this does not establish every downstream assertion or every
possible mutation. Candidate does not remove required identity verification, but
prior and baseline also preserve it without the added guidance.

Each native process checks copy-local module/function bindings, not a separate
import-only probe. All originals, modes, notes, Git HEAD/staged entries and skill
resources pass independent artifact checks; model snapshots include Git metadata
and finally cleanup. Initial binary index bytes were not independently captured.
Identity baseline has no child deadline; the other five use30-second child
deadlines, all within the360-second cell cap.

Four skill native CLI outputs are shorter suffixes than matching original records;
the complete original tool evidence is retained without replay. Both baseline
captures match exactly. Exact skill bodies appear in initial messages and later
reads in all skill cells; baseline non-observation is not proof of absence.
Private initial messages remain local; exported evidence is redacted and scanned.

## Decision

Reject the added entrypoint paragraph as an optimization candidate: it adds
instructions without an observed decision or resource advantage in this check.
This is not proof that the advice is universally harmful. Restore the prior
entrypoint and preserve the candidate revision and all evidence. Do not retune
these exposed fixtures until they turn favorable. No featured/chart update or
release approval; whole-task performance across all eight skills remains unproven.

한국어: 6개 실행 모두 요구사항은 충족했지만 수정본의 토큰 절감이나 고유한
행동 개선은 확인되지 않았다. 이전 대비0.31%, 무스킬 대비10.08% 더 사용했다.
같은 호스트에서 회귀 검사가 겹쳐 시간 차이를 개선 근거로 사용하지 않는다.
추가 지침은 채택하지 않고 이전 진입 지침으로 되돌리되 모든 결과를 보존한다.
