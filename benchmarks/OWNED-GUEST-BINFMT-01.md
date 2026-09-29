# Owned guest binfmt01 — actual automatic x86 child repair

Dated checkpoint **2026-09-27**, protocol/resource `ad2432df`, parent `dbfd6a1b`.
[Protocol](OWNED-GUEST-BINFMT-01-PROTOCOL.md),
[final native outcome](results/owned-guest-binfmt-01/result.json),
[observed markers/handler state](results/owned-guest-binfmt-01/observed-markers.txt).
Zero models and selected-case tests. Eight skills and featured measurements unchanged.

## Before/after observable behavior

The unchanged [project01 child command](OWNED-OFFICIAL-PROJECT-01.md) originally
raised native **OSError errno8**, while its explicitly translated parent imported
Requests from `/testbed`. After guest binfmt setup, **the exact same probe bytes**
now produce child **exit0,stdout`42\n`,empty stderr**. Project Requests version2.7.0,
path `/testbed/requests/__init__.py` and opaque file SHA256 are unchanged. This is
an actual scoped routing repair, not controllerexit0 interpreted as child success.
The final VM/controller return0, all7 routing statuses0, guest poweroff observed,
no deadline hit, **5.339 seconds** total. No layer was reapplied or source repaired.

## Guest-only mechanism and input identity

The frozen initramfs contains6.12.110-0-virt loop/squashfs drivers but lacks
binfmt_misc. Retrieved the official Alpinev3.22 aarch64
[netboot modloop image](https://dl-cdn.alpinelinux.org/alpine/v3.22/releases/aarch64/netboot/)
in2.58 seconds,16,347,136 bytes. Its actual SHA256, recorded before VM execution,
is `da142869626ec9d4543ab46482af10b5ff2c8c1c2e01068ddf32360316a06218`.
The URL is mutable; this records actual bytes, not a preexisting immutable pin.
[Download identity](results/owned-guest-binfmt-01/download.json).

Readonly SquashFS mounted in the owned guest exposes the **raw** module
`modules/6.12.110-0-virt/kernel/fs/binfmt_misc.ko`. Copied only that native module
to guest RAM `/tmp` and loaded it successfully; mismatched kernel ABI is not
claimed compatible. A guest binfmt filesystem is mounted at the **chroot's** proc
path. [Registration helper](results/owned-guest-binfmt-01/fixture/register.py)
uses Apple's documented x86 ELF magic/mask and credentials/preserve/fix-binary
semantics mapped to kernel **POCF** flags. `F` keeps the opened interpreter available
across chroot; `C` implies `O`. See [Apple's guest setup](https://developer.apple.com/documentation/virtualization/running-intel-binaries-in-linux-vms)
and [Linux registration/flag documentation](https://docs.kernel.org/admin-guide/binfmt-misc.html).
Only the disposable guest kernel is affected; no host binfmt/install/profile change.

## Retained first attempts

Four related owned VM observations, all zero models/external cases:

1. [First outcome](results/owned-guest-binfmt-01/first-result.json): guest `/tmp`
   absent, shell redirection fails before module preparation; controller1,VM0,
   native child stillerrno8. This was not a module ABI failure.
2. [Second outcome](results/owned-guest-binfmt-01/second-result.json): create only
   guest RAM `/tmp`; assumed `.ko.gz` path missing, empty module short-read,
   controller1,VM0, childerrno8. Compressed kernel-package configuration does not
   establish modloop's actual module representation.
3. [Third outcome](results/owned-guest-binfmt-01/third-result.json): narrow module
   discovery/raw payload copy succeeds, native module load0. Registration fails
   because mounting binfmt under outer `/proc` does not mount it under the separate
   chroot proc. Controller1,VM0, childerrno8; original log/collector/source retained.
4. Final outcome: change only binfmt mount to chroot proc; registration0 and actual
   same childexit0/stdout42. Earlier failures remain failures, never rescored.

Public artifacts retain each original result/source and opaque raw-log digests;
raw console stays private. Final marker copy is a whitelist, not byte-identical
raw console. [Source](results/owned-guest-binfmt-01/probe.swift),
[controller](results/owned-guest-binfmt-01/control.py),
[resource hashes](results/owned-guest-binfmt-01/resource-hashes.json).
The existing image root and probe shares remain readonly; guest proc/tmpfs/modules
are RAM-only. One CPU,1GiB RAM,no network or block devices,180-second guest and
independent200-second parent watchdog with owned process-group TERM/KILL cleanup.
All VM processes terminate; owned root volume is detached after collection.

## Remaining requirements

This related authored child control is not an independent model task, full source
preparation parity, UID/GID/capability/amd64-kernel equivalence, official test/parser
or selected-case FAIL/PASS grade. No shell/shebang test was performed here. Native
pytest/assertion controls and exact official case/runtime preparation still need
separate frozen gates. No quality or whole-task token/time gain is measured, and
no release claim uses this runtime fix to overwrite adverse model comparisons.

한국어: 게스트 x86 자동 실행 연결을 수정해 동일한 자식 Python 명령이 errno8
실패에서 종료0·출력42로 바뀌었다. 프로젝트 파일은 그대로이며 앞선3개 설정
실패를 보존했다. 호스트 설치·설정 변경은 없고 공식 과제·모델 실행은0회다.
이 결과는 실행 기반의 수정 검증이며 스킬 품질·토큰·시간 절감의 증거가 아니다.
