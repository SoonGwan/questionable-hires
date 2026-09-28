# pytest5221 offline-build pair02 — 2026-09-28

**The scoped original-script native gate passes with declared offline build inputs.**
Both fresh cells complete editable installation successfully. The unchanged official
parser records base2 required failures+170 required passes and gold172 required
passes. The corrected observer records only the173 primary items, with native
pytest exits1/0. This is author-side grading readiness for one existing case,
not a model repair, all-eight readiness or a token/time improvement.

[Protocol](EXTERNAL-BUNDLE-02-PYTEST5221-CONTAINER-02-PROTOCOL.md) `6ff5e783`,
input-readability correction `da7d8bcf`, completed controls/frozen driver hashes
`d06f8e54`, parent `16d3e665`. The rejected [pair01](EXTERNAL-BUNDLE-02-PYTEST5221-CONTAINER-01.md)
remains unchanged: tests separated there, but both editable installations failed
and the original observer mixed nested pytester reports into its aggregation.
This distinct pair changes the offline build inputs and observer; neither cell
is an unchanged retry of pair01, and neither is rerun or replaced.

| Original observed result | Base | Gold |
| --- | --- | --- |
| Editable installation success marker / ERROR diagnostics |present /0|present /0|
| FAIL_TO_PASS, unchanged2 labels |2 failed|2 passed|
| PASS_TO_PASS, unchanged170 labels |170 passed|170 passed|
| Primary collected items |173|173|
| Extra primary item |1 xfail|1 xfail|
| Primary setup/teardown failures |0|0|
| Actual pytest session exit |1|0|
| Official shell / container exit |0 /0|0 /0|
| Declared native variant contract |pass|pass|

[Original summaries](results/external-bundle-02-pytest5221-container02/grade-summary.json)
retain actual versions, counts and private output/observer hashes.
[Execution states](results/external-bundle-02-pytest5221-container02/pair-native.json)
retain both terminal states and limits. Shell exit alone is never the grade:
the official script does not enable errexit. Per-cell installation evidence is the
unaltered original output's success marker and zero ERROR diagnostics; the separate
preflight captures an actual installation subprocess exit0. This does not claim
execution of the entire upstream SWE-bench harness or its infrastructure parity.

## What changed and what was verified

Reuse the exact already-loaded image config
`1718609d2c1e3a6d929eb4643f8474ee9e8f551cab77847f6c492dd0df6f1701`, all10 ordered diffIDs
verified against pair01. No image download/tag refresh. The historical
[SWE pilot offline recipe](SWE-LITE-PILOT-01-SERVICES.md) already solves this class
of build failure. Its old wheel directory is absent, so acquire the same three
universal wheels with the same frozen hashes: setuptools75.1.0,
setuptools-scm3.5.0 and wheel0.44.0, total1,341,745bytes.
[Wheel identities](results/external-bundle-02-pytest5221-container02/wheels.json)
include exact source URLs and hashes; every actual container verifies those bytes.
PIP_NO_INDEX=1 and PIP_FIND_LINKS=/qh/wheelhouse supply the unchanged build-isolated
`python -m pip install -e .`. No host install or container network access.
This explicitly prepared build environment differs from default image dependencies.

The first preflight stops before pip on PermissionError reading the copied public
wheel manifest. Preserve its [original diagnostic](results/external-bundle-02-pytest5221-container02/preflight-native.stderr).
Public dependency files become0644 and their directory0755 within the enclosing
private author root0700. No private patch/log permissions or runtime protections
change. A fresh preflight then installs successfully and exercises actual pytest
pass0, assertion-fail1 and an outer-pass/inner-fail nested control. The nested
control's native inner exit1 and `assert 41 == 42` are visible in the
[original authored control output](results/external-bundle-02-pytest5221-container02/controls/nested.stdout),
while its observer records exactly one passing outer item and three phase reports.
All [raw authored controls](results/external-bundle-02-pytest5221-container02/controls/)
and their hashes are retained; they are not selected-issue results.

The [observer](results/external-bundle-02-pytest5221-container02/qh_pair_observer.py)
uses the actual item.session identity in a makereport hookwrapper, not filename
filtering or status renaming. Both issue cells have exactly519 reports for173
unique primary items, one setup/call/teardown each. The
[post-run consistency check](results/external-bundle-02-pytest5221-container02/observer-consistency.json)
confirms all belong to the evaluated file. No post-run filtering is needed to
accept these original counts; pair01's incorrect aggregation stays historical.

Before and after preflight installation, all433 selected archive file bytes match.
The existing image's synthetic Git HEAD `c0698ad6368fb4dfda4e3d2b8dab498874793848`
and432 executable-mode differences from the archive remain explicit pair01 limits.
The build regenerates version metadata: preflight/base actually import
`4.4.2.dev175+gc0698ad6`, gold imports
`4.4.2.dev175+gc0698ad6.d20260928`, all from `/testbed/src/pytest.py` using Python3.9.20.
The gold dirty suffix is recorded, not normalized to selected-base metadata.
Preflight before/after generated-file hashes differ and are retained in the
[original control summary](results/external-bundle-02-pytest5221-container02/preflight02-native.stdout).
No manually fabricated version file or test/source assertion repair is used.

## Scope and cleanup

Both original cells use the same image, wheelhouse, environment and observer;
only gold receives the original gold patch. Official evaluation script hash
`950987985c71231ea07667924061f204b67af5d249098b35833f08e5fa05fad3`, embedded test patch,
required labels and official parser remain unchanged. All executed driver hashes
match their pre-issue [freeze](results/external-bundle-02-pytest5221-container02/freeze.json).
Private grading logs, labels and patches stay outside the repository and solvers.

Network none, no host mounts, cap-drop ALL, no-new-privileges, default seccomp,
writable disposable root,1GiB/1CPU/64PIDs remain. Zero timeout/OOM/protection
relaxation. [Cleanup](results/external-bundle-02-pytest5221-container02/cleanup.json)
confirms zero containers, inactive/disabled guest services, VM Stopped and no owned
Lima/SSH processes. Per-cell elapsed time is administrative evidence under Rosetta,
not a model performance comparison or an optimization claim against failed pair01.

The [model execution authorization blocker](SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md)
and other selected-case grading limits remain. This is one already-exposed author's
base/gold pair, not independent validation, host-tool isolation proof, all8 quality
superiority or measured savings. Model calls0; skills, featured benchmark, README
onboarding and hosted landing release are unchanged. Whole-task improvement remains
unproven. Carry the prepared dependencies and proven observer into later distinct
native protocols without repeating this accepted pair merely for another result.

한국어: 고정한 오프라인 의존성으로 실제 설치가 성공했고, 원본2개 실패·170개
통과와 정답172개 통과를 원본 파서로 확인했다. 관찰기는 최상위173개 항목의
519개 보고만 기록하며 중첩 실패가 섞이지 않는 대조군도 통과했다. 최초 권한
오류와 이전 설치 실패를 보존하고, 빌드가 생성한 실제 버전 차이도 공개한다.
해당1개 사례의 선언된 네이티브 평가 조건만 통과한 것이며 모델 호출·토큰 절감·
전체8개 개선으로 계산하지 않는다. 컨테이너·서비스·VM 종료를 확인했다.
