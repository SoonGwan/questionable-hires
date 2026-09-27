# Owned Linux service01 — actual separate-prefix HTTPbin execution

Dated checkpoint **2026-09-27**, protocol/resource`0b2e8aaf`,parent`f68c1f4d`.
[Protocol](OWNED-LINUX-SERVICE-01-PROTOCOL.md),
[actual native outcome](results/owned-linux-service-01/result.json).
Zero models and selected-case tests;8skills and featured measurements unchanged.

The11 [verified Linux wheels](OWNED-LINUX-SERVICE-WHEELS-01.md) were rechecked,
shared readonly, and installed **offline/no-deps/no-cache/no-compile** by actual
image Python pip into guest tmpfs `/tmp/qh-http-service-lib` only. Installexit0.
No host/global installation or official site-packages write; image root is readonly.
pytest2.8 and pytest-mock are not added. Existing client Python3.9.20/pytest7.4.4
and project source remain unchanged. Install stdout/stderr digests retained;
nonempty stderr is not silently described as warning-free.

A separate native service process, PYTHONPATH set only to this prefix, imports
actual HTTPbin0.4.1,Flask1.1.4,Werkzeug1.0.1,MarkupSafe2.0.1 from that path.
It loads **MarkupSafe `_speedups.cpython-39-x86_64-linux-gnu.so`**. Its actual native
file digest matches the previously verified cp39/x86_64 wheel extension, not just
an ELF-header/target-tag guess. [Post-observation verification](results/owned-linux-service-01/verify_observation.py)
checks this original observation, versions and echoed URL without any native replay.

The service uses the real HTTPbin app and pytest_httpbin WSGI Handler, not a health
stub. It binds guest127.0.0.1/dynamic port; the unchanged official project Requests
in the separate client gets **`/get?control=owned-linux-service` →200**,
exact args and full echoed URL. Source path `/testbed/requests/__init__.py` and
opaque file digest remain unchanged. The client still cannot find httpbin/flask/
werkzeug after prefix installation; service PYTHONPATH is not injected into it.
This observes process/import separation, not a general sandbox security proof.

Native stdin-triggered service shutdown returns0; its thread joins and socket
closes. No forced cleanup. VM/controller0, all loopback/device/routing statuses0,
guest stop, no timeout, **6.983 seconds**. First service execution succeeds,
no retry/version upgrade or source repair. Prior image missing-import observations
remain true for the unmodified client rather than being relabeled as package imports.

[Native driver](results/owned-linux-service-01/fixture/probe.py),
[service](results/owned-linux-service-01/fixture/server.py),
[VM](results/owned-linux-service-01/probe.swift),
[controller](results/owned-linux-service-01/control.py),
[resource hashes](results/owned-linux-service-01/resource-hashes.json).
Reuse the earlier HTTPbin/Handler/WSGIServer lifecycle, adapted to a separate
Linux prefix and native process.1CPU/1GiB,no NIC/block device; only guest loopback,
proc/dev/tmp/binfmt additions. Root/probe shares readonly. Pip30s/ready10s/request3s/
shutdown10s then guest-owned process-group TERM/KILL; guest180s/independent parent
200s watchdog. All processes stop and owned root volume is detached after collection.
Public output contains only authored endpoint/args, module paths and scalar/opaque
identities; original raw console private. No external source/test/gold/script/labels
or keys published.

TLS/default trust/mixed-scheme/hostname/HTTPbin-wide endpoint compatibility,
official evaluation script/parser/required-label base-gold grading and solver
isolation remain unverified. The service is a prospective compatibility environment,
not full OCI/amd64-kernel parity or a retroactive pass for older declined results.
This native service gate is not skill quality, whole-task model token/time saving
or general8skill release adoption. Exact official-case execution needs its own
frozen private resource/variant/cleanup controls.

한국어: 공식 클라이언트 패키지는 그대로 두고 별도 게스트 경로의 HTTPbin을
실제로 실행했다. 원본 Requests의 실제 `/get` 요청이200·정확한 인자/URL을
받았고 네이티브 확장 바이트도 검증된wheel과 같았다. 서비스 스레드·소켓·
프로세스는 정상 종료했다. TLS·공식 평가·전체 스킬의 품질·토큰·시간 개선은
아직 입증하지 않았으며 모델·선택 과제 실행은0회다.
