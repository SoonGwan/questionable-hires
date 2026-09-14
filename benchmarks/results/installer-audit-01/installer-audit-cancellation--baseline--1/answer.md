I’ll read the project instructions and installer code, then run the four specified tests against isolated correct and faulty copies. I’ll verify which installer each test loads and remove all audit scratch before finishing.


The cancellation test completes the second skill’s copy, raises a specific `KeyboardInterrupt`, then checks that the same exception propagates and only the unrelated marker remains. I’ll change the outer rollback handler from `except BaseException` to `except Exception`—a realistic defect that should leave ordinary error handling intact but skip cancellation cleanup.


The existing tests **detect the cancellation cleanup defect**.

I changed only the outer handler at `scripts/install.py:99` in the faulty copy:

```diff
-    except BaseException:
+    except Exception:
```

This lets `KeyboardInterrupt` bypass rollback, leaving newly copied skills behind.

Actual native results:

| Test method | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 0 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 0 |

Each isolated method run executed **1 test**. The initial suites each executed **4 tests**: correct had 4 passes, exit 0; faulty had 3 passes and 1 assertion failure, exit 1. All runs had zero errors or skips.

The detecting assertion was `tests/test_install.py:303`:

```python
self.assertEqual(list(self.dest.iterdir()), [marker])
```

Expected: only `user.txt`. Observed in the faulty copy: `user.txt`, `necromancer/`, and `receipt/`, with four copied files in each skill directory. The original cancellation object still propagated, and `user.txt` still contained `keep`. Execution tracing confirmed cancellation skipped rollback; the correct copy removed both targets.

For every run, I verified the installer’s `__file__`, `ROOT`, and function code filename pointed into the intended isolated copy, then traced actual calls to that function. Copied test files remained byte-identical. No stronger check was needed.

Limitations: this verifies one mutation and cancellation injected after the second real copy completes; it does not establish coverage of every interruption timing or cancellation combined with cleanup failure. Only the four authorized methods ran.

Project instructions were followed using Python’s standard library only. All scratch was removed; before/after comparison confirmed all 90 original filesystem entries retained their contents, modes, and structure.
