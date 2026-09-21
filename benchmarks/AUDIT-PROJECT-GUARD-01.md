# Optional audit whole-project preservation

2026-09-21, parent `f157b76`. Capability implementation and native controls;
model efficiency/adoption **unmeasured**.

All six [contract-transfer sessions](CONTRACT-AUDIT-01-REVIEW.md) authored their
own whole-tree preservation wrappers. Existing Con Artist comparison support
already replaces copy/run/cleanup orchestration, but its integrity check covers
only selected originals. That is insufficient by itself when a task explicitly
requires preserving unselected notes, added paths and in-root Git metadata. This
is a demonstrated capability gap, not proof it caused non-adoption or all excess
tokens in those sessions.

`guard_project: true` now adds a bounded before/after inventory directly to the
existing audit recipe; default off, unchanged selected-file semantics. It records
file hashes/modes, directories and symlinks without following link targets, including
in-root Git files. Limit:10,000 entries and20MB per inventory; hashing uses bounded
reads and verifies opened regular-file identity. It runs after owned-scratch cleanup
on normal, incomplete and exceptional exits. Changed paths raise without restoration;
failed inventory is not successful preservation. Batch baseline identity includes
the guard inventory, and shared recipes support the flag.

The source root must be trusted, stable and authorized for complete reading. This
is not sandboxing, atomic snapshot isolation, proof about files outside the root,
external worktree Git metadata, transient changes later restored, or adversarial
process containment. A whole-root guard adds I/O; do not enable it for unrelated
work or claim it makes execution faster. It never broadens execution-copy inputs.

Nine tests cover native correct/faulty tests and stronger assertions, real Git
metadata preservation, unselected edits/additions/deletions/modes/Git changes,
default-off no-inventory behavior, invalid options and entry/byte limits before
execution, links/special files, file-to-FIFO replacement, early incomplete checks,
interruptions, batch reuse and real isolated CLI/stdin evidence. Native faulty
probe fails with `AssertionError: 2`; unchanged existing tests still pass both
variants. Changes remain available to the owner rather than being hidden by
automatic restoration. Default recipes retain their prior output shape.

Validation: nine focused tests pass on Python3.9.6 and3.11.16; the complete
`test_audit*.py` selection passes67 tests on Python3.11.16 (6.844s, no skips).
Skill metadata, repository links and featured synchronization checks pass. These
are native regression outcomes, not model benchmarks or a full release rerun.

The implementation is self-contained in `audit.py`; no Receipt installation or
cross-skill import is required. Reference recipes document opt-in use; entrypoint
instructions are unchanged. Both README capability tables are synchronized.
No benchmark numbers or featured charts change. Next evidence needed is actual
fresh-task helper adoption and complete task cost, not an arithmetic estimate
from removed handwritten lines or another run of the exposed contract fixtures.

한국어: 기존 감사 도우미가 선택 파일만 확인하던 빈틈을 선택형 전체 프로젝트
변경 검사로 보완했다. 반복 작성하던 보존 코드를 대체할 수 있지만, 모델의
실제 채택과 토큰 절감은 아직 측정하지 않았다. 기본 비활성이고 검사 범위·
크기를 제한하며, 감지한 변경을 자동으로 덮어쓰거나 복원하지 않는다.
