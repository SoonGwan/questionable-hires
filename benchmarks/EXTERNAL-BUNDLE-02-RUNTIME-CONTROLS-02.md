# Native runtime distinctions02 — 2026-09-27

Parent `e1a34d5c`, skills unchanged `7172b50c`, zero models.
[Author controls](results/external-bundle-02-runtime-controls-02/) retain source,
scalar observations and original output hashes. Original grade01 remains unchanged.
Failure-section keyword counts locate experiments, not causal proof or rescoring.

Requests2674's original mixed-scheme check uses the same explicit endpoint port
for HTTP and HTTPS. Grade01 supplied an HTTP-only local server. A fresh native
unpatched Requests control gets HTTP200 but `WRONG_VERSION_NUMBER` on HTTPS
to that port. A disposable WSGI server accepting HTTP and TLS on that same port
gets200 for both with the owned CA and rejects untrusted TLS. Only the test
service changes; no Requests/test patch, global trust or verification bypass.
Native server threads terminate and sockets close. This explains the protocol
mismatch in the control; the designated full base/gold case is not yet rerun.

Apple Python3.9's default pycache prefix is outside the standard `__pycache__`
location. A fresh `py_compile` control with grade01's `-B`/no-write environment
produces zero expected files there and fails; native `-X pycache_prefix=` alone
restores the normal location and passes. Explicit compilation still occurs
with no-write enabled, so that flag is not the distinguishing cause here.
The original pytest5103 P2P source requires this standard cache location. A
controlled native original test and whole required-pair check are still needed.
The owned HOME contains all default Apple cache files; no user cache is changed.

한국어: HTTP 전용 포트에 HTTPS로 접속하면 같은 오류를 재현했고, 검증을
유지하는 HTTP/TLS 공용 테스트 서버에서는 둘 다 성공했다. Apple Python의
기본 캐시 위치도 기존 검사 기대와 달랐으며 표준 CLI 옵션 하나로 대조 결과가
실패에서 통과로 바뀌었다. 원래 사례 전체 검증 전이며 기존 실패와 모델0회를
보존한다. 품질·전체 토큰·시간 개선 증거로 쓰지 않는다.
