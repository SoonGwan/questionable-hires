I’m using the receipt skill to compare the committed fix with its previous implementation in disposable project-local copies, keeping the tests, fixtures, and company configuration identical.



Verified: the committed fix rounds positive and negative ties away from zero.

Loaded `billing.money` from these revisions, with imports verified inside each disposable copy:

- Before: `cd977e157a823954db7e382d5d60fe258e5498fe`
- After: `ad875f211bc29230a9558a23c38c26713f396035`

The receipt comparison helper ran the documented `unittest -v checks.test_invoice` suite using Python 3, with bytecode disabled. Both runs used identical, hashed current tests, fixtures, supporting code, and company configuration (`USD`, quantum `0.01`).

| Case | Before | After |
|---|---|---|
| Positive tie: `1.005` | `1.00` — FAIL | `1.01` — PASS |
| Negative tie: `-1.005` | `-1.00` — FAIL | `-1.01` — PASS |
| Sum before rounding: `1.005 × 2` | `2.01` — PASS | `2.01` — PASS |
| Empty invoice | `0.00` — PASS | `0.00` — PASS |

Before exited **1**, with two assertion failures; after exited **0**, with all four tests passing. Neither run timed out or truncated output.

The focused implementation diff replaces `ROUND_DOWN` with `ROUND_HALF_UP` in `billing/money.py`; summation remains unchanged.

Verification covers the current fixtures and configuration. Original files were preserved, disposable copies were removed, and nothing was installed or accessed externally.
