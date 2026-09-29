# Assertion observation prototype01 — 2026-09-27

Motivation: [optional-detail01 originals](RECEIPT-OPTIONAL-DETAIL-01-REVIEW.md)
include hand-written observers and three assertIsNot argument-name errors before
repair. Search current skills/scripts and existing histories found no reusable
assertion-argument collector; retain existing native comparison/provenance support.

Local standalone prototype only; no installed skill/helper changes or model calls.
[Source and original controls](results/assertion-observer-prototype-01/) capture
standard unittest assertEqual/assertIsNot entry arguments through actual function
code identities, without replacing assertions. Primitive-only encoding avoids
arbitrary object repr; unsupported values are explicitly omitted. Existing profile
hooks are rejected without replacement. Observer errors mark unavailable evidence,
never turn missing values into observed equality or a verified fix.

Four native three-method suite runs show the same outcomes with/without observer:
correct code3PASS/native0; real regression1 assertion failure/native1. A custom
repr that raises remains uncalled in successful identity assertions. Existing
profile hook control passes. Two direct100-assertion controls preserve assertion
success with a64-record limit or a deliberately failing encoder, reporting one
unavailable-evidence marker. Source hashes and final-source results retained.

These are local authored controls, not independent model quality or token/time
measurements. Support currently covers only two standard unittest methods and
bounded primitive types/depth/container sizes. A shared serialized-record byte
budget, interpreter/native startup integration, existing hook behavior and honest
incomplete-output reporting remain production gates. Do not install or advertise
this prototype as ready or reuse old costs as its performance. It is a concrete
candidate to remove repeated observer authoring, not justification for another
shorter-reference comparison. Owner all8 objective remains unmet.

한국어: 실제 관찰 코드 인자 오류를 줄일 수 있는 작은 로컬 시제품을 검사했다.
관찰 여부와 관계없이 정상3개 통과·회귀1개 실패가 유지되고 임의 repr과 기존
프로파일 훅을 건드리지 않았다. 관찰 오류/한도는 확보하지 못한 근거로 표시한다.
스킬에 설치한 기능이나 모델 절감 증거가 아니며 출력 전체 바이트 한도와 실제
네이티브 실행 통합 검증이 남아 있다.
