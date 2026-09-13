I’ll check the project’s test instructions and commit history, then run both implementations in disposable local copies with the same current tests, fixtures, and company configuration.

The commit changes rounding from `ROUND_DOWN` to `ROUND_HALF_UP`. The current tests cover all four requested behaviors. I’ll run the documented command in each copy and check the loaded module paths and hashes to confirm which implementation each copy uses.

Verified using the documented runner, `python3 -B -m unittest -v checks.test_invoice`, in two disposable project-local copies.

Both used identical current tests, fixtures, and company configuration (`USD`, quantum `0.01`). Loaded module paths and content hashes matched:

- Fixed: `ad875f2`, money implementation blob `fa4f37c`.
- Previous: `cd977e1`, money implementation blob `b525756`.

| Behavior | Fixed | Previous |
|---|---|---|
| Positive tie: `1.005` | `1.01` — pass | `1.00` — fail |
| Negative tie: `-1.005` | `-1.01` — pass | `-1.00` — fail |
| Sum before rounding: `1.005 × 2` | `2.01` — pass | `2.01` — pass |
| Empty invoice | `0.00` — pass | `0.00` — pass |

The fix passes all four tests; the previous implementation fails both tie tests. Original files were preserved. Nothing was installed; no external services were used.

[Verification evidence](project/.invoice-verification-cyu_f2bz/report.json) includes full revisions, module paths, hashes, and results.
