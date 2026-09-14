I’ll inspect the project instructions and installer, then run the four specified tests against isolated correct and faulty copies. I’ll verify which installer each run loads and remove the scratch files afterward.

I’ll test a bookkeeping defect that records a new target only after `copytree` succeeds. If copying raises after target creation, rollback would miss that target. I’ll run each requested method in a separate process and trace execution to verify it uses the copied installer.

The existing tests **detect the defect**. No stronger check was needed.

The faulty copy moved `installed.append(target)` from before `shutil.copytree(...)` to after it. This realistic bookkeeping error leaves a newly created target untracked when copying raises, so rollback misses it.

I ran exactly the four requested native methods, unchanged, individually in isolated processes:

| Test method | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 1 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 1 |

**Actual counts:** correct: 4 tests, 4 passed; faulty: 4 tests, 1 passed, 3 assertion failures. Neither run had setup errors, other test errors, or skips.

Detecting assertions in `tests/test_install.py`:

- **Line 278:** `assertEqual(list(self.dest.iterdir()), [existing])` expected only `unrelated`; observed `receipt` plus `unrelated`.
- **Line 303:** expected only `user.txt`; observed `user.txt` plus `receipt`.
- **Line 325:** expected cleanup attempts `['receipt', 'necromancer']`; observed `['necromancer']`.

Module-path and function-code-path checks verified each process loaded its copied `scripts/install.py`. Execution tracing confirmed the copied installer actually ran. At `OSError("disk full")`, `receipt` already existed: the correct copy tracked and removed it; the faulty copy had an empty rollback list and left it behind. Original-exception identity assertions in the cancellation and cleanup-failure tests passed before their detecting assertions failed.

Limitations: disk and cleanup failures were injected by the existing mocks, not actual disk exhaustion. This evaluates one mutation, not every possible rollback defect. The immediate disk-error test checks exception type and an empty unrelated directory; stronger error-identity and unrelated-file checks occur in separate scenarios.

Project instructions were followed. Only Python’s standard library was used; no other test methods ran. All scratch was removed, and supplied file hashes and modes remained unchanged.
