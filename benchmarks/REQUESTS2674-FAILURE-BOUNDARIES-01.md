# Requests2674 failure boundaries01 — 2026-09-28

**Restore the known compatible service stack; keep the original grade declined.**
A small actual Linux client control reproduces HTTPbin's cookie endpoint HTTP500
under the superseded Flask1.1.4/Werkzeug1.0.1 stack. Reusing the historically verified
Flask0.10.1/Werkzeug0.11.4 repair makes the same control return200 and remove the
expired cookie. Client code and the other nine service dependencies are unchanged.
This repairs one author service path, not the existing issue's full grading contract.

[Protocol](REQUESTS2674-FAILURE-BOUNDARIES-01-PROTOCOL.md) `cba5726f`, corrective
service freeze `f303461f`, parent `d262be6a`. Exorcist directs diagnosis at actual
failure boundaries and reuse of prior observations. No selected issue tests,
original grade retries or model calls occur. Original Requests2674 outcomes remain
154 native passed/8 failed in **both** variants, with11 of12 designated failures
already passing on base. No dependency change is claimed to create that absent
regression contrast.

## Retained original failures

Verify original stdout/observer hashes against frozen owned-official-grade01
records and both private input hashes. Match all8 failed native identities per
variant to their exact original failure section and unchanged required group.
Public [audit](results/requests2674-failure-boundaries01/retained-grade-audit.json)
contains counts, observation categories and hashes, never private grading labels,
test/gold bodies or original failure text. No new statuses or rescoring.

| Observed boundary, same count in each variant | FAIL_TO_PASS | PASS_TO_PASS | Outside required |
| --- | ---: | ---: | ---: |
| DNS resolution fails for external hosts |0|2|0|
| Immediate unreachable network, test expects connect timeout |0|2|0|
| Local issuer verification fails, actual verify=True |1|0|0|
| Cookie-expiration assertion |0|1|0|
| Unsupported string argument to pytest.raises |0|0|1|
| Closed connection pool; gold additionally masks with missing exception.message |0|0|1|

The network observations are not interchangeable: two requests need name
resolution; two public base tests intentionally target a timeout address but the
isolated guest returns immediate ENETUNREACH/ConnectionError instead of the required
ConnectTimeout. No external-network enablement, route manipulation or manufactured
timeout is attempted. The TLS trace shows actual verify=True, consistent with the
already documented [direct-send/default-trust distinction](EXTERNAL-BUNDLE-02-REQUESTS2674-TLS-REVIEW.md).
Correcting that fixture cannot turn the other11 already-passing base obligations
into observed failures. Test-support API/exception compatibility issues outside
required labels still matter to whole native exit, but are not agent failures.

## Cookie boundary and service repair

The client is the exact already-loaded official image config
`1cf3ffbd1932395d2603da9b51dbb7383dc9f64044d241e3cd6b418d5fe56821`, Python3.9.20,
Requests2.7.0 from `/testbed/requests/__init__.py`, source hash verified. The service
runs in a separate process with its own offline-installed prefix; this prefix is
absent from the client path. All11 wheel hashes are verified before transfer and
again in each container. No download, new build, host install or client repair.

The authored sequence sets a sentinel cookie, verifies an unexpired round trip,
and expires it using the public base test's1970 date. It compares a stdlib HTTP
server with the actual HTTPbin app/pytest-httpbin Handler. The first control fails
its expected HTTP200 assertion. Its [original service log](results/requests2674-failure-boundaries01/original-control/service.stderr)
records HTTP500: httpbin0.4.1 calls jsonify on headers.lists(), a generator that
Flask1.1.4 cannot serialize. The final comparative JSON was never written; missing
partial headers/cookie states are not reconstructed or claimed as recorded passes.

This mechanism and its two-version repair were already documented in
[Requests3362 core preparation](EXTERNAL-BUNDLE-02-REQUESTS3362-CORE.md). Linux
service preparation had reused the **pre-repair** stack. The historical repair
should have been traced before fresh reproduction. The original grade's retained
service.stderr also contains two matching generator errors and two endpoint500
records; it was inspected afterward. Its hash is first recorded in this audit,
not falsely described as matching a previously frozen service-log digest. The
first unpublished audit wording overlooked that retained file; its correction
and original private audit hash are preserved. This is not independent validation
or a newly discovered general mechanism.

