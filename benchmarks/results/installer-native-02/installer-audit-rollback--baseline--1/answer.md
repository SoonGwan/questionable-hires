I’ll read the project instructions and installer, then run the four named tests against isolated unchanged and faulty copies. I’ll verify which implementation each test executes and remove the scratch files before finishing.

The installer records each new target before copying into it. I’ll test a defect that moves that bookkeeping step until after the copy succeeds; a disk-copy error would then leave the reserved target out of rollback.

The named tests check for that leftover target, and also cover cancellation and cleanup failures. I’ll run all four unchanged and trace execution to confirm they use the copied installer.

The existing tests **detect the defect** at the requested boundary.

I read `AGENTS.md` and used only Python’s standard library. In an isolated faulty copy, I moved `installed.append(target)` from before `shutil.copytree(...)` to immediately after it. This realistic bookkeeping error leaves a newly created target untracked when copying raises.

Initial native suite results:

| Implementation | Tests run | Passed | Failures | Errors/skips | Exit |
|---|---:|---:|---:|---:|---:|
| Unchanged | 4 | 4 | 0 | 0/0 | 0 |
| Faulty | 4 | 1 | 3 | 0/0 | 1 |

Each method was then run individually, with these actual process exits:

| Test method | Unchanged | Faulty |
|---|---:|---:|
| `test_selected_skill_is_complete` | 0 | 0 |
| `test_copy_failure_rolls_back_only_new_targets` | 0 | 1 |
| `test_cancellation_cleans_all_new_targets_and_preserves_unrelated` | 0 | 1 |
| `test_cleanup_failure_preserves_error_and_attempts_remaining_targets` | 0 | 1 |

There were **16 native test executions total**, including individual reruns. No other methods ran.

The detecting assertions in `tests/test_install.py` were:

- **Line 278:** `assertEqual(list(self.dest.iterdir()), [existing])`. After `OSError('disk full')`, expected only `unrelated`; observed `receipt` and `unrelated`. The newly reserved directory survived rollback.
- **Line 303:** Expected only `user.txt`; observed an additional `receipt` directory after cancellation.
- **Line 325:** Expected cleanup attempts `['receipt', 'necromancer']`; observed `['necromancer']`.

These were assertion failures, with no setup errors. Original exception identity assertions passed in the cancellation and cleanup-failure tests.

For provenance, the runner verified each imported installer’s `__file__`, function `co_filename`, and `ROOT` against its isolated copy. Execution tracing confirmed every test entered that copy’s `install()` and reached the relevant copy/rollback lines. Copied test files were byte-identical to the supplied file; the correct installer was also byte-identical.

Limitations: this evaluates one mutation. Disk and cleanup errors were injected by the existing mocks, rather than actual disk exhaustion. The disk-error test checks an empty unrelated directory and exception type, not unrelated file bytes or exception identity. No stronger check was needed because the mutation was detected.

All scratch was removed. Before/after inventories confirmed supplied files, bytes, modes, and directory structure were preserved.
