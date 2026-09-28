# pytest5221 offline-build pair02 — 2026-09-28

Parent `16d3e665`. Preserve rejected [pair01](EXTERNAL-BUNDLE-02-PYTEST5221-CONTAINER-01.md).
The original issue behavior separated, but build-isolated editable installation
failed offline. This distinct author-only protocol changes the supplied build
inputs and primary-session observation, not the issue, test/gold patches,
required labels, official evaluation script or official parser. Zero model calls.

Reuse the already loaded official image config
`1718609d2c1e3a6d929eb4643f8474ee9e8f551cab77847f6c492dd0df6f1701`; verify its identity
and ordered RootFS against retained pair01 evidence. No image refresh/download.
Reuse the approach and exact three wheel hashes from the historical
[SWE pilot services preparation](SWE-LITE-PILOT-01-SERVICES.md):
setuptools75.1.0, setuptools-scm3.5.0, wheel0.44.0. This is an explicitly prepared
build environment, not the image's default setuptools68.0.0 or a new discovery.
The old local wheel directory is absent. Acquire only those three universal wheels
from PyPI, require the previously frozen SHA256 values, bound total downloads at
5MiB and90seconds, and keep acquisition metadata. No host installation.

Copy this fixed wheelhouse into each disposable container. Set PIP_NO_INDEX=1 and
PIP_FIND_LINKS to that private local path, maintaining original `python -m pip
install -e .` and build isolation. No no-build-isolation flag, dependency assertion
changes or external network. Only wheelhouse build requirements may be installed;
record the actual generated version/package provenance and installation outcome.

Before any issue evaluation, execute the actual editable installation in a fresh
container and require native exit0, its success marker and zero installation
ERROR diagnostics. Verify selected-base bytes before build, then inspect actual
project import and before/after source changes. Generated metadata differences
must be identified, never silently treated as original bytes. Use this same
runtime for passing, intended assertion-failing and nested pytest-session controls.

Replace observer logreport aggregation with hookwrapper observation of reports
whose item.session is the original primary session. Keep native exit and collection
count. A synthetic outer test invoking inner pytest with an intended assertion
failure must pass itself; observer must record only the outer item, while inner
native exit1/assertion diagnostics prove the nested run happened. Also require
ordinary pass0/fail1 controls and corresponding observer records. Validate these
before freezing driver hashes and before running either issue cell. No test labels
are normalized or invented. Preserve all control failures; do not weaken restrictions.

Then execute exactly two fresh original base/gold cells, in that order,180seconds
each. Same image/script/parser as pair01, original gold patch only for gold, same
wheelhouse/environment/observer for both. Accept only successful installation,
source pytest provenance, original2 FAIL_TO_PASS failed/passed, all170 PASS_TO_PASS
passed in both, actual primary pytest exits1/0, no top-level setup/teardown failures,
timeout or OOM. The extra xfail is not a pass. Shell/container exit alone is not a
grade. No unchanged rerun, case substitution or promotion into featured results.

Keep pair01 protections: writable disposable root, network none, no host mounts,
cap-drop ALL, no-new-privileges, default seccomp,1GiB/1CPU/64PIDs. Controls180seconds
including installation; parent watchdogs and cleanup retained. Stop guest services
and VM, verify no containers or owned Lima/SSH processes. Public exports contain
only identities, control diagnostics and scalar summaries; raw issue logs, labels
and patches stay private. Standard-container native readiness does not resolve
the model-tool approval blocker or prove all8/token/time/quality improvement.

한국어: 앞선 실패를 보존하고, 과거에 검증한3개 wheel을 같은 해시로 준비해
원본 설치 명령을 오프라인으로 실행한다. 관찰기는 실제 최상위 session의 항목만
기록하며 중첩 실패 대조군으로 확인한다. 원본/정답을 각1회 검증하고 전체 설치와
필수172개 항목을 모두 확인한다. 실행 제한·기존 실패·모델 비용 구분은 유지한다.

## Input readability correction before build or issue evaluation

The first preflight stops before pip because the transferred public wheel manifest
retains restrictive author file modes and is unreadable by the capability-dropped
container process. Preserve that PermissionError and original logs. Change only
public wheel inputs to readable files0644/directories0755 inside the enclosing
private author root0700; no patch/log exposure or container protection change.
A distinct preflight02 uses the unchanged native driver in a fresh container.
Neither installation nor any issue cell ran in the failed attempt.
