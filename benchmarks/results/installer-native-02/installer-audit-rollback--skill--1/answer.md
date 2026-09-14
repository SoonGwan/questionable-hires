I’ll use the con-artist skill to trace the four selected tests, run them against isolated correct and faulty copies, and check which assertions detect the rollback defect. I’ll preserve the supplied files and remove all audit scratch before finishing.

I’ll move rollback registration until after `copytree` returns. This models a realistic bug: a copy error leaves the newly created target untracked and therefore unremoved. The selected tests reach this path through mocked copy failures and cancellation; I’ll trace the copied installer in each test process to confirm the binding and filesystem effect.

The selected tests **detect the defect**: moving `installed.append(target)` after `shutil.copytree(...)` leaves a newly created target outside rollback tracking when copying raises.

The native suite ran **4 tests per copy**: correct code passed all 4 (exit **0**); faulty code passed 1 and failed 3 (exit **1**). There were no setup errors or skips. Separate one-test subprocesses confirmed these exits:

| Existing method | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 1 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 1 |

The detecting assertions were:

- **Line 278:** `assertEqual(list(self.dest.iterdir()), [existing])` expected only `unrelated`; the faulty copy also left `receipt` after `OSError("disk full")`.
- **Line 303:** the destination-list assertion expected only `user.txt`; the faulty copy also left `receipt`. The preceding cancellation-identity assertion passed.
- **Line 325:** cleanup attempts expected `['receipt', 'necromancer']`; observed `['necromancer']`. The preceding original-error-identity assertion passed.

Execution used `python3 -B audit_runner.py InstallTests.<method>`, with all four selectors for suite runs. The wrapper invoked the unchanged test file’s native `unittest.main()` through `runpy`. In-process tracing confirmed every installer call’s code filename, module filename, and `ROOT` pointed into the corresponding isolated copy. It also observed the actual leftover directories before test cleanup.

There were **16 total test executions**, including individual reruns. No additional check was needed.

Limitations: this establishes sensitivity to one rollback-registration defect. Disk failures were injected by the existing mocks, not actual disk exhaustion. The direct disk-error test checks exception type and an empty unrelated directory; other selected tests check exception identity and marker contents.

All scratch was removed. All 52 original files retained identical hashes and modes. No other test methods, external services, dependencies, or global installations were used.
