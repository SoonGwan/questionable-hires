# Receipt guide compaction 02 — 2026-09-14

Parent source: `b55aa6a`. This is a documentation candidate, not a new model
benchmark. The [native-mode review](RECEIPT-NATIVE-MODEL-01-REVIEW.md) still
reports 14.67% more tokens than the earlier baseline; no token parity is claimed.

## Change and checks

`skills/receipt/references/existing-fix.md` shrinks from 7,563 to 6,953 UTF-8
bytes: 610 fewer bytes (8.07%). This measures file bytes, **not tokens or model
performance**. A single guide remains; entry instructions, runtime, recipe
examples and resource count are unchanged.

The edit removes repeated wording from tree preservation, native invocation,
exit interpretation and execution limits. It retains authorization boundaries,
size limits, fail-closed behavior, native empty/all-skipped exit caveats,
provenance requirements, cleanup limitations and the trusted-test-only boundary.
It does not add a new routing rule or relax evidence requirements.

Validation: 72 passing tests (47 helper / 15.293s, 13 native invocation / 5.855s,
12 build / 3.282s); repository validation,
Receipt skill validation, featured localization check and whitespace check.
These are author checks, not evidence of reduced model effort. No model run was
performed for this prose candidate. Frozen results, charts and the featured
pointer are unchanged. A future efficiency comparison must measure the candidate
and a contemporaneous baseline with identical required work; file-size reduction
alone cannot justify a performance claim.

## 한국어

실행 안내를 7,563바이트에서 6,953바이트로 줄였다(610바이트, 8.07%).
파일 크기 감소이며 토큰·실행 시간 감소를 측정한 결과는 아니다. 실행 코드,
예제, 시작 안내와 문서 개수는 그대로이고, 원본 보존·실행 종료 해석·제한의
중복 설명만 줄였다. 위험 조건과 검증 의무는 유지했다.

작성자 테스트와 문서·언어 동기화 검사를 적용했다. 이 변경의 모델 실행은
아직 없으며 이전 결과와 그래프는 변경하지 않았다. 직전 측정의 기본 모델
대비 토큰 14.67% 증가도 그대로 남는다. 실제 효율은 동일한 작업을 수행하는
새 기본/스킬 비교로 확인해야 한다.
