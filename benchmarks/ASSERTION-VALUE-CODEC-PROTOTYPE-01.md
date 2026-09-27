# Assertion value codec prototype01 — 2026-09-27

Parent `c2ad2c35`; standalone observer SHA256
`3f840f86fe988da438232dde98542285c2662e73ac69fa1e2b55165bde166d29`.
**Local prototype, zero models, no installed skill changes.** The preceding
[API01 model review](RECEIPT-ASSERTION-API-01-REVIEW.md) remains adverse:
whole tokens+25.03%,time−5.05%,zero joint reductions. This is a new primitive
representation experiment, not a rerun or relabeling of its measurements.

Existing history search found the [native transcript format](NATIVE-TRANSCRIPT-FORMAT-01.md)
rejected because section metadata outweighed escaping savings, and the bounded
observer prototypes use verbose kind/items containers. This prototype changes
only container encoding: built-in lists become JSON arrays; tuples become
`{"tuple":[...]}`. Bytes retain `bytes_hex`, primitive scalar values unchanged.
No user dictionaries/custom objects are admitted, so tuple tags are unambiguous.
Existing depth/size/node/record/report bounds and profile ownership remain intact.

[Control and source](results/assertion-value-codec-prototype-01/control.py) reuse
real Receipt helper/native fixtures and inject the candidate source in memory.
[Final observations including native outputs](results/assertion-value-codec-prototype-01/results.json)
retain exact original argument encodings and decoded equality. Native comparison
copies are disposable and production skill bytes are unchanged.

## Local evidence

Final run:8 comparisons/20 actual native six-test processes, both bootstrap and
module modes across existing exposed single/multiple windows cases. Original
before failure(s)/after PASS, exits1/0 or1/1/0, suite counts, copy imports/full
revisions, source guard and scratch cleanup pass. Ten report pairs cover70 argument
records; all restore equal primitive values and object-identity flags. Nine
primitive/list/tuple roundtrips and five unsupported/bounded/no-arbitrary-repr
controls pass. Candidate reports stay within4096 bytes.

| Ten corresponding reports | ASCII JSON bytes |
| --- | ---: |
| Previous kind/items encoding |14,896|
| Candidate array/tuple encoding |8,806|
| Change |−40.88%|

These are report bytes, not tokenizer counts, full native output, whole-task model
tokens, latency or quality scores. Model readability/adoption and downstream
compatibility are unverified; installed API still uses previous representation.
No paid comparison is justified solely by this local size reduction.

The first control attempt stops with a KeyError after the first two comparisons
(four native processes): it assumed module-only provenance_ready exists in
bootstrap results. [Original failure](results/assertion-value-codec-prototype-01/initial-control-failure.txt)
is retained; corrected control verifies actual import lines in both modes and
module readiness additionally. The [first completed run](results/assertion-value-codec-prototype-01/first-complete-results.json)
passes20 native processes but retains only argument reports. A separate final
20-process run adds full native-output retention; it is not recovered first-run
output. Total44 local native processes including failed-control attempt, no models.
Reused fixtures are development checks, not independent validation/all8 readiness.

Next gate: explicit API migration/consumer compatibility and meaningful native
budget/ownership controls for the candidate before any model efficiency claim.
Do not promote report byte reduction into landing charts or featured benchmark.

한국어: 리스트·튜플의 반복 표식을 줄인 로컬 시제품은 실제 값70개를 동일하게
복원하며 관찰 보고서 크기40.88%를 줄였다. 이는 전체 모델 토큰·시간 절감이
아니며 기존 설치 기능은 변경하지 않았다. 초기 검사 오류와 별도 출력 보존
재실행을 구분하고, 전체8개 개선 목표는 미완료로 유지한다.
