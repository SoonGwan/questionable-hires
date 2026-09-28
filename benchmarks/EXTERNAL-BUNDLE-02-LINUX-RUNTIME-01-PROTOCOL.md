# Owned Linux runtime preparation01 — 2026-09-28

Parent `7fcf880e`. External bundle02 keeps all eight selected identities and skill
resource `7172b50c`. This preparation addresses the unavailable executable Linux
route identified by the official row/runtime lookup. It does not rescore the
original native Mac grades or replace cases. Zero model/issue-grade calls here.

Use the owner's continuing improvement authorization to prepare an author-owned
runtime, without altering existing package installations, shells, Docker contexts
or account startup. The earlier Python-environment preparation alone did not
establish this route. Current narrow checks find no Lima/Colima/QEMU installation;
host is ARM macOS with8 GiB memory and230 GiB available disk. Existing Rosetta has
an installed package receipt; that alone is not proof Linux translation works.

Use official Lima **2.2.0**, Darwin-arm64 archive37,586,365bytes, SHA-256
`bbdef91774885a0d05f7b048c4eb89ae2bcf3a0c252ae7ca7934e63df76d93c3`.
Verify downloaded bytes against the release metadata/checksum before execution.
[Official installation](https://lima-vm.io/docs/installation/),
[VZ](https://lima-vm.io/docs/config/vmtype/vz/) and
[multi-architecture guidance](https://lima-vm.io/docs/config/multi-arch/)
permit an owned prefix and native ARM VM with translated x86 user programs.
Translation is not native x86 hardware or an identical performance environment.

Use a fresh0700 owned temporary root for tools, Lima state, downloads and logs;
set LIMA_HOME only on child commands. No host filesystem mounts, SSH-agent
forwarding, automatic service startup or host application-port forwards. Keep
outbound networking for declared downloads. Mount denial is not a claim of full
network/credential isolation. Never export generated SSH keys or private runtime
configuration. Inspect the resolved configuration before startup.

Limit VM to2vCPUs,2GiB memory and20GiB disk. Binary download limit60MiB/120seconds;
pin the guest image URL/hash before startup, at most1GiB/180seconds to download.
VM startup has a300-second command bound; inspect the actual instance/process
state after any observation failure rather than relaunching blindly. Preserve
failed preparation attempts. No host Rosetta install if the existing route fails.
No automatic retries of unchanged failed inputs. Stop the owned VM after controls
so an idle author environment does not retain memory/background execution.

Controls: actual fresh Linux shell/kernel identity; resolved mounts plus a newly
created host-only sentinel unavailable in the guest; absence of solver/grader
payloads; guest runtime and CPU-translation capability if available. Record bounded
commands, exits and source/config/tool identities. No grade patches, labels, old
model logs or credentials are copied. Official task-image pulls, exact image
preparation, grader/network boundaries and execution protocol remain a separate
next stage. A running Linux shell alone never establishes all-eight readiness,
quality or whole-task token/time improvements.

한국어: 기존 외부8개 사례를 바꾸지 않고 별도 Linux 실행 환경의 가능성을 확인한다.
기존 설치·계정 자동 실행을 바꾸지 않고 임시 전용 경로,2CPU·2GiB·20GiB 한도와
호스트 공유 없는 설정을 사용한다. 실패도 보존하며 모델·이슈 평가0회, 실제
Linux 구동·분리 확인은 전체 품질·토큰·시간 개선과 별도 단계다.