The corrective control reuses the existing universal Flask0.10.1 wheel, whose
SHA matches the original frozen successful Mac build stdout, plus the pinned
Werkzeug0.11.4 wheel. Source sdist provenance and all other wheel identities remain
verified. [Exact freeze](results/requests2674-failure-boundaries01/corrected-service-freeze.json).
Both actual probe/service Python files are byte-identical between controls;
only these two dependency versions and disposable host/container names change.
This is a joint compatibility repair, not a one-variable causal measurement.

[Corrected original result](results/requests2674-failure-boundaries01/corrected-control/result.json):
normal cookie preservation succeeds against **both** servers; expiration returns200,
actual normalized/raw Set-Cookie headers contain the requested expiration, and the
client removes the cookie in both cases. Server threads stop and sockets close.
The control does not exercise original full-suite ordering or the dual TLS listener,
and no original issue grade is replayed to assert a repaired scored outcome.

## Decision and cleanup

Retain this proven service preparation for a future distinct protocol. Do not run
Requests2674 again just to obtain a green result: DNS/timeout/TLS/test-support limits
and especially the absent11 base failures remain. Its earlier paired rejection,
all required labels and adverse evidence are unchanged. A local service fix is not
a model quality, token/time or all-eight improvement.

Both containers retain network none, no host mounts, cap-drop ALL,
no-new-privileges, default seccomp, writable disposable root,1GiB/1CPU/64PIDs.
[Cleanup](results/requests2674-failure-boundaries01/cleanup.json) verifies no containers,
three inactive/disabled services, stopped VM and no owned Lima/SSH processes.
The [model authorization blocker](SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md) remains;
no approval settings, ordinary skills, featured charts or hosted release change.

한국어: 원본8개 실패를 정확한 필수 그룹과 연결해 DNS2·즉시 네트워크 불가2·
인증서1·쿠키1·필수 밖 호환성2로 구분했다. 쿠키 서버500은 이미 Mac에서 해결한
호환 문제가 Linux 준비에 재도입된 것이며, 기존 수정 버전으로 같은 실제 클라이언트의
정상 유지·만료 제거를 두 서버에서 확인했다. 최초 실패와 뒤늦은 기존 로그 확인도
보존한다. 과제 채점은 반복하지 않았고 원본에서 이미 통과한11개는 그대로다.
모델 호출0회, 전체 품질·토큰·시간 목표는 미달이며 컨테이너·서비스·VM을 종료했다.

## Original regression membership audit — 2026-09-28

`requests2674-required-membership01`, input SHA256
`67f45674a057dd56efaf931dcd1019bc5a4cd721ece0621ee6f01ca92d3375a4`:
the original test patch adds one complete top-level regression function, absent
from the selected base. Its exact native node identity occurs in neither the12
FAIL_TO_PASS nor142 PASS_TO_PASS labels. The
[scalar membership record](results/requests2674-failure-boundaries01/required-membership.json)
retains hashes/counts, not the private test name or patch body. This was obtained
by parsing added patch lines as Python AST and comparing the resulting test identity
with the unchanged groups; no source execution, new model or native replay.

The earlier closed-pool failure outside the required groups is therefore not
evidence that all intended regression behavior is covered by those groups alone.
The existing full native-exit gate already rejects extra failures; this audit
does not uncover a false acceptance or change any grade. Nor does static membership
explain the historical generation of the12 labels, prove that every older runtime
would pass them, or authorize replacing/reclassifying them. Restoring service
compatibility supplies no evidence of the missing base-failure contrast. Keep this
case declined and require new evidence before another environment/grade attempt.

한국어: 원본 테스트 패치가 새로 추가한 회귀 검사1개는 고정된 실패12개·통과142개
목록 어디에도 포함되지 않았다. AST와 원본 목록을 대조했으며 재실행은 없다.
전체 네이티브 종료값 기준은 이미 추가 실패를 거부하므로 잘못된 합격을 발견한
것은 아니다. 기존 결과·기준을 바꾸지 않고, 서비스 호환성만으로 누락된 원본 실패
대조를 만들 수 있다고 가정하지 않는다. 새 근거 없는 평가 반복은 하지 않는다.
