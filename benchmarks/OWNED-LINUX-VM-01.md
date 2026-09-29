# Owned Linux VM01 — 2026-09-27

Subsequent [x86 control01](OWNED-LINUX-X86-01.md) verifies static guest translation
and a paired shared-directory write boundary. The unverified next-gate statements
below describe this original boot checkpoint; official image/grading remains pending.

Parent `55c97a7d`; unchanged eight skill resources, **zero models or external case
reruns**. [Boot outcomes/artifact hashes](results/owned-linux-vm-01/result.json),
[identities](results/owned-linux-vm-01/identity.json) and original failure remain.
This opens a possible local Linux route beyond the absent Docker/Colima CLI;
it does not establish official AMD64 grading or a skill-efficiency update.

## Actual runtime and isolated boot

The installed Swift/Apple Virtualization runtime queries
`VZVirtualMachine.isSupported=true`. A new owned executable uses one virtual CPU,
512 MB RAM, a serial console and entropy device, with no networking, storage
or host directory shares. Only that temporary executable receives an ad-hoc
signature with the virtualization entitlement. No global installation, persistent
VM profile, existing container/CF service reset or host security/account change.

The actual ARM guest boots Linux `6.12.110-0-virt`, executes BusyBox `uname -a`,
prints a distinct standalone proof line, and powers off. Host delegate reports
`QH_VM_GUEST_STOPPED`, executable exit0, no deadline/parent timeout. The first
success uses the original local controller; a second success validates the
published controller after replacing its hardcoded private root with a caller
argument and adding explicit proof assertions. These two related boots are not
independent validation. All VM processes are terminal; no VM is left running.

[Apple's Linux VM sample](https://developer.apple.com/documentation/virtualization/running-linux-in-a-virtual-machine)
requires a kernel/initramfs matching the host CPU architecture. Official Alpine
v3.22 aarch64 [netboot artifacts](https://dl-cdn.alpinelinux.org/alpine/v3.22/releases/aarch64/netboot/)
were downloaded over TLS into the owned temporary directory. Actual downloaded
bytes/hashes, decoded kernel hash and guest uname are retained. The URLs are
mutable distribution paths: future downloads must match recorded hashes for
replay, not silently relabel this checkpoint. Kernel/initramfs binaries are not
redistributed here; no public issue/evaluation text or gold resources enter this VM.

## Distinguishing the initial failure

The original EFI ZBOOT kernel is rejected at VM start with VZErrorDomain Code1.
[Original child exit1 and absent proof](results/owned-linux-vm-01/first-result.json)
and [error](results/owned-linux-vm-01/first-guest-reading.txt) remain. The initial
Python controller itself returned0 while recording the child failure; do not
mistake that wrapper exit for boot success. Its [reading source](results/owned-linux-vm-01/initial-control-reading.py)
is a path-redacted derivative, not the final portable control.

The downloaded configuration has EFI_ZBOOT and gzip compression; the EFI wrapper
lacks the raw ARM64 Image magic. The [upstream ZBOOT header](https://github.com/torvalds/linux/blob/v6.12/drivers/firmware/efi/libstub/zboot-header.S)
records payload offset/size/compression. The observed gzip member starts at the
same declared offset; decoding the bounded declared payload reproduces the exact
raw kernel bytes. Raw ARM64 header magic and image size validate. The same binary,
entitlement, initramfs, resources and commands then boot successfully with only
the boot-image representation changed. This supports a format mismatch for this
failure; it does not certify other kernels or every possible VZ startup error.
[Transform facts](results/owned-linux-vm-01/kernel-transform.json) retain source
and decoded identities. No kernel source or project test was rewritten.

## Reproduction and next gate

The published [Swift executable source](results/owned-linux-vm-01/probe.swift),
[entitlement](results/owned-linux-vm-01/entitlements.plist),
[header decoder](results/owned-linux-vm-01/decode_kernel.py) and
[portable process/proof controller](results/owned-linux-vm-01/control.py)
are retained. In a new owned directory with the exact frozen EFI kernel and
initramfs, decode the kernel into `vmlinuz-virt`, compile `probe.swift` as `probe`,
ad-hoc sign with the supplied entitlement, then run:

```sh
python3 -B benchmarks/results/owned-linux-vm-01/control.py /path/to/owned-directory
```

The Swift guest deadline is25 seconds; the parent process deadline35 seconds
retains results and terminates only its owned process group on timeout. Parent
result/proof assertions must pass; native start failure/timeout is not success.
[Final console reading](results/owned-linux-vm-01/final-guest-reading.txt) preserves
actual boot, command outputs and guest power-down. Published paths are reading
copies; original private log hashes are recorded.

A separate actual Swift enum query reports Linux Rosetta availability **installed**;
no installation or guest activation occurred. [Apple's Intel Linux documentation](https://developer.apple.com/documentation/virtualization/running-intel-binaries-in-linux-vms?language=objc)
describes Intel userspace binaries in ARM Linux, not booting an Intel Linux OS.
Guest translation share activation, actual x86 ELF execution, required shared
libraries and exact official environment remain unverified. The initramfs lists
virtiofs/fuse modules, but that listing is not proof they load or mount a share.

The official selected eight-case preflight still has its missing runtime/contrast
gates. No Python/project tests, selected gold patch, model solver, official OCI
image or full native grading was executed here. Prior native already-PASS/adverse
results stay unchanged. Next work can test the installed translation facility
with a small non-answer-bearing x86 binary before using official image layers.
All-eight quality, whole-task token/time and delivered update remain unmet.

한국어: 임시 Apple VZ 프로그램에서 실제 ARM Linux 부팅·명령 실행·전원 종료를
확인했다. 최초 EFI 압축 커널 형식의 실패를 보존하고 같은 커널의 raw 표현으로
바꾸자 부팅됐다. 기존 Rosetta 상태는 설치됨으로 조회했지만 게스트 번역 실행은
아직 없다. 공식 x86 이미지·8개 외부 과제·모델 효율 검증으로 확대하지 않는다.
