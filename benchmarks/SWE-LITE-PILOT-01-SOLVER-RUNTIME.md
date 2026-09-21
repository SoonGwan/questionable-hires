# SWE-Lite pilot01: solver runtime preparation

2026-09-22; implementation `365fea9`, based on `299cdf6`.
**No model calls, skill efficiency result or public release.**

## What changed

Built separate solver images from the previously verified [base-only images](SWE-LITE-PILOT-01-ISOLATION.md),
not from any gold/scoring container. Each keeps the original tracked source tree,
one fresh Git commit and no remote. Added Codex CLI0.153.4, the same CLI release
as earlier comparisons. Requests receives only the dependency/TLS repairs already
validated in [combined reference grading](SWE-LITE-PILOT-01-SCORING-04.md).
The separate pytest runtime keeps its original pytest version.

The [context builder](swe-lite-runtime/stage.py) copies an explicit wheel
allowlist, verifies every wheel against retained preflight SHA256 values, and
copies only the public CA certificate plus the build recipe. It never traverses
the scoring directory or copies auth/private keys. Four synthetic tests check
exact inventory, exclusive output creation, changed/linked wheel rejection,
manifest path traversal and private-key rejection. All4 pass in the checkout and
in a fresh source-only copy without Git history/local artifacts.

Recipe: [Dockerfile](swe-lite-runtime/Dockerfile),
[dependency preparation](swe-lite-runtime/prepare.py),
[public-source probe](swe-lite-runtime/smoke.py).

## Observed runtime checks

Both probes used Linux/amd64 compatibility mode, Python3.9.20,2CPU/2GiB/256PID
limits, all capabilities dropped and no-new-privileges. There were no host
mounts, Docker socket or authentication files supplied. Each verifies a fresh
public-package import, then native collection in the same process with every
test module's package reference bound to the project import. Tracked source
diffs remain empty before/after. These are public original tests, not hidden
grading tests or model-produced fixes.

| Project | Same-process native result | Container process exit |
| --- | --- | --- |
| Requests |142pass,3warnings; all142 bindings checked;8.77s |0 |
| pytest |77pass; all77 bindings checked;14.88s |0 |

Times describe author smoke tests, not comparable solver latency. Requests used
the previously prepared internal TLS service at10.255.255.4 and explicit client
10.255.255.5; pytest used network-none. The TLS service was stopped afterward.
CA expiry remains2026-10-21T14:59:54Z; validate before reuse, never bypass TLS.

Logs: [Requests](results/swe-lite-pilot-01-solver-runtime/requests.log),
[pytest](results/swe-lite-pilot-01-solver-runtime/pytest.log).
Their SHA256 values are respectively
`91535edfb4fde5e8491294b354f0fca0d8edeb8c57423be6666b339902c795be` and
`173fd4b49e68423d026e49eae976ea631175ec846ab7eeb90ed2dd1bab4a56f7`.

## Frozen local artifacts, not portable image publication

Requests `qh-swe-lite-requests:solver-01` image ID:
`sha256:18a37ed6f5179b655c81ae5c5d9c47c1d8677762cba417ee661c5c66dc2c2d8d`.
pytest `qh-swe-lite-pytest:solver-01` image ID:
`sha256:34f351fda2c7ba6644ebacc03822fbc78d8e0a294cba5360fe91c76460633923`.

The CLI executable SHA256 in both images is
`56ef98ab4032d317ab26e9b5e5a175650717351edb16ed9cde0cb6d1734d62da`.
Downloaded installer SHA256 in both probes is
`dd4282a1a3c8188f792513f2f16afb852e63ce3b98dbbc67684f716ebcc1e862`.
Installation requested0.153.4 and checked `codex --version`; it made no model
request and received no credentials. The installer URL is mutable, so this is
an identity record for the local built images, not a bit-reproducible rebuild
claim. Docker warns that BASE_IMAGE lacks a default; both builds explicitly
supplied and resolved the documented local base image. Nothing was pushed to
a container registry.

## Remaining gates / next action

The existing browser runner already launches the model itself in a container;
reuse its launcher boundary, not a host-side Python path-rewriting wrapper.
Consulted [official Codex security documentation](https://learn.chatgpt.com/docs/security)
and installed CLI0.153.4 help before choosing the execution boundary.

Before the four predeclared model cells, verify the actual launcher with
per-cell source/state, generated pytest metadata, credential handling, timeout
cleanup and retained initial-message evidence. No solver has yet been launched
from these images. Model API connectivity is also not established: internal-only
test networking cannot reach the API, while giving the container external
network access is not enforced solution-lookup prevention. Freeze and disclose
the chosen network policy rather than claiming strict network isolation.
One-commit source preparation does not certify an exhaustive search of every
inherited image file/layer for solution-bearing artifacts.

한국어: 모델이 사용할 이미지 두 개에서 실제 프로젝트 소스에 연결된 원본 테스트
142개/77개가 통과했다. 정답 패치가 들어간 채점 컨테이너는 재사용하지 않았다.
다만 모델 실행·접근 경계 검증과 비교 실험은 아직 남아 있으며, 스킬 성능 향상이나
배포 완료로 해석하지 않는다. 기존 그래프와 불리한 결과도 변경하지 않았다.
