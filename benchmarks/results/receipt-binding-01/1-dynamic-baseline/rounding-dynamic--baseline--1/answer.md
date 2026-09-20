I’ll compare both revisions in disposable project-local copies, run the four selected tests with the current test file, and verify the component path inside each test process. I’ll also check that the original files and Git state remain unchanged and remove the scratch copies.


Verified: HEAD fixes both half-cent ties, including negative adjustments. Both controls pass before and after.

- HEAD^: `341f10beb9c0e0e941c70573c08216ba5fdaaaaa`
- HEAD: `f112e2647e333b7b11d0f12471990b6fd0d35748`

Exactly the four selected identities ran under `unittest`, all prefixed `test_rounding.RoundingTests.`:

| Test | Input | HEAD^ | HEAD |
|---|---|---|---|
| `test_positive_half_cent` | `1.005` | `1.00` — FAIL | `1.01` — PASS |
| `test_negative_half_cent` | `-1.005` | `-1.00` — FAIL | `-1.01` — PASS |
| `test_non_tie` | `1.004` | `1.00` — PASS | `1.00` — PASS |
| `test_exact_cent` | `2.30` | `2.30` — PASS | `2.30` — PASS |

Each actual test process asserted that `test_rounding.component.__file__` resolved to its own project-local copy:
- `.rounding-verification-omgp16pp/before/rounding.py`
- `.rounding-verification-omgp16pp/after/rounding.py`

Both explicitly excluded the original tree and the other copy. The unchanged current test file had matching SHA-256 in both processes.

The change from `ROUND_HALF_EVEN` to `ROUND_HALF_UP` produces the required ties away from zero. Original bytes, modes, `notes.txt`, and Git state were verified unchanged. All scratch was removed; no harness or report remains.
