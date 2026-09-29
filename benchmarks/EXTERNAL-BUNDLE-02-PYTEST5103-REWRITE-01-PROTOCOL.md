# pytest5103 assertion-loading distinction01 — 2026-09-28

Parent `581c4ef2`. The official pair's two additional primary failures remain a
failed native gate. Static inspection finds both extra tests are added by the
original test patch and expect expanded assertion messages from nested pytest.
Gold adds special handling for the relevant expression shapes. Original output
has plain AssertionError text instead of the requested rendering. Existing image
environment/evaluation flags do not explain this difference. These observations
do not establish a runtime cause, repair or ready benchmark.

Searches of existing pytest5103/cache/runtime reports find no matching loading
distinction. Do not repeat the issue pair, alter its score, discard extra tests or
guess that Python version or cache state caused the failures.

Use one fresh author container from the already pinned official image config
`6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787`.
Reuse the exact three offline wheels and install command from pair01. Verify418
original source hashes, apply the original private gold patch, then verify patched
source bytes survive installation. No test patch or required labels enter this
container. No registry, dependency or model calls.

Freeze six authored diagnostic cells: scalar false, all(generator) false and
all(list-comprehension) false, each through direct AST assertion rewriting and a
fresh native pytest process. The bodies use new simple values and are not issue
tests. Keep all six results, including errors and unexpected passes. Record native
assertmode, import-hook classes, special-handler availability and collected test
bytecode rewrite markers; do not replace or wrap the production rewriter.

Decision boundary: if direct transformation also fails, inspect its actual error
before proposing an import/cache explanation. If direct works but native lacks
rewriting, trace native import dispatch. If both produce expected expanded text,
these authored probes do not reproduce the issue-test context; preserve that limit
and inspect the missing context rather than declaring the original failure fixed.
The scalar control distinguishes a general loader problem from a shape-specific
transformation problem. A native nonzero exit is expected for authored failures,
but its actual assertion content and observation must be present.

Retain network none, no mounts, cap-drop ALL, no-new-privileges, default seccomp,
1GiB/1CPU/64PIDs. Installation90seconds, each diagnostic15seconds, driver180seconds.
Reuse the existing bounded container runner and terminal cleanup; no changed
limits or automatic retry. Remove the container, stop services/VM and verify state.
Record input hashes before execution, and export authored logs/scalars only;
private issue data remains private. This is native diagnosis, not model performance
evidence, full-harness validation or a change to ordinary skills/public metrics.

한국어: 추가 실패를 제거하거나 원본 채점을 반복하지 않는다. 같은 정답 소스에서
직접 AST 변환과 실제 pytest 로딩을 비교하는 간단한 작성자 대조군6개를 고정한다.
실제 오류·로딩 상태가 원인을 구분할 때만 후속 조치를 정하며, 이 진단 자체를
성능 개선이나 외부 사례 통과로 계산하지 않는다.

## Pre-cell storage recovery

The inherited start script stops before services/containers/cells because available
guest space is7,957,454,848bytes, below the unchanged8GiB threshold. Preserve that
startup failure. The already-loaded owned pytest5103 transport archive is redundant:
reverify its host and guest SHA256 against the frozen transport, retain the host
copy and remove only the guest copy (1,025,771,520bytes). Recheck the original
threshold and loaded image identity before continuing the six never-started cells.
This changes cache storage only, not source, environment, limits or diagnostics.
[Recovery evidence](results/external-bundle-02-pytest5103-rewrite01/space-recovery.json).
