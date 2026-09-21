# Con Artist selected-input read correction — 2026-09-21

Parent `06353c6`. A real file replacement between inspection and open affected
two paths: selected-input snapshot copying and final original-byte comparison.
The whole-project inventory already checked descriptors; those protections did
not cover these two selected-input reads.

[Native replacement controls](../tests/test_audit_read_races.py) move the inspected
file aside at the actual open boundary and replace it with a FIFO without a writer,
a different regular file, or a symlink. Replacement files contain identical bytes,
so byte comparison alone cannot detect that the earlier inspection is stale.

Before the correction on Python3.9: both FIFO cases exceed the external two-second
probe deadline; all four file/symlink cases are accepted and fail the assertions.
Afterward, all six cases reject. The probe never runs mutation tests or alters a
user project: each uses its own temporary directory and a subprocess deadline.
This is author-native reliability evidence, not a model-cost or latency benchmark.

Validation: all72 `test_audit*.py` tests pass on Python3.11.16. Python3.9 runs the
same72 with10 pytest-dependent skips (pytest is absent), all others passing. The
six replacement subcases run on both interpreters. Repository validation and
English/Korean featured synchronization checks pass; no hosted-CI claim is made.

Both paths now open with nonblocking/no-follow flags and validate the opened
descriptor's regular-file type, device/inode and permission mode against inspection.
Snapshot failures abort; final comparison reports mismatch. Bounded reads still
charge actual bytes when an unchanged inode grows. Existing growth/budget tests
now intercept descriptor opening, preserving their read-size and shared-budget
assertions rather than removing them. Whole-project inventory and child execution
are unchanged.

The claim is narrow: no parent-directory race isolation, same-inode mutation
snapshot, whole-collection deadline or security sandbox. Final preservation still
compares bytes/modes, not historical inode identity throughout execution. No
automatic restoration is added. Both README capability rows and the conditional
audit guide document these limits; entry instructions and charts stay unchanged.

The earlier proposed compact-instruction direction was not repeated: historical
[decision-core](DECISION-CORE-01.md) and mode-disclosure experiments already rejected
similar approaches. Current Necromancer source also already guards its source open;
the actual uncovered path was found by inspecting Con Artist's separate input reads.

한국어: 파일 검사 직후 대상이 바뀌면 선택 파일 복사와 마지막 무변경 확인이 멈추거나
교체된 파일을 받아들이던 문제를 재현·수정했다. 모델 성능 수치가 아니라 실제 도구의
신뢰성 개선이다. 동시 파일 변경 전체를 격리하거나 모든 실행 시간을 제한하지 않는다.
