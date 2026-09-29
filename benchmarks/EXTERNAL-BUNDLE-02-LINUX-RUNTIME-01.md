# Owned Linux author runtime01 — 2026-09-28

[Protocol](EXTERNAL-BUNDLE-02-LINUX-RUNTIME-01-PROTOCOL.md) `fbb44ccf`, guest pin
`261e266c`. Existing external-bundle02 case identities and skill resource `7172b50c`
are unchanged. This establishes a separate Lima-managed Linux/translated-x86 route. The earlier
[owned VM](OWNED-LINUX-VM-01.md), [official Python](OWNED-OFFICIAL-PYTHON-01.md) and
[official grade](OWNED-OFFICIAL-GRADE-01.md) had already executed Linux and the
selected image. Treating Linux execution itself as newly unblocked was incomplete
history review; this is an alternative runtime, not the first executable route.
It does not repair or rescore either the Mac or earlier Linux grades.

Lima2.2.0 is extracted into a new owned0700 temporary prefix after the37,586,365-byte
[official binary hash matches](results/external-bundle-02-linux-runtime01/download.json).
The first extraction guard rejected a legitimate internal documentation symlink
(`share/doc/lima/templates` → `../../lima/templates`) before extracting anything.
A corrected resolved-containment guard plus Python's data filter accepted that
in-prefix target using the same archive. No download retry or unsafe external link
was accepted. The initial guessed Debian template path and help topic were absent;
the actual bundled versioned template and CLI help supplied configuration details.

The dated Debian13 ARM image matches the frozen335,413,248-byte size andSHA-512
([download identity](results/external-bundle-02-linux-runtime01/image.json)); no moving
fallback image was used. [Validated authored/resolved configuration](results/external-bundle-02-linux-runtime01/config-review.json)
sets2vCPUs,2GiB RAM,20GiB disk, empty host data mounts, no SSH-agent/public-key loading,
no proxy-environment propagation, no container daemon and ignored application-port
forwards. Dedicated local SSH management is still required. Existing Rosetta is
used without installing it or changing host package/account startup settings.
The pre-start protocol explicitly allows only its runtime share.

[One startup](results/external-bundle-02-linux-runtime01/start.json) completes with
exit0 in41.349seconds, no startup retry or timeout. This is preparation timing,
not skill/VM performance comparison. The VM remains in the owned temporary root
for subsequent bounded author preparation; original host grading/source data is
not copied. The published configuration replaces the private owned prefix with
`<owned-runtime>`; it is a reading copy, not a directly runnable path.

## Executed controls and boundaries

The [actual guest script](results/external-bundle-02-linux-runtime01/guest_control.py)
runs once via a fresh `python3 -I -B` process with45-second host/10-second native-child
bounds. [Original stdout](results/external-bundle-02-linux-runtime01/control.stdout)
and [execution identity](results/external-bundle-02-linux-runtime01/control.json)
show Linux ARM, kernel6.12.95+deb13-cloud-arm64, Python3.13.5 and2 CPUs.
A newly created host-only sentinel exists on the host but is absent in the guest;
the existing solver-staging path and SSH agent are also absent. The only observed
virtiofs/9p/sshfs mount is `vz-rosetta` at `/mnt/lima-rosetta`.

Two authored static x86-64 ELF controls contain only write/exit syscalls, with no
project code, dynamic libraries, filesystem reads or network. Both print the exact
marker; expected exits0 and37 are preserved, no stderr. This verifies execution
through the configured translation route, not native x86 hardware, compatibility
with an official task image, or Python/OpenSSL dependency parity. The intentional
nonzero exit is a runtime control, not a project regression assertion.

No issue statements, solution/test patches, grading labels, private account
credentials or original model logs are transferred. Beyond Lima startup/provisioning
and its generated public SSH access key, the guest control source is the only
manually supplied execution payload.
These directory/mount observations do not prove all network isolation: outbound
networking exists, and host-service/grader/network separation must be established
before any model solving. No container daemon/task image, official evaluation
script, project test, skill invocation or model session has run here.

[Graceful stop and authoritative instance state](results/external-bundle-02-linux-runtime01/terminals.json)
record Running→Stopped with exit0. [Scoped process cleanup](results/external-bundle-02-linux-runtime01/process-cleanup.json)
finds no owned Lima/SSH process afterward. Generated keys/runtime files stay private;
[raw log hashes and redacted reading copies](results/external-bundle-02-linux-runtime01/identities.json)
retain startup/configuration/stop evidence without publishing them.

## Next gate

Use this stopped author runtime only for a distinct standard-container preparation
with pinned image identity and explicit transfer/disk/time limits. Reuse prior layer
acquisition. Earlier image-source mode/HEAD differences and the declined Linux
base/gold pair remain authoritative; a new container backend does not itself
justify another identical grade or predict that those differences disappear. Preserve all eight tasks and prior adverse results; do not replace failed
cases. Existing exact image/runtime metadata is the starting point, not guessed
Python versions. Solver/grader isolation and model execution protocol remain
separate gates. No README skill capability, featured chart, website or model-cost
claim changes; all-eight quality/token/time remains unmet.

한국어: 전용 임시 경로에 해시가 검증된 Linux VM을 준비했고 실제 Linux 실행과
x86 프로그램 종료0/37을 확인했다. 호스트 전용 파일·기존 평가 작업 폴더·SSH
에이전트는 보이지 않았고 Rosetta 실행 공유만 존재했다. 정상 종료 후 Stopped와
관련 프로세스 부재를 확인했다. 최초 압축 해제 경로 검사 실패도 보존한다.
공식 이미지·프로젝트 테스트·모델 실행은 아직0회이며, 다음 단계는 고정된 공식
이미지의 원본/정답 검사와 분리 확인이다. 전체 품질·토큰·시간 개선 근거는 아니다.
