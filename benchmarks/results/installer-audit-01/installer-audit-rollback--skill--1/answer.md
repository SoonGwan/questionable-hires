I’ll use the requested con-artist skill to trace the four tests, run them against isolated correct and faulty copies, and verify whether any failure detects the cleanup defect. I’ll preserve the supplied files and remove scratch before finishing.

The tests call `install()` directly and inject failures through `shutil.copytree`. I’ll move rollback registration until after copying—a realistic ordering defect that leaves the newly created target untracked if copying fails. Same-process tracing will verify which installer executes and what remains after rollback.

The existing tests **detect the defect**. No stronger check was needed.

I moved `installed.append(target)` after `shutil.copytree(...)` in the faulty copy. When copying raises, the newly created target is untracked and survives rollback.

The initial native suite ran exactly **4 tests per implementation**:

- Correct: **4 passed**, exit **0**.
- Faulty: **1 passed, 3 assertion failures**, exit **1**.
- No setup errors, skips, or timeouts.

Separate one-test processes confirmed these exits; each ran exactly **1 test**:

| Test | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 1 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 1 |

The detecting assertions in `tests/test_install.py` were:

- **Line 278:** `assertEqual(list(self.dest.iterdir()), [existing])` expected only `unrelated`; observed both `receipt` and `unrelated` after `OSError("disk full")`.
- **Line 303:** expected only `user.txt`; observed an additional `receipt` directory after cancellation.
- **Line 325:** expected cleanup attempts `['receipt', 'necromancer']`; observed `['necromancer']`. The preceding assertion preserving the original exception’s identity passed.

Execution used `python3 -B .agents/skills/con-artist/scripts/audit.py --spec -`, with explicit unittest method selectors. Same-process checks verified the tests’ actual `installer` binding and function source path; tracing recorded execution inside each copied `scripts/install.py`, the injected exceptions, and remaining destination entries. Test-file hashes matched across copies.

Limitations: this establishes sensitivity to one rollback-registration defect. Disk errors were injected through mocks, not physical disk exhaustion. The direct disk-error test checks exception type and preserves an empty unrelated directory; it does not itself verify error identity or unrelated file bytes.

Only the four authorized methods ran. All supplied paths, file bytes, and modes remained unchanged, and all scratch was removed.
