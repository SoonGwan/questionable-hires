# Receipt selected-read01 — reproduced open-time replacement, then rejection

2026-09-21. Before resource `266798e`. No model sessions or timing-gain claim.

Inspection after the all-eight cost review identified that `compare.py` used
`Path.open` for selected files, unlike its descriptor-checked optional tree guard.
The comparison's child deadline does not cover a blocking parent-side file read.
`tests/test_receipt_selected_read.py` deterministically replaces an owned input
at the open boundary, without external paths or concurrent scheduling assumptions.

Before the correction, three controls establish distinct failures:

| Open-time replacement | Before | After |
| --- | --- | --- |
| FIFO with no writer | Outer3-second process deadline expires | Rejected without blocking |
| Symlink to owned same-byte file | Accepted | Rejected |
| Another regular file with identical bytes | Accepted | Rejected |

The before test exited1 with two assertion failures and one TimeoutExpired;
the outer subprocess supervisor terminated and reaped the blocked child. This
does not establish a production incident or an unbounded wait duration measurement.
Afterward all three controls complete in the same test without an error.

`read_limited` now observes a regular file using lstat, opens with
`O_NOFOLLOW|O_NONBLOCK`, and compares descriptor type/device/inode/mode before
reading at most limit+1 bytes. Both initial selected snapshots and final integrity
reads use it. The recipe, native runner, provenance checks and child deadlines
are unchanged. Files are not automatically restored after a detected mutation.

Two integration checks establish that an initial replacement prevents native
execution and a final-read replacement rejects after both simulated native checks
while owned copies are removed. These lifecycle checks deliberately mock native
execution; they are not extra model or native correctness observations. Existing
native before/after tests continue to exercise actual comparisons.

The first helper-suite runs failed one old budget test because it observed
`Path.open`, no longer used. Its hook was moved to descriptor opens, retaining
the assertion that the overflow file must never be opened. The post-stat growth
control now grows the real owned file during descriptor open and still checks
the remaining budget, pre-execution rejection and cleanup. This author-test
adaptation is disclosed, not an excluded production failure.

Python3.9:49 helper checks plus the three-case race test pass. Python3.11.16 runs
all175 `test_receipt*.py` checks in65.659s: OK, no skips. This is a targeted
reliability correction, not proof of broad performance or release readiness.
All13 build checks pass on Python3.11; skill structure, repository validation,
localized featured synchronization and diff checks pass.
The preceding1,010-test whole-suite checkpoint predates this change.

Remaining limits: snapshots are not atomic; same-inode concurrent writes,
parent-directory races, mutations restored between observations, escaped test
effects and non-file metadata remain outside this guarantee. No sandbox or
complete filesystem race protection is claimed. Bilingual capability descriptions
and conditional details are updated; the entry body and featured graphs are not.

한국어: Receipt의 파일 읽기 경계에서 FIFO 교체에 멈추고 링크·다른 파일 교체를
수용하는 문제를 재현했다. 수정 후 세 경우를 모두 거부하고 시작·종료 검사 흐름도
확인했다. 실제 신뢰성 수정이며 모델 토큰 절감 수치로 환산하지 않는다. 동일 파일
내부의 동시 쓰기와 상위 디렉터리 교체 등은 여전히 원자적으로 차단하지 못한다.
