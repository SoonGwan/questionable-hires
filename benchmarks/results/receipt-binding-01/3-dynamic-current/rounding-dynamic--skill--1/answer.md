I’m using the receipt skill to compare both revisions in isolated project-local copies, run the four unchanged tests, and verify which component each test process loads.

Verified: `rounding.py` changes `ROUND_HALF_EVEN` to `ROUND_HALF_UP`, fixing half-cent ties for both signs.

- Before (`HEAD^`): `341f10beb9c0e0e941c70573c08216ba5fdaaaaa`
- After (`HEAD`): `f112e2647e333b7b11d0f12471990b6fd0d35748`

| Selected test | Before | After |
|---|---|---|
| `test_positive_half_cent` | FAIL: `1.00`, expected `1.01` | PASS |
| `test_negative_half_cent` | FAIL: `-1.00`, expected `-1.01` | PASS |
| `test_non_tie` | PASS: `1.004 → 1.00` | PASS |
| `test_exact_cent` | PASS: `2.30 → 2.30` | PASS |

Both copies used identical current tests and exactly the four selected identities, through the same interpreter’s `-B -m unittest -v` command with `tests/` as an import root. Native exits: before **1**, after **0**; no skips.

Inside each actual test process, `test_rounding.component.__file__` was verified against its copy’s resolved path, relative to the project:

- PID **28391**: `.receipt-1_ljr83p/before/rounding.py`
- PID **28392**: `.receipt-1_ljr83p/after/rounding.py`

The preservation guard confirmed unchanged original bytes/modes, `notes.txt`, and Git metadata. Final diff checks passed; existing untracked entries remained unchanged. All scratch was removed; no code, tests, harness, or report was left changed.
