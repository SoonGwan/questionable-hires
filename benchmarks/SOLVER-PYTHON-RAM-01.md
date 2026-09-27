# Solver Python RAM01 — 2026-09-27

Parent `307a2d25`; actual guest Python feasibility, zero models/issue tests. All8
selected source archives remain in guest RAM as in [source isolation01](SOLVER-RAM-ISOLATION-01.md).

The existing [official Python runtime extraction](OWNED-OFFICIAL-PYTHON-01.md)
is reused, without its previous host runtime share. Its owned case-sensitive sparse
image is attached read-only at a new owned mountpoint only for staging, then detached
before VM boot. Only the extracted environment/glibc runtime subtree is archived;
no official project/grading root is copied. The253,747,200-byte tar is appended to
the prior source initramfs in a gzip/newc member, alongside a guest runtime check.
[Input hashes](results/solver-python-ram-01/inputs.json) identify the runtime tar and
base/augmented initramfs. The guest verifies the tar hash before extraction, then
deletes that guest-only tar to release RAM space.

The new VM has no storage or network devices and no arbitrary host data-directory
shares. It has **one Apple Rosetta translation directory share**, required for the
x86 interpreter; unlike the preceding zero-share source boot, it is not a zero-share
configuration. The executable and scripts are retained under
`results/solver-python-ram-01/`. No host grader/runtime/project directory is exported.
Guest-only proc/sys mounts, Rosetta mount, glibc loader link and native library path
enable the relocated Python. No host account/runtime/service configuration changes.

First [1GiB attempt](results/solver-python-ram-01/result.json) fails to extract the
runtime with `No space left on device`, despite all8 source proofs and VM exit0.
The parent verifier correctly exits1 because Python and grader-path proofs are
missing. [Original guest output](results/solver-python-ram-01/guest.txt) and original
Swift configuration remain unchanged. Do not count normal VM shutdown as Python
success or silently amend this failed resource.

The second configuration increases guest RAM to1.5GiB and adds a `df` diagnostic,
using the identical runtime/source initramfs. The diagnostic itself cannot find `/`
in the mount table and fails; it is outside the checked Python script, remains in
the output, and is not a successful capacity measurement. Actual extraction and
Python checks then succeed. This supports insufficient guest space in the first
attempt; it does not establish a universal memory threshold or efficiency gain.

[Second terminal result](results/solver-python-ram-01/result-memory1536.json):
executable0, no timeout, all8 source proofs, exact Python proof, absent host grader
paths and normal guest shutdown, elapsed7.536s. Actual native output records Python
3.9.20, pytest7.4.4, OpenSSL3.0.15 and SQLite3.45.3, prefix `/runtime/env`. The Python
check imports pytest/pluggy/SSL/SQLite, creates an in-memory table, writes7 and
asserts the read returns `[(7,)]`. This is runtime/stdlib execution, not native pytest
fixture execution or any selected issue import. Public proof checks use complete
output lines, not the echoed command text. Both VM processes are terminal; the
owned host disk was detached before either boot and no VM disk was configured.

Each VM has a25-second internal deadline and35-second parent wait, followed by a
bounded process-group kill if needed. Cpio is bounded30 seconds; archive construction,
compression, image attachment, compilation and signing have no independent parent
deadline and all completed. Fresh controlled issue imports, selected native grading,
child-process execution, solver tool bridge/output delivery and final isolation
protocol remain unverified. A host shell bridge or sharing the earlier answer-bearing
grading root would invalidate this boundary. No all8 role quality, whole-task token
saving or faster developer completion is claimed; ordinary skills/README/featured/
hosted performance claims are unchanged.

한국어: 호스트 runtime 폴더를 공유하지 않고 실제 Python을 게스트 RAM에서
실행했다. Rosetta 전용 공유1개는 필요하며 일반 호스트 폴더·디스크·네트워크는
없다. 첫1GiB 공간 부족 실패를 보존하고1.5GiB에서 Python·기본 라이브러리·SQLite
읽기 쓰기·소스8개 확인·정상 종료를 검증했다. df 진단 실패도 유지한다. 실제
이슈 import·검사·모델 도구 연결은 미실행이며 전체 품질·토큰·속도 목표는 미달이다.
