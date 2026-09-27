# Owned Linux TLS01 — trust controls and corrected scheme echo

Dated checkpoint **2026-09-27**, protocol`f5c9886a`,prospective scheme fix`89b2e640`,
parent`0a7c5b5c`. [Protocol](OWNED-LINUX-TLS-01-PROTOCOL.md),
[first observation](results/owned-linux-tls-01/first-result.json),
[final observation](results/owned-linux-tls-01/result.json).
Zero models/selected-case tests;8skills and featured measurements unchanged.

## Actual cryptographic and protocol outcomes

Reuse unchanged image Python3.9.20/project Requests and the separately installed
Linux HTTPbin prefix. The actual service accepts both HTTP and TLS on the same
native guest loopback port, using the earlier owned socket-peek DualServer.
Final native client outcomes:

| Control | Actual outcome |
| --- | --- |
| Plain HTTP /get | 200, exact authored args, echoed http URL |
| HTTPS with owned CA explicitly supplied | 200, exact args, echoed https URL |
| HTTPS with default CA, without owned trust | SSLError, certificate-verification message |
| Owned-CA HTTPS to wrong hostname127.1 | SSLError, actual hostname-mismatch message |

No verify=False or global trust installation. Unexpected connection/resolver/error
classes do not satisfy rejection checks. Numeric loopback alias127.1 reaches the
same service but differs from certificate CN127.0.0.1; the actual rejection has
hostname text, rather than an inferred DNS failure. Default CA rejection demonstrates
that this authored certificate is **not** trusted by default; it does not establish
selected-test default trust readiness.

## Retained initial scheme defect and correction

First observation passes all4 transport/trust controls and cleanup,7.056s. However
trusted HTTPS's JSON URL incorrectly echoes **http**, so transport trust success
is not complete protocol parity. Original result/source/raw log remain preserved;
no first success/failure is relabeled. After freezing the observed intervention,
subclass only the existing WSGI Handler to set **HTTPS on/off according to the
accepted ssl.SSLSocket** in per-request environ. Keep client/app/test/certificate/
wheel bytes unchanged. This corrects fixture metadata, not Requests behavior.

Second related observation **6.608s** preserves all4 outcomes and now requires
both exact HTTP/HTTPS echoed URLs. VM/controller0, offline install0, all routing
statuses0, native service0, no forced cleanup or deadline hit. Thread joins/socket
closes and guest powers off. Actual imported module versions/paths and native
MarkupSafe extension match the verified Linux wheel; post-observation checks from
[service01](OWNED-LINUX-SERVICE-01.md) validate original values without native replay.
Client service package absence and original source digest remain unchanged.

## Certificate and process boundaries

Existing owned leaf/CA both pass actual OpenSSL **checkend3600** before this gate.
Leaf CN127.0.0.1,notBefore2026-09-27 00:54:46UTC,notAfter2026-09-29 00:54:46UTC.
Digests match the earlier certificate-refresh record;
[opaque identities](results/owned-linux-tls-01/certificate-identities.json).
Only server key is copied into private0700 fixture with0600 key permissions;
CA signing key is not copied. **No key/certificate body is published** or given to
solvers, no host/profile/trust-store change. This dated short-lived fixture needs
fresh validity checking for any later execution, not permanent readiness claims.

[Driver](results/owned-linux-tls-01/fixture/probe.py),
[service](results/owned-linux-tls-01/fixture/server.py),
[VM](results/owned-linux-tls-01/probe.swift),
[controller](results/owned-linux-tls-01/control.py),
[resource hashes](results/owned-linux-tls-01/resource-hashes.json).
Root/probe readonly; only guest tmpfs receives isolated service packages.1CPU/1GiB,
no NIC/block device, loopback only. Pip30s/ready10s/request3s/shutdown10s with owned
guest group TERM/KILL, guest180s/independent parent200s watchdog. All VMs/service
processes terminate normally; owned volume detached after evidence collection.
Nonempty service stderr hashes are retained; negative TLS handshakes and warnings
are not described as warning-free. Raw original consoles remain private/opaque hashes.

No selected official script/testpatch/parser/FAIL-PASS grade or solver ran. This is
prospective compatibility service evidence with a recorded fixture correction,
not Docker/OCI/amd64-kernel/default-trust/full-endpoint parity or retroactive pass
for old declined Mac grades. Whole8skill quality/lower model input+output tokens/
faster completion still require independent scoped model/resource comparisons.

한국어: 실제 Linux 환경에서 HTTP·신뢰한 HTTPS 성공, 잘못된 CA·호스트 거부를
확인했다. 첫 HTTPS 응답의 http 스킴 오류를 보존하고 서비스의 요청별 WSGI
설정만 수정해 두 스킴의 응답을 정확히 맞췄다. 검증 비활성화·전역 신뢰 변경은
없고 키는 비공개다. 공식 선택 과제·모델·토큰 절감 측정은0회다.
