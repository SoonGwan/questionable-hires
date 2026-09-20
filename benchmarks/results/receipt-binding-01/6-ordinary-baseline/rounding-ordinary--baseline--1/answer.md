I’ll run the four selected tests against disposable copies of both revisions, using the unchanged current test file. Each test process will verify its component path, and I’ll check that originals and Git state are preserved after cleanup.

Verified: HEAD fixes both half-cent ties, including negative adjustments. All four selected tests pass.

- **Before — HEAD^:** `341f10beb9c0e0e941c70573c08216ba5fdaaaaa`
- **After — HEAD:** `f112e2647e333b7b11d0f12471990b6fd0d35748`

All identities below have prefix `test_rounding.RoundingTests.`:

| Test | Input | Before | After / expected |
|---|---|---|---|
| `test_positive_half_cent` | `1.005` | `1.00` — FAIL | `1.01` — PASS |
| `test_negative_half_cent` | `-1.005` | `-1.00` — FAIL | `-1.01` — PASS |
| `test_non_tie` | `1.004` | `1.00` — PASS | `1.00` — PASS |
| `test_exact_cent` | `2.30` | `2.30` — PASS | `2.30` — PASS |

Used the supplied Python 3.9.6 interpreter and `unittest`, with `tests/` as an import root. Both copies used byte-identical current tests and ran exactly the four selected identities.

Inside each actual test process, assertions before and after execution verified that `test_rounding.component.__file__` resolved to its corresponding project-local path:

- `.rounding-verification-bfjgi6uy/before/rounding.py`
- `.rounding-verification-bfjgi6uy/after/rounding.py`

Both excluded the original tree and the other copy. The fix changes `ROUND_HALF_EVEN` to `ROUND_HALF_UP`.

Scratch was removed. Original bytes and modes, `notes.txt`, and Git state were verified unchanged. No code, tests, harness, or report was left modified or added.
