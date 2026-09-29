# Initial working-file evidence

2026-09-27, parent `ca71b596`. Runner correction, not a skill performance result.

The [integration05 review](ALL-EIGHT-CURRENT-05-REVIEW.md) retains an evidence
gap: initial untracked working-file permission modes were not directly captured.
Existing Git trees cannot represent every ignored file or full permission bits.
This change does not establish those historical modes.

The runner reuses its resource inventory to retain regular-file byte digests and
permission bits (including special bits), plus symlink targets, before starting
the model process and timer. `project-files.before-model.json` stays outside the
model's workspace. It includes ignored/untracked files and owner configuration,
excluding `.git` and `.agents/skills`; installed skills already have a separate
inventory. Metadata retains the local artifact name, digest and scope. The raw
inventory remains local and is not automatically exported. No prompt or paid
model call is added.

This is not an atomic snapshot, directory-metadata record, transient-change
detector or automatic preservation verdict. Symlink targets are recorded rather
than opened. A capture read failure stops before launching the model.

The original runner fails the updated regression control because the inventory
is absent before launch. The updated control checks an ignored file's actual
`01640` mode and digest, then changes its mode to `0600` during the simulated
model invocation: the initial record stays unchanged. It also checks owner
configuration inclusion, excluded metadata/resources, artifact digest and raw
export exclusion. The runner's27 tests and all45 `test_benchmark*.py` tests pass
on local macOS/Python3.11.6. A Git-free archive of the parent with the two changed
Python files overlaid also passes45/45, with no skips, in3.638s (checkout3.673s).
These are local author controls, not model evidence or a full release matrix.

한국어: 이후 측정부터 모델 실행 전 미추적·무시된 파일의 내용 해시와 실제
권한을 별도로 기록한다. 원본 목록은 로컬에만 보관한다. 과거 결과의 미확인
권한을 소급해서 입증하거나 토큰 절감 성과로 해석하지 않는다.
