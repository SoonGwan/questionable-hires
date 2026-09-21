# Offline build inputs and internal HTTP service

2026-09-21, parent`a91f235`. Author environment preflight only. Same two selected
instances, source/gold/test patches and evaluation scripts as the
[unsuccessful attempts](SWE-LITE-PILOT-01-SCORING-PREFLIGHT.md). No model calls,
skill change, scoring-label removal or new performance claim.

## Concrete environment repairs

pytest's original pyproject requires setuptools>=40.0, setuptools-scm and wheel.
Its image already has setuptools75.1.0 and wheel0.44.0 but no installed SCM helper.
Three universal wheels are copied into each fresh grader's `/opt/wheelhouse`:
setuptools75.1.0, wheel0.44.0, setuptools-scm3.5.0. The latter is a historical
version compatible with the project's era, not a task-source modification.
[Exact downloaded hashes](results/swe-lite-pilot-01-services/wheel-hashes.json)
are retained; packages are not vendored into the public repository. Setting
`PIP_NO_INDEX=1` and `PIP_FIND_LINKS=/opt/wheelhouse` permits the unchanged
evaluation script's build-isolated installation without external network access.

Requests' base tests already support `HTTPBIN_URL`. The
[documented HTTP service](https://httpbin.org/) runs locally from
`kennethreitz/httpbin@sha256:599fe5e5073102dbb0ee3dbb65f049dab44fa9fc251f6835c9990f8fb196a72b`.
The source image's amd64 runtime is used in compatibility mode, with512MB/1CPU,
read-only rootfs and temporary `/tmp`. A new Docker internal-only network connects
this service and Requests graders; no host ports or mounts, no external route.
An actual `/get` request returns200 and the expected local URL. Requests receives
`HTTPBIN_URL=http://httpbin/`; pytest remains on `--network none`.

## Attempt03 outcomes

[Aggregate statuses](results/swe-lite-pilot-01-services/attempt-03.json),
[installation checks](results/swe-lite-pilot-01-services/installation-check.json)
and [executed driver](results/swe-lite-pilot-01-services/preflight-driver.py):

| Project / source | Fail-to-pass group | Pass-to-pass group |
| --- | --- | --- |
| pytest original |1 failed|77 passed|
| pytest gold |1 passed|77 passed|
| Requests original |6 passed /2 failed|127 passed /6 failed|
| Requests gold |7 passed /1 failed|127 passed /6 failed|

All four installation stages contain one success marker and no `ERROR:` marker;
this repairs the previously observed pytest dependency failure. Native output
groups are complete with no missing labels. pytest satisfies the expected
unfixed/fixed distinction and all78 gold checks, **not a model-generated repair**.

Requests remains unsuitable for scoring: its gold version still fails7 required
checks. Base code already passes6 of the nominal fail-to-pass labels under this
environment; do not describe8 newly repaired behaviors. The unmodified base test
file includes hard-coded `https://httpbin.org` targets outside `HTTPBIN_URL`, so
an HTTP-only alias is insufficient. That observation does not establish that
HTTPS alone explains all remaining failures. Diagnose actual native failures and
service compatibility; do not drop checks or replace the chosen instance.

The official evaluation scripts' final shell exits are0 in all four cells, again
not their grade. Counts use the same selected official parser code and delimiters
as attempt02, not complete official harness execution. Timing under emulation is
not a native-performance result. Original private logs/answer-bearing materials
stay local; exported aggregates retain hashes.

## Remaining gates and cleanup

The service was stopped after all four grader containers terminated; the unrelated
database container remains untouched. Images/network are retained locally for
reproduction, not published. Prior failed attempts remain unchanged.

Next establish a service configuration that satisfies Requests' unchanged checks,
then verify same-process package provenance and solver-facing access constraints.
The derived solver image also needs the validated environment inputs; successful
grading setup alone does not certify the solver runtime. No comparison is launched
until both tasks satisfy these gates. Featured/EN/KO graphs remain frozen.

한국어: pytest의 오프라인 빌드 의존성을 고정해 설치 오류를 해결했고, 기준 패치의
필수78개 검사 통과를 확인했다. Requests는 내부 HTTP 서버로 실패가 줄었지만
기준 패치도7개 실패하므로 미완료다. 실제 스킬 성능으로 계산하지 않으며 테스트나
과제를 교체하지 않았다. 사용한 내부 서버는 검사 후 중지했다.
