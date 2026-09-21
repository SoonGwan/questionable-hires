# Current candidate: whole-task performance remains unproven

Checkpoint **2026-09-21, resource `a3dee3b`**. This is a decision index, not a new
measurement. [Full chronological history](CANDIDATE-HISTORY-2026-09-21.md) preserves
every preceding checkpoint, including adverse results and preparation notes.
Use dated reports for exact tasks, resources, scope and capture limitations.

## Objective and unfinished requirements

All eight hires should improve real developer outcomes at similar or lower
token/time cost. Reliable helpers and passing tests do not establish that outcome.
A broad20–30% gain remains **unproven**. No independent generalization,
hosted-check success or public-release approval is claimed here.

한국어:8개 스킬 전체가 실제 개발에서 더 적거나 비슷한 비용으로 좋은 결과를 내는
목표는 아직 미달이다. 개별 과제·버전의 결과를 전체 성능으로 확대하지 않는다.
과거 실험과 불리한 결과는 이력 문서에 그대로 보존했다.

## Model evidence that governs claims

Preparation checkpoint2026-09-21, parent`0a7256e`:
[dependency-plan transfer protocol](PLAN-AUDIT-01-PROTOCOL.md) defines two new
authored requests and six planned sessions. Native correct/equivalent/fault
controls pass; no model attempts yet. It is synthetic development transfer,
not independent holdout evidence. 한국어: 새 과제의 실제 대조 검증을 마쳤으며
모델 실측 전 준비다. 개선 수치나 독립 검증 결과로 계산하지 않는다.

| Dated checkpoint / resource | Observed result | Decision and limitation |
| --- | --- | --- |
| [All-eight screen03](results/all-eight-current-03/README.md),2026-09-20,`ee5eb28` | Both arms8/8; skill summed tokens+20.34%, time−3.61%; every pair uses more tokens | Efficiency target unmet. Eight exposed authored tasks,n=1; not a measurement of subsequent changes. |
| [Cachetools audit01](CACHETOOLS-AUDIT-01.md),2026-09-21,`b1875a0` | All three arms5/5; current versus baseline tokens−20.6%, time+30.9% | Changed helper unused; unequal extra checks. One source-excerpt task,n=1; no optimization attribution. |
| [Proposal boundary01](AUDIT-PROPOSAL-01.md),2026-09-21,`e17e13d` | Proposal: tokens−17.46%, time−8.48%,20→10 unittest processes. Verified: tokens+3.40%, time−3.34%; required assertions retained | Retain scope distinction provisionally. Two requests on reused development fixture,n=1; not independent validation. |

한국어: 전체 비교에서는 토큰 증가가 남았다. 제안과 입증을 구분한 수정은 한 사례에서
추가 실행을 줄였지만 입증 과제의 토큰 증가도 공개한다. 독립적인 프로젝트에서
효과가 유지되는지는 아직 확인하지 못했다.

## Implemented capabilities and local validation

- [Receipt selected-read correction](RECEIPT-SELECTED-READ-01.md),`a3dee3b`:
  reproduced FIFO blocking plus accepted link/regular replacements; all three
  now reject at the observed open boundary. Python3.11 Receipt175/build13 and
  Python3.9 helper49 plus race test pass. Same-inode writes and parent races
  remain limitations. No token-saving claim.
- [Con Artist baseline reuse](AUDIT-SELECTION-REUSE-02.md),`b1875a0`: alternating
  selections reduce native executions16→10 while preserving all8 mutant checks.
  [Native timing](AUDIT-SELECTION-TIMING-01.md):0.7080→0.4525s on that authored
  workload. Not whole-task/model efficiency.
- Whole-checkout checkpoint at`7034f1d`: Python3.11.16,1,010 tests in171.171s,
  no failures/skips. It **predates Receipt's selected-read correction**.
- Source archive at`ac1d17c`:994 discovered,22 skipped,no failures. This does not
  establish archive validation of`a3dee3b`. Both detailed test checkpoints remain
  in the [history](CANDIDATE-HISTORY-2026-09-21.md).

한국어: 도구 신뢰성과 특정 배치의 반복 실행은 개선했다. 관련 검사, 전체 검사,
소스 압축본 검사는 서로 다른 범위·커밋의 결과이므로 구분한다.

## Avoid repeating rejected approaches

Reuse [the existing cost analysis](ALL-EIGHT-03-INPUT-COSTS.md) and
`analyze_response_costs.py`; no second profiler is needed. Its arithmetic is not
causal savings. Initial instructions, evidence, source reads and generated work
all contribute to repeated input.

- Receipt read-order/support-routing experiments and transfer limits remain in
  the history. Omitting implementation reads did not consistently reduce cost;
  do not retune the exposed ledger case with another generic “read less” rule.
- [EventEmitter completion candidate](EVENTEMITTER-BOUNDARY-01-REVIEW.md) passed
  criteria but increased both costs on both tasks; not promoted.
- [Hostage conditional candidate](HOSTAGE-CONDITIONAL-01-REVIEW.md) and historical
  reporter experiments retain adverse results. Smaller output or fewer methods
  do not establish equivalent coverage or measured savings.

Before another edit, identify an unresolved mechanism and check prior attempts.
New performance experiments need a different relevant task plus controls,
frozen criteria and every scheduled attempt retained. The known proposal case
is a regression control, not an independent test set.

한국어: 같은 읽기 안내·출력 축소 후보를 반복하지 않는다. 기존 실패 실험부터
확인하고 새 근거가 있을 때 수정한다. 다른 과제와 필수 검증 대조가 필요하다.

## Release and publication boundary

Last inspected hosted checkpoint:
[run35563929473](https://github.com/SoonGwan/questionable-hires/actions/runs/35563929473)
at`2753915` had no executed job steps; annotation cited payments/spending limit.
This is historical, not a fresh account-status check. Local results do not
establish hosted validation. Do not change billing/visibility without owner
direction; scoped local work can continue.

Keep `featured.json` tied to its frozen evidence. Representative changes require
reviewed data and synchronized English/Korean text/charts. No small checkpoint
above independently justifies replacing it.

한국어: 호스팅 검사 성공과 공개 배포 승인은 아직 확인되지 않았다. 과거 결제·한도
오류를 현재 계정 상태로 단정하지 않고 계정 설정·공개 여부도 임의로 바꾸지 않는다.
대표 그래프는 검토된 자료와 두 언어를 함께 갱신할 때만 변경한다.
