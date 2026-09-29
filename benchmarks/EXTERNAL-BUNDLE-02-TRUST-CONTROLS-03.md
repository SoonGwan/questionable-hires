# Requests native default trust controls03 — 2026-09-27

Parent `202ee64a`, unchanged skills `7172b50c`, five native author client controls,
zero models. [Evidence](results/external-bundle-02-trust-controls-03/) preserves
authored client source, scalar results, native exits and original output hashes.
Client uses the original archived Requests2674 source with the same owned
Apple Python3.9 legacy environment as the case probe. A real owned dual HTTP/TLS
WSGI service uses the existing checked private certificate/key assets.

| Controlled call | Native result |
| --- | --- |
| Higher-level GET with CA environment setting |200,exit0 |
| Direct Session.send with same setting and ordinary default CA |Certificate verification rejected,exit1 |
| Direct send with explicit test CA |200,exit0 |
| Direct send with private copied certifi default CA extended by test CA |200,exit0 |
| Same extended default CA with wrong hostname |Hostname rejected,exit1 |

The certifi package is copied into a disposable runtime directory. Only its
cacert.pem asset is extended; every certifi Python file remains byte-identical,
original environment files/global trust stay unchanged. CA file hashes identify
both variants. Requests' native default CA lookup uses the copied package through
normal PYTHONPATH resolution; verification is never disabled. Service termination
completes exit0 with no timeout. Certificate private keys and raw helper errors
remain local. Source/test/gold Python is never edited by these controls.

This distinguishes environment merging from direct default verification and
provides a compatible owned fixture trust route. It does not establish the full
case's original FAIL_TO_PASS contrast or repair, nor rescore previous failures.
The eleven already-passing designated failures remain independently unresolved.
Freeze any new full-case default-trust preparation separately before execution.

한국어: 같은 원본 클라이언트에서 상위 요청의 CA 환경 설정은 통과하고 직접
send는 거부됐다. 명시적 CA와 별도 복사한 런타임 기본 CA 확장은 통과했으며
잘못된 호스트는 계속 거부됐다. Python 코드·원본 런타임·시스템 신뢰 저장소를
바꾸지 않았다. 전체 사례 검증이나 모델 품질·작업 토큰·시간 절감은 아직 아니다.
