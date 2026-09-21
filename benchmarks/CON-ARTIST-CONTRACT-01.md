# Con Artist contract-focused assertion candidate

2026-09-21, parent `903e7c8`. Historical instruction-only candidate.

Disposition: [six-cell transfer review](CONTRACT-AUDIT-01-REVIEW.md) found no
observed decision or token advantage. The extra paragraph is removed and the
entrypoint restored byte-for-byte to `903e7c8`. The candidate remains available
at `19d63ec`; all original measurements remain intact. This rejects an unproven
optimization, not the general value of contract-based testing.

The design rationale below records the pre-experiment proposal, not a current
unmeasured-status claim.

The [Click pair](CLICK-CONTEXT-01-REVIEW.md) supplies a concrete failure:
the skill-side added test rejected correct code on an incidental traceback
identity requirement before repairing it. That repair and wider native selection
accompany an adverse cost result; no exact causal saving can be inferred.

The candidate adds a narrow distinction to stronger-assertion design: test the
requested behavioral contract rather than incidental representation/identity,
while preserving identity and order when the contract requires them. It names
no Click function, exception mechanism, traceback fix or benchmark answer. It
does not weaken propagation-object identity, native binding, actual assertion
failure, neighboring controls, preservation or cleanup requirements.

Metadata/link checks are structural validation, not proof of model improvement.
The exposed Click task must not be reused as an independent holdout. A subsequent
small frozen transfer comparison should include both a representation-flexible
contract and a genuinely identity-sensitive contract, retain prior/current and
no-skill arms, and review native behavior plus complete resource cost. Reject a
candidate that saves cost by weakening required assertions. No featured changes.

한국어: 정상 구현까지 실패시킨 과잉 검사를 줄이기 위한 지침 후보다. 요구사항에
명시된 객체 동일성·순서 검사는 유지한다. 수정본의 모델 성능은 아직 미측정이며,
이미 정답을 확인한 Click 결과를 개선 증거로 재사용하지 않는다.
