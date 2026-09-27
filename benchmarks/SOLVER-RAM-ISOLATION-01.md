# Solver RAM isolation01 — 2026-09-27

Parent `ec04c803`; actual guest source staging for all8 fixed external issues,
zero models or issue tests. No skill-performance or complete solver-readiness claim.

The retained [ARM Linux boot controller](OWNED-LINUX-VM-01.md) is reused with no
networking, storage devices or host directory shares. Its original frozen kernel
and initramfs remain unchanged. The new initramfs appends a gzip-compressed newc
archive containing only eight source tar archives, their checksum manifest and a
guest check script. This uses the [pristine source staging](EXTERNAL-BUNDLE-02-SOLVER-STAGING-01.md),
excluding `.git`; genuine generated version files remain declared source inputs.
No host grading directory, gold/test patch, required label list or private grading
log is copied or mounted. The source archives total25,886,720 bytes.

[Input identities](results/solver-ram-isolation-01/inputs.json) preserve all archive
hashes and base/augmented initramfs hashes. The original initramfs SHA is checked
against its retained boot evidence before appending; it is not a mutable download.
[Swift source](results/solver-ram-isolation-01/probe.swift), entitlement and
[guest check](results/solver-ram-isolation-01/check.sh) are retained. One newly owned
executable receives only an ad-hoc virtualization signature. No global runtime,
host service, account or security configuration changes.

[Actual guest output](results/solver-ram-isolation-01/guest.txt) checks all eight
archive SHA256 values and extracts every project into guest RAM. Each extracted
project has no `.git`. Guest checks confirm the host grading directory and `/Users`
are absent, then print the explicit all-source completion proof. This establishes
the configured no-share source staging boundary, not a general VM escape/security
audit or verification of every conceivable host path. File-by-file guest mode
verification, Python execution and native issue checks are not performed.

[Terminal result](results/solver-ram-isolation-01/result.json): executable0, no
timeout, all8 source proofs and guest poweroff observed, elapsed4.125s. The Swift
deadline is25 seconds; parent wait35 seconds followed by bounded process-group kill
on timeout. Swift compilation and ad-hoc signing are not independently bounded;
both completed before the actual boot. The only devices are serial console and
entropy plus RAM boot; configuration provides no host filesystem or network device.
No VM or root disk mount is left running by this control.

This is stronger than same-account host staging: the actual guest cannot address
the host grader through an exported filesystem device. It remains only an ARM
BusyBox RAM guest. It has no target Python runtimes, model tool bridge, durable solver
output route, final execution protocol or native grading readiness. Any later tool
bridge must execute entirely inside the guest and retain this input boundary;
mounting the previous answer-bearing official grading root would invalidate it.
The full fixed cohort's runtime/reporting/gold failures remain outstanding. None
is retried or replaced here, and all8 developer quality plus joint whole-task
token/time reduction is still unproven. README, skills, featured metrics and hosted
efficiency claims are unchanged.

한국어: 공유 폴더·디스크·네트워크 없는 실제 Linux VM에 8개 원본 소스만 넣고
해시 확인·게스트 RAM 압축 해제·평가 자료 경로 부재·정상 종료를 확인했다.
Mac의 같은 계정 폴더와는 다른 실제 게스트 경계다. 다만 Python 실행 환경과
모델 도구 연결·출력 전달·전체 평가 규약이 없으므로 풀이 비교 준비 완료가
아니다. 모델·이슈 테스트0회이며 전체 품질·토큰·속도 목표는 미달이다.
