I’m using the receipt skill to compare HEAD and the working fix in isolated project-local copies, run the seven unchanged tests, and verify that original file bytes and permissions are preserved.

Verified: the existing `<` → `<=` fix merges touching intervals as required.

Compared HEAD `f0e4d86a49a4d6d2d1e7cbc3453070fa3adae517` with working `ranges.py`, SHA-256:
`6755f97b1e89dea7470b55322c46528b715e1c77cc8efbaaccea12e37149746b`

The receipt helper ran native `unittest -v test_ranges` in separate project-local copies. Each process verified `ranges.__file__` resolved inside its copy before running the unchanged tests.

| Test | HEAD | Working |
|---|---|---|
| bridge | FAIL | PASS |
| disjoint | PASS | PASS |
| empty | PASS | PASS |
| input_preserved | PASS | PASS |
| nested | PASS | PASS |
| overlap | PASS | PASS |
| touching | FAIL | PASS |

Actual HEAD assertion failures:

- Bridge: `[(1, 4), (4, 7), (7, 9)] != [(1, 9)]`
- Touching: `[(1, 4), (4, 8)] != [(1, 8)]`

HEAD exited 1; working exited 0. Both ran all seven tests, with no skips, timeouts, or output truncation.

SHA-256 byte checks and permission checks confirmed `ranges.py`, `test_ranges.py`, and `drafts/release.txt` unchanged; each retained mode `0644`. Git status remained unchanged, and `git diff --check` passed. All owned comparison copies were deleted. No original files were edited.
