# Owned official HTTP01 — actual loopback and missing service packages

Dated checkpoint **2026-09-27**, protocol/resource`b643b7d2`,parent`cace5b51`.
[Protocol](OWNED-OFFICIAL-HTTP-01-PROTOCOL.md),
[actual native outcome](results/owned-official-http-01/result.json).
Zero models and selected-case tests;8skills and featured data unchanged.

## Observed upstream-image behavior

The actual official source interpreter imports Requests from
`/testbed/requests/__init__.py`, unchanged opaque file SHA256
`364d408838c8073cab46f4846cefaabb03c5b8d18b530c6d8d563f4d6a3920bf`.
Explicit guest-only loopback interface activation returns0. An authored stdlib
HTTPServer binds127.0.0.1 at a dynamic port; actual project Requests GET of the
fixed health endpoint returns **200** and exact body`QH_OFFICIAL_HTTP_OK`.
Native server thread shuts down/joins, socket closes. VM/controller0, all routing/
device/loopback statuses0, guest stop, no timeout, **5.85 seconds**. First attempt
succeeds for this narrow control, without retry.

Direct native imports of **httpbin,pytest_httpbin,flask,werkzeug,mock** all raise
ModuleNotFoundError in the official image. This is observed import absence, not
metadata guesswork; no package is installed/replaced to hide it. Passing
[original collection](OWNED-OFFICIAL-COLLECTION-01.md) does not imply these packages
exist or that full HTTPbin/TLS service is ready. Their absence does not establish
a defect in the official image: service dependencies may belong in an external
service environment. `mock` may likewise be optional for original fixture logic;
collection did not require importing it under that name.

The existing [Mac HTTPbin/dual-service controls](EXTERNAL-BUNDLE-02-RUNTIME-CONTROLS-02.md)
use a separately pinned Flask/httpbin stack. Their package/source availability and
native TLS success cannot be relabeled as executable Linux service readiness.
This simple health server proves loopback transport/client cleanup **only**, not
HTTPbin endpoints, mixed-scheme behavior, TLS/default trust, proxy or official
required tests. It must not replace the required service with an easier health
endpoint for grading. A separately frozen Linux service prefix/sidecar, preserving
the client image environment, is the next preparation option.

## Execution and resource boundaries

[Probe](results/owned-official-http-01/fixture/probe.py),
[VM](results/owned-official-http-01/probe.swift),
[controller](results/owned-official-http-01/control.py),
[resource hashes](results/owned-official-http-01/resource-hashes.json).
Root/probe shares readonly; guest proc/dev/tmp/binfmt/loopback changes are disposable,
not host installation/configuration.1CPU/1GiB, no NIC or block device. Request
3-second timeout, native server shutdown/join3 seconds, guest180s/independent parent
200s process-group watchdog; all processes terminate and root volume detached.

Public observation contains only authored body, source/import paths, module error
types and opaque identities; no external issue/test/gold/script/label body is
exported. Original raw console remains private with its byte hash in the outcome.
No selected testpatch/native grading, no base/gold repeat/rescore or solver run.
Earlier adverse Requests2674 local-service results remain declined, and original
HEAD/mode limits remain. General8skill quality/lower whole-task tokens/faster time
still require actual fresh model/quality/resource comparisons; this gate is not
an efficiency gain or release adoption.

한국어: 공식 소스의 Requests가 게스트 루프백에서 실제 HTTP200·지정 본문을
받고 서버 스레드·소켓을 정상 종료했다. 그러나 기존 HTTPbin 서비스 패키지는
이미지에서 모두 import 불가였다. 별도 서비스가 필요할 수 있으므로 이미지의
결함이나 공식 테스트 준비 완료로 단정하지 않는다. 단순 상태 응답을 전체
HTTPbin/TLS 대신 쓰지 않으며 모델·선택 과제·토큰 절감 측정은0회다.
