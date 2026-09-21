# Scoped HTTPS trust and complete native Requests controls

2026-09-22 KST, parent`dfbe182`. Continues the
[network contract work](SWE-LITE-PILOT-01-NETWORK.md). No task/gold/test patch
changes, model sessions or claimed skill savings.

## Fixture, not disabled verification

The pinned httpbin image serves actual HTTP80 and HTTPS443 on the existing
internal-only Docker network at10.255.255.4. Gunicorn processes share the same
unmodified app. Aliases include`httpbin`, `httpbin.org`, the existing cross-host
redirect destination and a deliberately wrong TLS hostname. No published ports
or host mounts. Clients use explicit10.255.255.5/.6, away from the timeout target.

An ephemeral local CA signs the server certificate for exactly`httpbin` and
`httpbin.org`. Certificate validity is2026-09-21 14:59:54 UTC through
2026-10-21 14:59:54 UTC. Later reproduction must check validity, not silently
disable expiry checks. Public certificates/configuration are retained in
[the evidence directory](results/swe-lite-pilot-01-tls/); private keys stay local
under a0700 directory with0600 host file modes and are never exported. Server
key copies exist only in the isolated fixture container; this is not a production
PKI, host trust change or a certificate for public service deployment.

Install certifi2024.8.30 alongside the already validated Requests-only dependency
pins, then add this CA to that container's certifi data bundle. Requests' existing
optional-certifi path supplies the default trust bundle, including direct
`Session.send` callers. No Requests source or bundled source certificate is edited;
verification remains enabled. This is a custom runtime trust fixture, not an
assertion that the dependency bundle is pristine upstream data.

## Observed controls and an exposure correction

First attempt: private-CA rejection, trusted HTTPS success and wrong-host rejection
work; a separate native invocation passes142tests,24warnings,8.30s. Its explicit
TLS probe imports the installed Requests copy, not `/testbed`, because its script
resides under`/fixture`. This limits that first control's provenance and is retained
in the original log/source, not silently relabeled as project-bound evidence.

Second fresh client adds explicit`PYTHONPATH=/testbed` and asserts the imported
package path. In **one process** it performs the TLS controls, then calls native
pytest with a collection hook that checks all142 items' actual test-module path
and `item.module.requests is requests` binding:

- Before adding the fixture CA: the real TLS request raises`SSLError`.
- With the CA: a direct prepared-request send to the correct host returns200 and
  the expected HTTPS URL, without passing`verify=False`.
- The same certificate on the wrong hostname raises a hostname-related`SSLError`.
- Complete original native file: **142passed**,2deprecation warnings,7.79s,exit0.
- Tracked-project diff is empty before and after native tests.

Both exact executed control sources and original logs/commands are retained.
Different warning counts reflect earlier imports in the second process, not
removed tests. No timing comparison or model-cost conclusion follows.

## What remains

This verifies original public tests in the combined Requests runtime. It does not
replace the selected dataset's separate fail-to-pass/pass-to-pass contract. Gold
grading must now use these same compatible dependencies, scoped trust and service
conditions, preserving every prior failed attempt. Solver-facing access and final
execution-protocol checks remain pending. The separate pytest task's successful
preflight is unchanged; no new skill capability or graph value is claimed.

The service was stopped after verification; all owned TLS clients are terminal.
Existing source images and the unrelated database service remain untouched. No
public/private key is installed in the host trust store and no image is published.

한국어: 실험용 인증서를 컨테이너 내부에서만 신뢰하게 설정했다. 프로젝트 소스와
같은 프로세스에서 미신뢰 인증서·잘못된 호스트 거부, 정상 HTTPS 수락, 기존142개
검사 통과를 확인했다. 첫 실행의 설치본 import 한계도 기록했다. 아직 데이터셋
기준 패치의 통합 채점이나 모델 성능 결과가 아니며 내부 서버는 중지했다.
