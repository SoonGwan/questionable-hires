# Con Artist failure guidance correction — 2026-09-28

Parent **`ca033bac`**. [Source identity](../benchmarks/results/audit-error-guidance01/identity.json)
confirms the helper is unchanged; this corrects two installed reference documents,
not the runtime or the [mixed model-cost measurement](../benchmarks/AUDIT-PROBE-SELECTION-MODEL01-REVIEW.md).

The batch reference still said that integrity/cleanup RuntimeErrors propagate
without a collected batch report, and described later failures only as empty
checks. Since the [execution-evidence repair](../benchmarks/AUDIT-EXECUTION-EVIDENCE-01.md),
returned checks and earlier audits survive those errors, including baseline
references and partial evidence from a failing first audit. The common CLI guide
already describes this behavior correctly. The stale branch could cause a reader
to overlook returned evidence; no model rerun or measured cost is attributed to it.

The batch guide now distinguishes retained results from missing checks, stderr-only
failures with no evidence, later input/I/O incomplete returns, RuntimeError/first-audit
raises with attached partial evidence, and interruptions. The diagnostic guide
clarifies that an unconfirmed child has no completed observation, while earlier
returned checks remain available as incomplete evidence. It also recognizes the
existing authorized whole-project guard when describing protection outside selected
files. Nothing authorizes retrying an unconfirmed process, restoring originals,
continuing later mutations, or treating an incomplete audit as successful.

[Existing controls](../benchmarks/results/audit-error-guidance01/tests.txt):19 pass,
zero skips, Python3.11.6. They include real native observations with injected copy,
execution, cleanup and integrity failures, plus simulated child-confirmation and
interruption boundaries. They are not proof of OS process termination or every
possible exception. No new wording-matching test is added. The source diff is
restricted to the two references; entry, metadata, helper and original test contracts
remain unchanged. Both README capability rows already describe retained evidence
and remain accurate. Featured data and all model measurements remain historical.

한국어: 배치 안내가 이미 반환된 오류 근거를 잃는다고 잘못 설명하던 부분을
현재 동작에 맞췄다. 확인하지 못한 자식 실행은 결과를 추정하지 않지만 이전에
반환된 검사는 불완전 근거로 남는다. 전체 프로젝트 보호 옵션도 반영했다.
기존19개 검사가 통과했으며 실행 코드·모델 비용·대표 수치는 바꾸지 않았다.
