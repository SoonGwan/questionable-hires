# Requests network contracts: redirect and connect-timeout controls

2026-09-21, parent`eb0afbf`. Author environment work following
[native diagnosis](SWE-LITE-PILOT-01-REQUESTS-DIAGNOSIS.md). No source/test edits,
gold patch, model call or benchmark promotion.

## Isolated topology

Existing Docker networks used172.17–20 subnets; no inspected network overlapped
the new internal-only10.255.255.0/24 subnet. Gateway is10.255.255.254. The pinned
httpbin image runs at10.255.255.2 with aliases`httpbin`, `httpbin.org` and
`www.google.co.uk`, no published host ports or host mounts. These aliases are
local fixture endpoints, not connections to the real named websites.

The unchanged public redirect test follows an HTTP redirect to`www.google.co.uk`
and asserts that the actual Requests client removes its Authorization header.
It does not assert Google response content. The service supplies a different-host
destination while retaining real redirect/header handling; no passing response
or client behavior is mocked. Connect-timeout tests retain their original
`10.255.255.1` target and exception checks.

## Actual attempts

[Original logs, commands and state](results/swe-lite-pilot-01-network/):

- Default client address allocation: redirect and basic control pass, both
  timeout checks fail with connection-refused rather than timeout;2pass/2fail,
  3.61s,exit1. This attempt remains failed. Its live assigned address was not
  captured; post-exit inspection clears dynamic address fields, so do not claim
  a directly observed assignment to the target address.
- Explicit client address10.255.255.3: same image, source, tests, server and
  arguments; all4pass,1.56s,exit0. This reserves the client away from the target
  and demonstrates the required timeout behavior in that observed topology.

The four checks are the unchanged off-host-auth redirect, connect timeout,
total/connect timeout and basic-request construction. No whole-suite or hidden
scoring pass follows. Future containers need explicit non-target addresses;
network emulation/host scheduling can affect timeout behavior, so combined
preflight must still exercise these checks. No model-cost inference from timings.

## HTTPS is still unfinished

The current Requests runtime returns `/testbed/requests/cacert.pem` from both
`requests.certs.where()` and `DEFAULT_CA_BUNDLE_PATH`. Base code optionally uses
an installed `certifi` provider, otherwise that bundled file. Some native tests
prepare requests and call `Session.send` directly; these do not go through the
environment-merge path that reads`REQUESTS_CA_BUNDLE`.

Therefore merely setting that environment variable is not enough to prove private
TLS trust for all unchanged tests. Configure a scoped runtime trust provider,
preserve project source, and test both accepted certificates and rejected untrusted
or wrong-host certificates. Do not disable verification or change the host trust
store. No certificates/trust settings were changed in this checkpoint.

The HTTP service is now stopped; all owned diagnostic containers are terminal.
The dedicated network/images remain local for reproduction. Existing networks
and the unrelated database container were not modified. The Requests gold
preflight remains failed until the combined environment is checked in full.

한국어: 별도 내부 네트워크에서 기존 리다이렉트·타임아웃 검사와 대조 검사4개가
통과했다. 주소 자동 할당 상태의 실패도 보존했다. HTTPS 인증서 신뢰는 아직
미완료이며 호스트 신뢰 저장소나 프로젝트 코드는 변경하지 않았다. 전체 채점이나
스킬 성능 검증 결과는 아니고, 검사 후 내부 서버를 중지했다.
