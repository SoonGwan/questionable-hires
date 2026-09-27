# Owned official root01 — Linux chroot layer application

Dated checkpoint **2026-09-27**, protocol/resource `33d6616f`, parent `df0337cd`.
[Protocol](OWNED-OFFICIAL-ROOT-01-PROTOCOL.md),
[actual outcome](results/owned-official-root-01/result.json),
[whitelisted observed markers](results/owned-official-root-01/observed-markers.txt).
**Zero model turns and zero external benchmark cases.** Eight skills and featured
benchmarks are unchanged. This is runtime feasibility, not token-saving evidence.

## Actual application and imports

All10 previously acquired pinned blobs were verified again before execution.
Header checks rejected unsafe entry names, special entries, whiteouts and reserved
scaffold collisions; none were present. Hard-link targets were checked for absolute
and parent escapes. [Preflight](results/owned-official-root-01/preflight.json).
A fresh owned8GiB case-sensitive APFS sparse image received their contents in
manifest order, through readonly VirtioFS blob shares **inside Linux chroot**.
The ARM initramfs BusyBox and its native musl loader were invoked explicitly from
`/_qh_probe_01`; no host extraction followed image symlinks. Absolute image links
resolve in the guest chroot. Each tar application returned **exit0**, with no tar
error line in the private log. No chown-error bypass or entry skipping was applied.
The first VM run completed in **57.44 seconds**, process0, without timeout.

Inside the applied root, explicit Rosetta executed the actual interpreter at
`/opt/miniconda3/envs/testbed/bin/python3.9`, prefix
`/opt/miniconda3/envs/testbed`, without relocated library aliases/search paths.
Actual imports reported Python **3.9.20**, OpenSSL **3.0.15**, pytest **7.4.4**,
pluggy **1.0.0**, Requests **2.7.0**, and platform **x86_64**. Interpreter marker,
Pythonexit0, all10 layerexit0 and guest poweroff were required; parentexit0 alone
was not accepted. The imported Requests file SHA256 is
`364d408838c8073cab46f4846cefaabb03c5b8d18b530c6d8d563f4d6a3920bf`.

**Import scope limitation:** Requests came from Conda `site-packages`, as shown in
the actual module path. The `-I -B` probe did not import from `/testbed`. Therefore
this is installed-package execution, **not prepared project-source execution**.
The next distinct probe must set the official working directory and check the real
project module path; do not relabel this first attempt or reapply identical layers.

## Process, filesystem and evidence boundaries

[VM source](results/owned-official-root-01/probe.swift) uses one CPU,1GiB RAM,
frozen ARM kernel/initramfs, no network or block storage device, readonly layers
and Rosetta shares, and only the fresh owned writable root share. Guest proc and
reserved scaffold are runtime additions; host existing disks/profiles/trust stores
are unchanged. [Controller](results/owned-official-root-01/control.py) enforces an
independent200-second parent timeout with TERM/KILL of the owned process group;
Swift has180-second guest timeout. Both completed normally. The owned sparse image
is detached after collection and retained privately for the next distinct probe.

Original raw console remains private because extraction failures could expose
project/test paths. Its size3,978 bytes and opaque SHA256 are in the outcome;
public console is an explicit whitelist, not a full or byte-identical transcript.
No config history, project/test/gold body or binary is published. All tar/process
outputs are preserved privately; this attempt had no runtime failure or retry.

APFS/VirtioFS ownership mappings, Linux xattrs/capabilities and full OCI execution
are **not independently verified** by tar exit0. ARM kernel/Rosetta is not an amd64
kernel. No selected tests, parser/FAIL-PASS controls, solver turn, general quality
or whole-task token/time comparison ran. Automatic x86 subprocess/shebang handling
via guest binfmt is also unverified; explicit interpreter execution alone does not
establish it. Earlier adverse cost measurements remain unchanged.

한국어: 고정10개 계층을 Linux chroot 안에서 순서대로 적용했고 각 tar 종료0과
공식 경로의 Python·라이브러리 실행을 확인했다. Requests import는 설치 패키지에서
왔으므로 `/testbed` 프로젝트 소스 실행으로 바꾸지 않는다. 전체 컨테이너의 소유권·
권한 재현, x86 자식 프로세스, 공식 테스트·품질·토큰 절감은 아직 입증하지 않았다.
모델과 외부 과제 실행은0회이며 원본 로그·파일시스템은 비공개로 보존한다.
