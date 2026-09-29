# External bundle02 — native HTTP/TLS fixture, 2026-09-27

Parent `0713be2f`; skill resource stays `7172b50c`. Author preparation only,
zero model calls or selected issue/performance claims. Original Requests3362
source/base and test bodies remain unchanged.

Inspect actual pinned pytest-httpbin0.2.0/httpbin0.4.1/pytest-mock0.11.0 wheel
sources and metadata before installation. The plugin supplies loopback HTTP/HTTPS
fixtures through its existing WSGI server. Download exact wheels and a compatible
pinned Flask1.1.4/Werkzeug1.0.1/Jinja2 stack into owned storage, then install offline
in the earlier dedicated pytest2.8 environment. No global/existing user packages
change. [Requirements](results/external-bundle-02-httpbin-native/requirements.txt),
[wheel hashes/install statuses](results/external-bundle-02-httpbin-native/server-summary.json)
and actual freeze are retained; pip check passes. These dependency versions differ
from the entire historical lockfile; complete compatibility remains unproven.

First author probe explicitly registers the plugin while pytest2.8 also autoloads
it, causing duplicate registration before tests. Preserve this setup failure.
Remove redundant explicit registration, not plugin functionality. Actual original
fixture HTTP request now passes; trusted HTTPS fails with certificate expiry.
The original bundled CA lasts until2045 but server certificate expired2025-06-23.
Native output explicitly reports `certificate has expired`;1 passed/1 failed.
Server threads stop after fixture teardown. This is a fixture failure, not an
application/agent error. Old pytest does not honor the modern autoload-disable flag.

Generate an owned local CA (30days) and RSA2048 leaf (2days), signed with SHA256,
using bounded OpenSSL subprocesses. Preserve legacy server CN127.0.0.1/no SAN so
original hostname/warning contracts can still be checked. Replace **only**
cacert.pem/cert.pem/key.pem in the owned installed pytest-httpbin fixture, retaining
before/after SHA256s. No application/test/plugin Python source edits or verify=False
are used. Public certificate metadata and certificates are retained; private keys
remain local with restricted permissions and are never exported. Leaf validity is
2026-09-27 00:54:46 UTC through2026-09-29 00:54:46 UTC; revalidate or refresh before
future execution, do not infer permanent readiness from today's result.

Fresh native source-bound Requests2.10 with pytest2.8/plain runs4 authored controls:
HTTP200 with echoed URL; HTTPS200 with the fixture CA; rejection of untrusted CA;
rejection of localhost against the127.0.0.1 certificate. All4 pass; retained control source asserts actual native trust/hostname exception
text, and server threads join and terminate. Plain mode retains assertions but changes rewriting/diagnostics;
this still is not an adopted evaluation runtime. Original expired-fixture attempts
are retained alongside the new results, not overwritten.

Next run three **unchanged original project tests**: GET alternative, GET params,
and HTTPS warnings. All3 pass, including its SubjectAltNameWarning contract; public
Requests source provenance is asserted in the same test process.140 archived file
bytes remain identical afterward. No full suite, selected issue regression, mock
fixture behavior or other Requests version's HTTP service is established here.

[All probe outcomes](results/external-bundle-02-httpbin-native/), original-byte hash
manifests and deterministic path-redacted gzip reading logs retain setup/expiry
failures and actual successful controls/project checks. All processes/server
threads have terminated; no production service/configuration changes. TLS uses
local trusted certificates rather than disabled verification. Loopback fixtures
are not OS-level network isolation; hard-coded external endpoints in other suites
still require an explicit verified treatment without changing their tests.

Next validate complete selected issue tests outside solver contexts, other-version
services, mock fixture behavior, solver snapshot/history isolation and reproducible
runtime/protocol gates. Whole-task token/time and all8 role quality improvement
remain unproven. Featured graphs/site/skill READMEs remain unchanged.

한국어: 원래 플러그인의 HTTP는 동작했지만 HTTPS는2025년에 만료된 인증서로
실패했다. 중복 플러그인 등록 실패와 만료 실패를 보존하고 임시 환경의 인증서만
갱신했다. HTTP·HTTPS 성공/신뢰하지 않은 CA 거부/호스트 불일치 거부4개와
원본 네트워크 검사3개가 통과했다. 인증서 만료 재검사와 전체 필수 검사·모델
효율 검증은 남아 있으며 검증 비활성화나 프로젝트 소스 수정은 하지 않았다.
