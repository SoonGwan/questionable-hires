# Owned Linux x86 control01 — 2026-09-27

Parent `ef69f7c7`; unchanged eight skill resources, **zero models or external
case runs**. [Final result](results/owned-linux-x86-01/result.json),
[fixture preservation](results/owned-linux-x86-01/fixture-preservation.json)
and [original/readable log identities](results/owned-linux-x86-01/log-identity.json)
retain actual observations and failed author controls. This is an x86 userspace
execution gate, not official OCI/native grading or all-eight efficiency proof.

## Actual translation and write boundary

The existing Apple Linux Rosetta capability is queried installed; no host
installation is performed. The [owned ARM Linux boot](OWNED-LINUX-VM-01.md)
uses the same frozen decoded kernel/initramfs and one CPU/512 MB RAM, with no
network devices, disks or persistent VM profile. This control adds the Rosetta
translation share, a readonly test-fixture share and a separate disposable
writable share. The configured shares are limited to these runtime and owned data directories.

The actual static x86-64 ELF is invoked as `/rosetta/rosetta /fixture/busybox.static`:
ARM BusyBox reports `aarch64`, translated BusyBox reports `x86_64`, and a translated
shell computes `6*7=42` with a distinct standalone workload marker. Both translated
invocations exit0. Guest poweroff invokes the host delegate and process exits0
without deadline/timeout. These are actual instructions in the guest, not a
rewritten simulator or solely host availability/discovery flags.

The final paired write test uses the **same host owner/group and directory mode
0700** for both fixture and writable roots. Guest creation in `/fixture` fails
with `Operation not permitted` and exit1; no host file is created. Guest creation
in `/writable` exits0 and the expected host file bytes are verified. The readonly
binary's bytes, mode0755 and sole-file inventory remain unchanged. This rules out
an inability to write any share or the earlier unequal directory modes as an
explanation for this paired outcome. It does not certify every VirtioFS operation,
all projects, link targets or untested writable mounts.

[Final console](results/owned-linux-x86-01/final-guest-reading.txt) retains kernel
identity, module load/mounts, actual native and translated output, failed readonly
write, successful normal write and power-down. Published [Swift source](results/owned-linux-x86-01/probe.swift)
and [process/proof controller](results/owned-linux-x86-01/control.py) are the exact
final executed text, with caller-selected owned directory and process deadlines.

## Provenance and reproducible inputs

The x86_64 Alpine v3.22 [APK index](https://dl-cdn.alpinelinux.org/alpine/v3.22/main/x86_64/APKINDEX.tar.gz)
selects `busybox-static`1.37.0-r20. Its [APK](https://dl-cdn.alpinelinux.org/alpine/v3.22/main/x86_64/busybox-static-1.37.0-r20.apk)
is fetched over TLS. Only the exact regular `bin/busybox.static` member is read
from the concatenated gzip tar; no unrestricted archive extraction. Actual ELF64,
little-endian machine62 (x86-64), bounded file size and absence of PT_INTERP are
checked. [Binary/package identities](results/owned-linux-x86-01/binary-identity.json)
record SHA256 and GPL-2.0-only. No APK signature-validation claim or binary
redistribution; all binaries remain in the owned private runtime directory.

[Apple's Intel Linux documentation](https://developer.apple.com/documentation/virtualization/running-intel-binaries-in-linux-vms?language=objc)
describes userspace Intel binary translation in ARM Linux. We use explicit
invocation, not an x86 Linux OS boot or installed binfmt handler. The guest loads
existing fuse/virtiofs modules and mounts the translation/data tags; the controlled
successful reads and writes establish mounts beyond a module-file listing.

To reproduce, supply exact frozen kernel/initramfs from VM01, the SHA-matching
static binary as `fixture/busybox.static` mode0755, and empty owned `writable` and
fixture directories with matching mode0700. Compile/sign the final Swift source
as `probe` using the supplied [entitlement](results/owned-linux-x86-01/entitlements.plist),
then run the published controller with that owned directory. Verify all result
assertions and fixture preservation; process0 alone is insufficient. The Swift
25-second and parent35-second ceilings retain timeout status and stop only the
owned VM/process group. The final VM and all earlier processes are terminal.

## Retained author errors and diagnostic controls

Six controller attempts include five actual guest boots; all are related local
controls, not independent samples or paid cells:

- Initial [controller source/error summary](results/owned-linux-x86-01/first-authoring-failure.json)
  fails before VM creation: an overbroad string replacement makes the log path a
  tuple. No guest starts.
- The [next controller/error summary](results/owned-linux-x86-01/second-authoring-failure.json)
  fixes opening the log but misses the same tuple in `read_text`. The
  [actual guest console](results/owned-linux-x86-01/first-native-guest-reading.txt)
  reaches x86 output/power-down; result collection fails, so no completed
  controller result is claimed. Both original erroneous sources are retained.
- The corrected [first complete result](results/owned-linux-x86-01/first-complete-result.json)
  and console pass x86 execution before the write-boundary test is added.
- The first readonly observer falsely requires the text `Read-only file system`;
  actual VirtioFS returns EPERM/`Operation not permitted` and exit1 with host file
  absent. The [original false result](results/owned-linux-x86-01/readonly-first-result.json),
  [assertion error](results/owned-linux-x86-01/readonly-observer-error-reading.txt)
  and source/console remain; not relabeled as a passing controller.
- A corrected paired probe succeeds, but its directories initially have unequal
  modes0700/0755. [Result](results/owned-linux-x86-01/unequal-modes-pair-result.json)
  remains separately. The final test matches owner/group/modes, removes only the
  owned prior positive-control file, and reruns the unchanged executable/controller.
  [Matched input facts](results/owned-linux-x86-01/matched-directory-inputs.json)
  and final result establish the stronger boundary.

The first two error summaries are observed author-error records, not purported
raw stderr exports. Original log hashes distinguish reading derivatives; console CR/newlines and trailing whitespace are normalized only in published reading copies. No
native benchmark case or model attempt is retried/rescored by these corrections.

## Remaining scope

No shared glibc/dynamic x86 application, binfmt registration, full official image,
Python project interpreter, selected base/gold regression, model solver, or
whole-task input/output/time comparison is executed here. Frozen eight-case
selection and prior already-PASS/adverse native outcomes remain unchanged.
The next gate is the official image's dynamically linked interpreter/library
layout, then exact native grading in an isolated author environment. This
component proof neither bundles a VM dependency nor completes the update goal.

한국어: 실제 ARM Linux 게스트에서 정적 x86 ELF가 uname·계산을 실행하고 종료0을
반환했다. 소유자·권한이 같은 읽기 전용 공유의 쓰기는 거부되고 별도 쓰기 공유의
정상 대조는 성공했다. 제어 코드의 두 경로 오류·errno 가정 오류·이전 권한 차이는
보존했다. 공식 이미지·동적 Python·외부8개 과제·모델 비용 개선은 아직 검증하지
않았으며, 전체 스킬 리소스와 과거 불리한 결과는 그대로다.
