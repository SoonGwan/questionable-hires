# Requests combined environment: gold contract passes

2026-09-22 KST, parent`f487972`. Two fresh **author preflight** cells, original
then gold, with the selected Requests instance unchanged. No model calls, no
new skill revision and no performance comparison.

## Combined runtime

Use the same pinned official Requests image/source and dataset evaluation script
as earlier attempts. Apply the validated Requests-only pytest/dependency pins,
certifi2024.8.30 with the ephemeral scoped CA, and the pinned HTTP/HTTPS service
on the internal-only contract network. Explicit client addresses are10.255.255.7
and.8, away from the timeout target. Offline build wheels remain available.
No external network, host mounts, published service ports, source/test rewrites
or disabled certificate verification. The exact
[driver](results/swe-lite-pilot-01-scoring-04/preflight-driver.py),
[trust setup](results/swe-lite-pilot-01-scoring-04/trust-runtime.py) and
[native provenance hook](results/swe-lite-pilot-01-scoring-04/qh_provenance.py)
are retained. Inputs/hashes are linked from the preceding
[TLS](SWE-LITE-PILOT-01-TLS.md), [runner](SWE-LITE-PILOT-01-REQUESTS-DIAGNOSIS.md)
and [build/service](SWE-LITE-PILOT-01-SERVICES.md) reports.

## Observed results

[Aggregate scoring](results/swe-lite-pilot-01-scoring-04/summary.json):

| Source | Dataset fail-to-pass group | Dataset pass-to-pass group | Full native execution |
| --- | --- | --- | --- |
| Original |7passed /1failed|133passed|142passed /1failed|
| Gold |8passed|133passed|143passed|

The required groups contain141 labels; the actual selected native file executes
143 items. Two additional native passes are not counted as extra required labels.
Seven nominal fail-to-pass cases already pass on original code in this environment;
the observed distinguishing transition is **one failure to one pass**, not eight
new fixes. Both groups have no missing, skipped or error labels. Native timings
8.58s/8.24s are author-run observations, not a skill-speed result.

[Setup and same-process evidence](results/swe-lite-pilot-01-scoring-04/setup-and-bindings.json)
records a successful reinstall and no setup `ERROR:` markers in both cells.
Both collection hooks verify all143 items come from `/testbed/test_requests.py`,
whose actual `requests` binding is the package at`/testbed/requests/__init__.py`.
The hook fails collection on a mismatch; it does not replace assertions or tests.
The unchanged dataset evaluation script still ends with shell exit0 for both
versions, so statuses—not that exit code—establish the distinguishing failure.

Scoring still uses selected unchanged official parser functions, not the entire
official harness. Original answer-bearing logs remain private with published
hashes. No patch/test labels are exported, and the coordinator's author-side
review is not represented as blind validation. All prior permission, dependency,
network and runner failures remain in their original reports.

## Decision

Requests now meets the scoped original/gold scoring preflight. The separate pytest
task's attempt03 already has successful setup and78 gold passes with its one
original failure; that result is not rerun or relabeled here. These are reference
patches, not model-produced solutions or evidence that the skills improve outcomes.

Before the four baseline/skill sessions: freeze solver-only runtime/source inputs,
exclude scoring artifacts and upstream Git stores, validate the actual solver
execution path, and freeze settings/order/ceilings/capture. Do not use these author
outcomes as the model comparison, expand the sample for favorable results, or
change featured graphs. All grader containers are terminal and the HTTP/HTTPS
service has been stopped again; the unrelated database service was untouched.

한국어: Requests 원본은 필수 검사 중1개 실패, 기준 패치는141개 전부 통과했다.
실제 실행은 추가 검사2개를 포함해143개이며 테스트와 패키지의 동일 프로세스
연결을 확인했다. 이제 기준 패치 채점 조건은 충족하지만 실제 모델·스킬 비교는
아직 실행하지 않았다. 이전 실패와 그래프 수치를 그대로 보존한다.
