# Standard-container runtime01 — 2026-09-28

[Protocol](EXTERNAL-BUNDLE-02-CONTAINER-01-PROTOCOL.md) `5c35fd67`, package pin
`6c9fab06`. Existing external8 identities/skills `7172b50c` and all prior adverse
measurements remain unchanged. This is a new standard-container backend check,
**not** the first Linux execution or a new Requests2674 grade.

Earlier [owned-VM official grade01](OWNED-OFFICIAL-GRADE-01.md) had already executed
the official script: both native variants154 pass/8 fail, required gate declined.
The prior turn's claim that Linux execution itself had just become possible omitted
that history; commit`a55780d3` corrects it. No same-image issue tests are repeated.
A broader initial filename inventory also traversed private grading directories;
no bodies were read, filenames are not exported, and this author conversation is
not an independent solver context. Fresh declared-input solver sessions remain required.

## Runtime and image identity

The existing dedicated Lima VM was resumed once. Guest-only installation uses
Debian docker.io/docker-cli26.1.5+dfsg1-9+deb13u1 plus the frozen three dependencies.
[All five package SHA256s](results/external-bundle-02-container01/package-observations.json)
match APT metadata;44,067,556 downloaded bytes. The first download completes, but
its guard incorrectly assumes every cached deb belongs to the new closure and
rejects a pre-existing bootstrap rsync deb. [Original error](results/external-bundle-02-container01/install.stderr)
and initial exit1 remain recorded. The corrected controller checks only the exact
five pinned packages, verifies the simulated installation set and installs from
cache with no-download. No package/source filter changes grading obligations.
Debconf falls back to Noninteractive, and boot-unit disable emits a socket-active
notice; native steps exit0 and final service shutdown is verified separately.
Host packages, contexts, account startup and trust are not changed.

[Transport preparation](results/external-bundle-02-container01/transport.json)
rechecks all10 cached compressed digests/sizes and their uncompressed diffIDs
against the unchanged image config. No layer is downloaded or extracted on the
host. The1,015,459,840-byte Docker transport contains untouched compressed layers,
config and a generated transport manifest; native [Docker26 loader](https://github.com/moby/moby/blob/v26.1.5/image/tarexport/load.go)
decompresses individual layers and validates diffIDs. This follows
[image load](https://docs.docker.com/reference/cli/docker/image/load/), not a flattened
filesystem import. The outer transport has its own digest and local tag; it is
not relabeled as the original registry manifest bytes.

Explicit transfer to the VM preserves the archive SHA256. Standard Docker load
succeeds with the native overlay2 driver. [Loaded identity](results/external-bundle-02-container01/loaded-identity.json)
requires config ID`sha256:1cf3ffbd1932395d2603da9b51dbb7383dc9f64044d241e3cd6b418d5fe56821`
and all10 ordered RootFS diffIDs, Linux/amd64 and no image-declared volumes.
Original registry manifest remains`c83bd92b48356279e868d16d51ec15ca1481fa1bc97968e7a8d935df062f0bf2`.
This does not establish that image HEAD/modes equal the selected upstream archive;
those earlier observed differences may be intrinsic to the image preparation.

## Actual constrained execution

The [authored probe](results/external-bundle-02-container01/container_control.py)
executes in one named container,1GiB memory/1CPU/64 PIDs, read-only root,
network none, no binds/volumes, cap-drop ALL and no-new-privileges; default seccomp
is unchanged. [Native Docker inspection](results/external-bundle-02-container01/control-isolation.json)
checks those settings before start. The container supplies no host credentials or
source/grading mounts and disables image healthchecks.

[Original native output](results/external-bundle-02-container01/native-control.stdout)
records actual Python3.9.20, OpenSSL3.0.15, pytest7.4.4, pluggy1.0.0 and Requests
from `/testbed/requests/__init__.py`, matching its previously observed SHA256.
The process sees CapEff0, NoNewPrivs1 and only loopback; a root filesystem write
is rejected with EROFS. These scoped checks are not a universal security proof.
The host kernel is ARM and execution uses configured translation, not native x86
hardware or an independent performance environment.

Two real child interpreter invocations preserve normal exit0 with exact marker,
and intentional exit1 with `AssertionError: QH_EXPECTED_ASSERTION`. These are
infrastructure controls, not selected project tests or a model fix. The parent
container exits0 only after checking both; native failed evidence is retained.
[Terminal state](results/external-bundle-02-container01/terminal-control.stdout)
shows exited, not running, exit0, no OOM. No timeout, protection relaxation or
container retry occurred. Host subprocess bounds cover install600s, transport600s,
transfer600s, load600s and each container command60s; native child bounds10s.

[Cleanup](results/external-bundle-02-container01/cleanup.json) confirms no remaining
containers, Docker/socket/containerd inactive and disabled, VM Stopped and no
owned Lima/SSH process. The verified image stays in the stopped owned VM for a
distinct next validation stage. [Sources and original hashes](results/external-bundle-02-container01/identities.json)
retain the preparation; full config/history stays private, no gold/test body or
required-label list is exported. Zero issue-test calls and model calls.

## Decision

The standard backend now has image identity and actual constrained interpreter/
assertion evidence. It does not cure Requests2674's adverse grade, justify another
unchanged comparison, prove all8 readiness or supply token/time savings. Next
choose a still-unresolved native gate from the existing selected cohort, freeze
its exact image/script/input boundaries, and use its original official evaluator.
Keep other-case failures and original-source differences accessible; model/solver
isolation and whole-task comparisons remain separate requirements.

한국어: 과거 Linux 평가 이력을 누락한 설명을 정정하고 표준 Docker 경로를 별도로
검증했다. 기존10개 계층·설정 식별자가 실제 로드된 이미지와 같고, 제한된 컨테이너에서
공식 Python·라이브러리·프로젝트 import 및 정상/실패 assertion 종료0/1을 확인했다.
처음의 기존 rsync 캐시 검사 오류도 보존했다. 컨테이너 제거·게스트 서비스 비활성화·
VM 종료를 확인했으며 이슈·모델 실행은0회다. 기존 불리한 결과와 전체 목표 미달은 유지한다.
