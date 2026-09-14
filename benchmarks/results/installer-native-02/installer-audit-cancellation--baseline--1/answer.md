I’ll read the project instructions and installer tests, then run the four specified methods against isolated correct and faulty copies. I’ll trace which installer each suite exercises and remove the scratch files when finished.

The cancellation test copies both skills before raising a specific `KeyboardInterrupt`, then checks that the same exception propagated and only the unrelated file remains. I’ll change only the outer rollback handler from `except BaseException` to `except Exception`—a realistic defect that would let cancellation bypass cleanup.

The trace shows that cancellation bypasses rollback in the faulty copy. My diagnostic callback then tried to inspect the destination after unittest had removed its temporary directory, so that run isn’t valid detection evidence. I’ll rerun with the standard unittest result handler and capture the filesystem state before test cleanup.

The existing tests **detect the cancellation rollback defect**. No stronger check was needed.

I changed only the outer rollback handler in the isolated faulty copy of `scripts/install.py:99`:

```diff
-    except BaseException:
+    except Exception:
```

This realistic narrowing excludes `KeyboardInterrupt`, allowing cancellation to propagate without removing newly created targets.

Both copies ran precisely the four requested, unchanged test methods:

| Native method | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 0 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 0 |

The complete correct suite ran **4 tests, all passed, exit 0**. The faulty suite ran **4 tests, 3 passed, 1 assertion failure, exit 1**. Both had zero errors and skips. Individual subprocess runs each executed one test.

The detecting assertion was `tests/test_install.py:303`:

```python
self.assertEqual(list(self.dest.iterdir()), [marker])
```

Expected: only `user.txt`. Observed in the faulty copy: `user.txt`, `necromancer`, and `receipt`. The preceding exception-identity assertion passed, and tracing observed `user.txt` still contained `"keep"`. Thus the reachable defect was leftover installation targets despite propagation of the original cancellation.

For every run, I verified the imported module path, `install.__code__.co_filename`, and `ROOT` pointed into the corresponding isolated copy. Execution tracing confirmed each test called that copied implementation; cancellation reached rollback in the correct copy and bypassed it in the faulty copy.

An initial diagnostic callback failed after test cleanup; those aborted runs were excluded from detection evidence and rerun successfully using the standard unittest result handler.

Limitations: this establishes detection of one mutation using the existing injected cancellation after the second real copy, not arbitrary interruption timing or actual OS signals. No other methods ran. Project instructions were followed; only Python’s standard library was used. All scratch was removed, and original file hashes and modes were unchanged.
