# pytest5221 official-container pair01 — 2026-09-28

Parent `32e0f136`. This author-only pair tests the original official evaluation
script in its official Linux/amd64 image through the verified standard Docker
backend. It is not a solver run, token optimization or replacement for the eight
selected issues. The [earlier Mac complete-file probe](EXTERNAL-BUNDLE-02-FILE-PROBE-01.md)
already separated base2 failures/170 required passes from gold172 required passes;
its extra xfail and original literal-selector failure remain historical evidence.
The distinct question is whether the unchanged official script/image satisfies
that same original grading contract. Do not retry Requests2674's adverse grade.

Registry metadata resolves the mutable tag once to OCI index
`547472f1933751a67623599dae697188232c9712a46ab66fb69330f88b911e5a`, Linux/amd64 manifest
`c190b1e0539cef0e292e5c6e6219734f298d1bdee17189e497c5b116d8c0ca7f`, config
`1718609d2c1e3a6d929eb4643f8474ee9e8f551cab77847f6c492dd0df6f1701`.
An initial metadata request wrongly assumed a direct manifest and stopped at an
assertion before download/evaluation. Retain that failure; the inspected OCI index
selects exactly one Linux/amd64 descriptor. No registry tag refresh after this pin.
Seven of ten layer digests match the cached Requests image. Reverify reused bytes;
download only three missing blobs (365,275,166 bytes), each verified against the
pinned descriptor. Bound new downloads at512MiB/600seconds total, transport at
5GiB/600seconds, decompressed verification at10GiB; check host/guest free space.
No host image extraction or host package installation. Guest transfer/load600s
per operation. Preserve all original attempts and stop on errors, no automatic retry.

Before grading, import actual project pytest from `/testbed/src` in the image's
Python environment and compare selected-base source file bytes/modes with the
image. Report synthetic Git HEAD or preparation differences explicitly. Exercise
actual pytest passing and deliberately failing assertions under the same runtime;
expected failures must contain assertion diagnostics rather than support errors.
These controls are authored and cannot count as issue/model evidence.

Freeze two cells, base then gold, in fresh disposable containers from the exact
image. Use the original private selected row, gold patch only for gold and original
evaluation script SHA256
`950987985c71231ea07667924061f204b67af5d249098b35833f08e5fa05fad3`.
Do not modify commands, test patch, assertions, required labels or parser. The
original official `parse_log_pytest` source is SHA256
`cd56156414f8327221e525665ace9b184f7d73e83b272d9eb3f545fb17c2d9bc`.
An identical passive observer may record actual collection/reports/session exit
for both cells. Its path must not replace pytest or inject fabricated status lines.
Keep official stdout/stderr and shell exit distinct from actual pytest exit.

Unlike the prior read-only runtime control, evaluation explicitly needs a writable
**disposable container root** for Git/test patch/cache and pytest subprocesses.
Freeze this difference now: network none, no host mounts, cap-drop ALL,
no-new-privileges, default seccomp, memory1GiB,1CPU,64 PIDs. Controls and cells use
these same limits. No external services or credentials. Transfer private grading
inputs only to owned author containers; no future solver sees them. Bound each
cell180seconds and controls60seconds. A failure or timeout is retained, with no
restriction relaxation, case replacement or unchanged rerun. Accept the pair only
if all2 FAIL_TO_PASS fail on base/pass on gold, all170 PASS_TO_PASS pass in both,
and actual native exits are1/0 with no timeout/OOM/infrastructure error.

Export only scalar summaries, identities and hashes; private patch bodies, labels,
source files and raw logs stay outside repository/model inputs. Clean up containers,
stop guest services and VM, verify terminal state. Native success cannot resolve
the separately documented model-tool approval blocker and is not token/time savings.

한국어: 기존 Mac 파일 전체 검증의 성공과 선택자 실패 기록을 유지하고, 같은
pytest5221을 공식 이미지·원본 평가 스크립트로 한 번씩 검증한다. 원본2개 실패와
170개 기존 통과 항목을 모두 보존한다. 평가용 쓰기 가능 컨테이너 차이를 미리
명시하며 모델 호출·토큰 절감 실적과 구분한다. 전체8개 목표는 아직 미달이다.
