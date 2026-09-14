I’ll use the requested con-artist skill to trace the four tests, run them against isolated correct and faulty copies, and check which assertion detects the cancellation defect. I’ll preserve the supplied files and remove all audit scratch afterward.


The cancellation test performs real copies, then raises a specific `KeyboardInterrupt` after the second skill is copied. It checks that the same exception propagates, both new targets disappear, and `user.txt` remains intact. I’ll narrow the outer rollback handler from `BaseException` to `Exception`: a realistic change that would leave cancellation outside the cleanup path.


The existing tests **detect the cancellation defect**.

I changed only the copied installer’s outer rollback handler from `except BaseException:` to `except Exception:`. This lets `KeyboardInterrupt` propagate without removing newly created targets.

Using `python3 -B .agents/skills/con-artist/scripts/audit.py --spec -`, the initial native suite ran exactly the four requested methods:

- Correct copy: **4 tests passed; exit 0**.
- Faulty copy: **3 passed, 1 assertion failure; exit 1**.
- No setup errors, skips, or timeouts.

Separate executions established actual test-specific process exits; each ran one test:

| Test | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 0 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 0 |

The detecting assertion is `tests/test_install.py:303`:

```python
self.assertEqual(list(self.dest.iterdir()), [marker])
```

Expected: only `user.txt`. Observed on the faulty copy: `user.txt`, `necromancer/`, and `receipt/`. The preceding exception-identity assertion passed; tracing also confirmed `user.txt` still contained `keep`. Thus the reachable defect is failed rollback, while the original cancellation and unrelated content survive.

Same-process binding checks verified the test’s `installer` object and function code pointed to each copied `scripts/install.py`. Execution tracing confirmed all four tests called that copied function. The cancellation test uses real filesystem copies and injects cancellation after the second copy completes.

No stronger check was needed. This establishes protection against this specific fault, not every interruption timing or cancellation combined with cleanup failure. No other test methods ran.

All supplied files were preserved. The helper verified unchanged bytes and modes for its 10 input files and removed its scratch; the final check found no audit scratch or bytecode caches.
