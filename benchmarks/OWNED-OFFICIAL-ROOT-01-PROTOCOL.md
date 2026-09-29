# Owned official root01 — frozen private Linux reconstruction

Dated **2026-09-27**, parent `df0337cd`, zero models/external-case runs,
unchanged8skills. Use the [complete verified blobs](OWNED-OFFICIAL-LAYERS-01.md)
of manifest `c83bd92b48356279e868d16d51ec15ca1481fa1bc97968e7a8d935df062f0bf2`.
Verify all blobs again before execution; do not download/relabel different data.

Create one new owned8GiB case-sensitive sparse APFS image and private mountpoint;
never format an existing disk. VM uses the frozen ARM kernel/initramfs, one CPU,
1GiB RAM, no NIC or block device, readonly layer share and Rosetta share, and only
this owned writable root share. Layers are applied in manifest order **inside a
Linux chroot**; do not follow image symlinks with a host extractor. Reuse the actual
initramfs ARM BusyBox and musl loader copied into a reserved guest scaffold, invoked
by its explicit native loader. Assert that no layer path/link claims that reserved
namespace. Reject special entries, unsafe entry names, hardlink escapes or whiteouts
(the pinned inventory observed none), without inventing incomplete whiteout support.
Absolute image symlinks resolve within the chroot. Keep failed extraction output
private because tar errors can contain source/test paths. Export scalar exits and
opaque original hashes only; do not export project/test/gold/history bodies.

Stop layer application on nonzero exit. Preserve the first partially reconstructed
root and original logs if it fails. Do not skip chown/mode errors silently or assert
UID/GID/xattr parity from an APFS/VirtioFS copy. Validate actual loader, Python and
core imports inside the applied root; optionally report requests import/version/path
and opaque imported file hash from prepared image, without running selected tests.
Guest proc/Rosetta mounts and reserved scaffold are explicit runtime additions.
No source repair, dependency upgrade, global host binfmt or profile/trust change.

Swift guest deadline180 seconds; independent parent watchdog200 seconds, then
TERM/KILL of the owned process group. Require actual interpreter marker, version,
module path and exit plus guest poweroff. Retain author/runtime errors without
relabeling first attempts; detach the owned volume after collection. Any source
change or resumption into the partial root requires a documented changed hypothesis.
Even success is user-space runtime feasibility, not Linux/amd64 kernel identity,
Docker/OCI ownership/capability parity, official FAIL/PASS grading or token savings.
Frozen original selected cases and adverse model results remain unchanged.

한국어: 고정한10개 계층을 새 임시 볼륨의 Linux chroot 안에서 순서대로
적용한다. 실패한 루트와 로그를 보존하고 소유권·권한 차이를 숨기지 않는다.
모델·공식 과제 실행은0회이며 실제 Python·프로젝트 import만 검증한다.
전체 컨테이너 재현·공식 테스트·토큰 절감의 증거로 바꾸지 않는다.
