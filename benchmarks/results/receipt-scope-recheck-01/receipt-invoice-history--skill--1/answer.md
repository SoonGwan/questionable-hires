I’m using the receipt skill to compare the committed fix with its previous implementation in disposable project-local copies, keeping the tests, fixtures, and company configuration identical.

The commit changes only the rounding mode, from `ROUND_DOWN` to `ROUND_HALF_UP`. The current suite covers all four requested behaviors. I’ll run that unchanged suite against both revisions with the same USD configuration and fixtures, and check which implementation each run loads.

Verified using the documented `python3 -B -m unittest -v checks.test_invoice` runner through the receipt comparison helper.

Loaded implementation revisions, with imports verified inside each disposable copy:

- Before: `cd977e157a823954db7e382d5d60fe258e5498fe`
- After: `ad875f211bc29230a9558a23c38c26713f396035`

Both runs used identical current tests, fixtures, supporting code, and company configuration (`USD`, quantum `0.01`).

| Behavior | Before | After |
|---|---|---|
| Positive tie `1.005` | `1.00` — FAIL | `1.01` — PASS |
| Negative tie `-1.005` | `-1.00` — FAIL | `-1.01` — PASS |
| Sum before rounding: `1.005 × 2` | `2.01` — PASS | `2.01` — PASS |
| Empty invoice | `0.00` — PASS | `0.00` — PASS |

Before exited **1** with two assertion failures; after exited **0**, all four tests passing. Neither run timed out or truncated output.

The focused committed diff changes only `ROUND_DOWN` to `ROUND_HALF_UP` in `billing/money.py`, preserving summation before rounding.

Evidence is limited to these four current cases. Original files were preserved, disposable copies removed, and nothing was installed or accessed externally.
