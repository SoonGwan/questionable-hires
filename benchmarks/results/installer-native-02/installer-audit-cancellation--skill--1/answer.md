I’m using the requested con-artist skill to trace the four tests, run them against isolated correct and faulty copies, and verify whether they detect a cancellation cleanup defect. I’ll preserve the supplied files and remove all audit scratch afterward.


The cancellation test performs real copies of both skills, then raises a specific `KeyboardInterrupt`. It checks that the same exception propagates, both new targets disappear, and `user.txt` retains its contents.

I’ll change only the outer rollback handler from `except BaseException` to `except Exception`. This realistic regression should bypass cleanup on cancellation while retaining rollback for ordinary copy errors.


The faulty copy fails the cancellation test at the destination-content assertion: both newly created skill directories remain. The original `KeyboardInterrupt` still propagates, and `user.txt` still contains `keep`. The other three tests pass on both copies.

Tracing within each test process confirmed execution of that copy’s `scripts/install.py`. I’ll finish with the four-test suite totals and verify that cleanup leaves the supplied files unchanged.


The existing tests **detect the cancellation cleanup defect**.

The sole mutation changed the outer rollback handler from `except BaseException:` to `except Exception:`. This lets `KeyboardInterrupt` bypass cleanup after both skills have been copied.

| Existing test | Correct exit | Faulty exit |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 0 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 0 |

Each individual invocation ran one native unittest. The combined suite ran **4 tests per copy**: correct **4 passed, exit 0**; faulty **3 passed, 1 assertion failure, exit 1**. There were no setup errors.

The detecting assertion was `tests/test_install.py:303`:

```python
self.assertEqual(list(self.dest.iterdir()), [marker])
```

Expected: only `user.txt`. Observed on faulty code: `user.txt`, `necromancer`, and `receipt`. The preceding exception-identity assertion passed; tracing also observed `user.txt` still containing `keep`.

Execution used `python3 -B <scratch>/runner.py -v test_install.InstallTests.<method>`, with the wrapper invoking native `unittest` through `runpy`. In-process tracing verified each executed installer’s code filename, module path, and `ROOT` belonged to the intended isolated copy. Test files were byte-identical to the originals.

No stronger check was needed. This establishes sensitivity to this specific handler regression; it does not cover every cancellation timing or cancellation combined with cleanup failure. No other test methods ran.

All scratch was removed. Supplied file contents and file inventory were verified unchanged using SHA-256. Only project-local operations and Python’s standard library were used.
