# Standard-container author preparation01 — 2026-09-28

Parent `a55780d3`. Reuse the stopped/verified Lima runtime and pinned Requests2674
image solely to validate a standard Linux container backend. All8 selected tasks,
prior Mac grades and [owned-VM Linux grade](OWNED-OFFICIAL-GRADE-01.md) remain fixed.
This is not the first Linux/image execution and does not authorize an unchanged
Requests2674 grade retry. No issue tests, models or gold/test patches in this stage.

The earlier APFS/VirtioFS/chroot route had unverified full OCI filesystem semantics;
132 source bytes matched but129 Git modes and synthetic HEAD differed from the
selected archive. Those differences may belong to image preparation itself; do
not assume Docker removes them. The distinct work here is standard Docker layer
loading, runtime identity, actual native assertion controls and no-host-mount /
network-none execution. A new backend is not evidence that old failures disappear.

Use guest-only Debian docker.io **26.1.5+dfsg1-9+deb13u1**, as returned by the
existing signed guest APT metadata. Review its full simulated dependency plan
before installation; retain package versions and package identity metadata. Limit
package downloads to256MiB and installation to600seconds with a parent watchdog.
Do not change host packages, Docker contexts, trust or services. Docker may run
inside this owned VM; disable its guest boot activation after preparation.

Reuse the10 compressed blobs previously acquired and SHA checked by
[owned layers01](OWNED-OFFICIAL-LAYERS-01.md). Manifest SHA256
`c83bd92b48356279e868d16d51ec15ca1481fa1bc97968e7a8d935df062f0bf2`, config SHA256
`1cf3ffbd1932395d2603da9b51dbb7383dc9f64044d241e3cd6b418d5fe56821`.
Verify every compressed digest/size and every uncompressed layer diffID against
that exact config. Build a Docker-save transport archive without extracting image
files on the host. At most5GiB archive and600seconds preparation; preserve source
blobs. Copy only that archive into the VM through explicit transfer, not mounts.
Transfer and native docker load each have600-second parent bounds.20GiB VM disk
limit remains; check space before loading. No registry tag refresh or new image.

After native load, require exact image config ID and ordered RootFS diffIDs.
Run an explicitly chosen interpreter in read-only containers, network none,
no mounts, no healthcheck, cap-drop ALL, no-new-privileges,1GiB memory,1CPU and64 PIDs;
retain default seccomp. Supply no host credential environment. Use disposable
named containers with cleanup checks, each60-second parent bound. Actual image
Python/SSL/pytest imports and Requests from `/testbed` must identify their paths
and hashes. Separately run authored passing/failing Python assertions with the
same interpreter; report both actual exits/diagnostics. These aren't project tests
or full official-harness equivalence. Preserve any restriction/runtime failure;
do not disable protections merely to obtain a green control.

Record every preparation attempt and terminal status. No automatic unchanged
retries; inspect the same live process/container after a timeout. Stop the guest
Docker services and VM, then verify owned process/container absence. Keep private
image config/history and source/test bodies out of public exports. During initial
history discovery, an overly broad filename inventory traversed retained private
grader directories; filenames appeared in author context, no bodies were read or
published. This author conversation is not a future independent solver context.
Future solvers must use fresh sessions with only declared answer-free inputs.

한국어: 과거 Linux 공식 평가를 유지하고 표준 Docker 경로 자체를 별도 검증한다.
이미 확보한10개 계층을 재사용하며 게스트에만 실행기를 설치한다. 이미지 식별자·
계층·실제 import·정상/실패 assertion 및 분리·종료를 확인하고 이슈·모델은 실행하지
않는다. 새 실행기가 기존 실패를 해결한다고 가정하지 않으며 전체 목표는 미달이다.

## Reviewed package closure, before installation

The daemon package recommends a separate CLI; include docker-cli at the same
26.1.5+dfsg1-9+deb13u1 version. Native APT planning shows exactly5 new packages,
zero removals/upgrades,44,067,556 download bytes and197MB installed estimate.
Remaining versions: containerd1.7.24~ds1-6+deb13u1, runc1.1.15+ds1-2+b4,
tini0.19.0-3+b8. First download-only, verify each retained deb's SHA256 against
APT package metadata, then install the same version-pinned closure with no-download.
A single600-second parent bound covers those steps. This is guest administration,
not a host install or a benchmark/model execution.
