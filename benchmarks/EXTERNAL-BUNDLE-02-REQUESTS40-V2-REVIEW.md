# Requests4.0 verbose/v2 author compatibility — 2026-09-27

Protocol `acfc5efe`, skills `7172b50c`, two fresh native cells, zero model calls.
[Evidence](results/external-bundle-02-requests40-v2-probe-01/) preserves all
scalar original outcomes, hashes, source guards, native exits and driver identity.
Both satisfy the prospectively frozen scoped compatibility contract: base has
the one designated failure and75 required passes; gold has all76 required passes.
Native base1/gold0, no timeout, both complete with source inventories unchanged
outside declared native caches and explicit native thread cleanup.

Whole-file base182PASS/1FAIL/2XPASS; gold183PASS/2XPASS. XPASS remains separate:
the official parser's TestStatus enum omits XPASS, so its zero parsed XPASS count
does not describe the native results. Native summary counts retain both events.
No gold/test bodies, labels or answer-bearing logs are published or given to solvers.

This uses unchanged official v2 parser code on actual native verbose classic
output. That function is not officially mapped to Requests. The original mapped
parser failure, grade01, complete-file probe and their failed obligations remain
unchanged. This is one author compatibility pair, not a full official harness,
independent model validation, all8-case readiness or token/time saving. Other
selected case gates and role-specific quality remain unresolved.

한국어: 사전에 고정한 별도 호환 검사에서 지정 실패1개가 정답 적용 후 통과했고
기존75개도 양쪽에서 통과했다. 전체 파일의 예상 밖 통과2개씩은 별도 보존한다.
Requests 공식 지정 평가기와 다른 함수라 기존 실패를 성공으로 덮어쓰지 않는다.
모델 실행은0회이며 전체8개 준비·품질·작업 토큰·시간 개선 증거가 아니다.
