I’m using the receipt skill to compare HEAD with the working fix in isolated project-local copies, preserving the originals and capturing each test outcome.

The six tests cover two cycle failures and four ordering controls. I’ll run the unchanged suite in both copies using the receipt helper, which checks the loaded `planner` path inside each test process. I’ll also verify that `planner.py`, `test_planner.py`, and `notes.txt` retain their bytes and permissions.

HEAD produced the expected assertion failures for both cycles: it raised `RecursionError` instead of `ValueError("cyclic dependency")`. All four controls passed, and the working fix passed all six tests. The comparison copies were removed and the originals are unchanged; I’m removing one tool-generated `xcrun_db` scratch file before the final cleanup check.

Verified: the working fix detects active-node cycles and raises the required `ValueError`.

- Before commit: `7180b34dc5ee5c3c309eb04346860c88a477f25e`
- Working `planner.py` SHA-256: `5a54575496ae852d3d508124427b69b5d6a016cf55c798ab7fe8a27ff0ac3977`

The receipt helper ran native `unittest -v test_planner` with identical current tests in separate project-local copies. Each process verified that the imported `planner` resolved inside its copy before running tests.

| Test | HEAD | Working |
|---|---|---|
| `test_chain` | PASS | PASS |
| `test_empty` | PASS | PASS |
| `test_independent_order` | PASS | PASS |
| `test_self_cycle` | FAIL | PASS |
| `test_shared_dependency` | PASS | PASS |
| `test_two_node_cycle` | FAIL | PASS |

Both captured HEAD assertion failures were:
```text
('RecursionError', 'maximum recursion depth exceeded')
!= ('ValueError', 'cyclic dependency')
```

HEAD exited 1; working exited 0. Neither run skipped tests, timed out, or truncated output. `git diff --check` passed.

Original bytes and permissions of `planner.py`, `test_planner.py`, and `notes.txt` are preserved. Comparison copies and generated scratch were deleted; Git status matches its initial state.
