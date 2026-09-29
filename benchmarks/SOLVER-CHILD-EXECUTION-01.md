# Solver child execution01 — 2026-09-27

Parent `5b6f16b8`; actual guest subprocess routing, zero models/selected issue tests.
This advances the solver tool path, not ordinary skill quality or cost evidence.

Search/reuse: the earlier [binfmt01](OWNED-GUEST-BINFMT-01.md) already established
unregistered native errno8 and the guest-only repair. This control does not repeat
that unchanged failure experiment. It reuses the exact retained registration helper
with only the guest Rosetta path changed to `/rosetta/rosetta`, and the frozen Alpine
modloop SHA256 `da142869626ec9d4543ab46482af10b5ff2c8c1c2e01068ddf32360316a06218`.
No download or host binfmt configuration change.

Append only that modloop, registration and child-control scripts to the existing
RAM runtime/source initramfs. Guest mounts the RAM modloop read-only via its loop/
SquashFS drivers, copies the exact raw binfmt_misc module into guest `/tmp`, loads
it and registers the handler in the same guest `/proc`. The observed handler has
the expected x86 ELF magic/mask and POCF flags, interpreter `/rosetta/rosetta`.
This setup differs from the earlier chroot proc-path failure; this guest has no
second chroot proc namespace. Guest-only devtmpfs remains enabled.

[Actual Python control](results/solver-child-execution-01/child-control.py) calls
`subprocess.run` directly on `sys.executable` without manually wrapping the child
in Rosetta. A normal child returns0, exact `42\n`, empty stderr. A deliberate
failure returns7, exact stdout bytes `00 ff` (base64 `AP8=`), and exact stderr
`expected failure`. Native ARM BusyBox also returns0 with exact `arm-child` output.
A BusyBox check for the host grader path returns1. Every actual subprocess has a
5-second timeout; timeout/kill recovery itself is not exercised by these successful
controls. A child exit7 is preserved as failure, not converted to a passing command.

[Terminal outcome](results/solver-child-execution-01/result.json) and
[complete guest stdout](results/solver-child-execution-01/guest.txt) record actual
handler state and observations: VM executable0, no timeout, exact child proof,
guest stop, elapsed8.209s. The checked guest script unmounts its RAM modloop before
poweroff. No VM or host disk remains attached by this control. All8 original sources
remain included from the preceding frozen RAM inputs, but this is not an8-issue
native regression execution or post-control source inventory.

Configuration has one Rosetta translation share, no arbitrary host data shares,
network or storage devices. The loop mount uses a file inside guest RAM, not a host
disk. [Input hashes](results/solver-child-execution-01/inputs.json) identify modloop
and base/augmented initramfs. Swift, registration/check scripts and complete output
remain retained. VM deadline45 seconds, parent55 seconds, bounded kill on timeout;
cpio30 seconds. Compression/compilation/signing lack an independent whole-attempt
deadline and completed. No solver/model or answer-bearing grader data enters the
guest input set.

Next establish a tool command channel that executes only in the guest, returns
actual output/exit states and preserves the no-host-data boundary. Persisted solver
output transfer, selected native grading, full-cohort runtime constraints and
role-appropriate cost/quality comparisons remain unverified. This control neither
establishes a complete solver bridge nor lower whole-task tokens/faster developer
work across all8. README/skill/featured/hosted claims are unchanged.

한국어: 기존에 검증한 게스트 Rosetta 등록 방식을 재사용해 Python의 직접
자식 실행을 확인했다. 정상0과 실패7, 바이너리 stdout·stderr를 정확히 보존했고
ARM 명령도 실행했다. 호스트 평가 경로는 부재하며 VM은 종료됐다. 이슈 회귀
검사·모델 도구 연결·출력 전달·전체 품질·토큰·속도 비교는 아직 미완료다.
