# Receipt known-input read candidate — 2026-09-20

Historical pre-measurement design, resources `ca668a4`. Follow-up
[read-order 01](results/receipt-read-01/README.md) rejected the candidate:
tokens +30.89%, time +5.42% versus original. The proposal below is retained as
written; production Receipt was not changed.
In [all-eight current 02](results/all-eight-current-02/README.md), Receipt used
104,717 tokens versus baseline 68,379 (+53.14%). Its first CLI command inventories
paths already supplied in the task, followed by known-file reads. It also reads
227 helper implementation lines. Neither activity is assumed worthless: missing
path discovery and concrete trust/diagnosis inspection remain permitted.

Candidate changes only the entrypoint's discovery paragraph to read known inputs,
applicable instructions and status together, with discovery for unresolved paths.
No helper implementation, evidence requirement, import provenance, preservation
guard, native runner, mode selection or read authority changes. It does not forbid
implementation inspection or promise fewer calls. Source and resource isolation
tests establish what changed, **not behavioral compliance or performance**.

Next measurement should retain the exposed ledger-delivery-b task, fresh no-skill
and original controls, serial calls and all costs; freeze scheduling, source
identities and native positive/negative controls before launch. Review actual
first reads, unresolved-path handling, needed support selection, same-process
imports, genuine before/after assertions and preservation before comparing
tokens/time. A favorable result on the exposed task is not a held-out all-eight
win. Reuse current assertions and disclose the partial-fix outcome; do not change
the fixture to turn its intended after-failure into a pass.

한국어: 최근 Receipt 실행에서 알려진 경로를 먼저 목록 조회한 뒤 읽은 비용을
줄이기 위한 미측정 후보다. 필요한 검색과 구현 검토 권한은 유지하고 첫 읽기
안내만 바꿨다. 런타임·증거 기준은 동일하며 실제 성능 향상은 아직 주장하지
않는다. 기존 부분 수정 과제의 실패 결과를 그대로 보존해 후속 비교한다.
