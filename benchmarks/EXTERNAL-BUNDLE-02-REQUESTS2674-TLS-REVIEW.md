# Requests2674 dual-protocol author probe01 — 2026-09-27

Protocol `77f669b0`, unchanged skills `7172b50c`, two fresh author cells,
zero models. [Evidence](results/external-bundle-02-requests2674-tls-probe-01/)
preserves all native scalar outcomes, output hashes, driver/helper identities,
source guards and actual service cleanup. All private labels/logs/patches remain
outside solving contexts and public artifacts; original grade01 is unchanged.

Both native variants finish exit1:11 designated F2P already pass, one fails,
and142 P2P pass. Inventoried source bytes/modes are unchanged outside declared
native caches. Service shutdown completes exit0, no timeout or remaining thread.
Neither variant meets the frozen contract; no new repair or readiness is claimed.

The failure section no longer contains WRONG_VERSION_NUMBER; it now contains
certificate-verification failures in both variants. The original mixed-scheme
test calls Session.send on a prepared request. Source tracing establishes that
Session.send defaults verify to self.verify, while environment CA settings are
merged by the higher-level Session.request path. Therefore supplying
REQUESTS_CA_BUNDLE alone does not configure this direct call. This is a supported
mechanism, not yet a controlled full-case pass after a default-trust correction.
The TLS service control used explicit CA arguments and did not exercise this
direct default-verification path; retain that preflight coverage limitation.

Next distinguish direct-send default trust from environment merging with a small
native unpatched client control. If owned default CA assets need extension, record
that distinct fixture preparation before another case probe; do not edit project
Python, bypass verification, change global trust or overwrite these outcomes.
Already-passing designated failures remain an independent acceptance limitation.

한국어: 포트 문제를 해소한 새 검사도 원본·정답 모두 인증서 검증 실패1개가
남아 채택하지 않는다. 직접 Session.send 경로는 상위 요청 함수처럼 CA 환경
설정을 자동 합치지 않는다. 명시적 CA를 쓴 이전 대조가 이 기본 신뢰 경로까지
검사하지 않았다는 한계를 보존한다. 원본에서 이미 통과한11개도 실패로 바꾸지
않고 모델 절감·전체 준비라고 주장하지 않는다.
