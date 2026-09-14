I’m using the receipt skill to compare HEAD and the working implementation in disposable project-local copies, with the same current tests and samples. I’ll verify import paths, preserve the original files, and remove the copies afterward.

The patch limits splitting to the first `=`, preserving later equals signs in values. The current suite has five tests: token padding and query values target the defect; whitespace/comments, empty values, and duplicate keys check neighboring behavior. I’ll run all five against both implementations with identical tests and samples.

Verified: the uncommitted fix changes `line.split("=")` to `line.split("=", 1)` and preserves equals signs within values.

- Before: HEAD `1877068eeac6ccbd648ab48ad3dc6e18b2458644`.
- After: working `src/settings/parser.py`, SHA-256 `5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`.

The receipt helper ran Python unittest with `-v checks.test_parser` in separate project-local copies, using identical current tests and samples. Each copy’s `src` preceded its root; implementation and test imports were verified inside each test process’s copy.

| Test | HEAD | Working |
|---|---|---|
| `test_token_padding` | Failed: returned `abc`, expected `abc==` | Passed |
| `test_query_value` | Failed: truncated URL at `?x`, losing `=1&y=2` | Passed |
| `test_whitespace_and_comments` | Passed | Passed |
| `test_empty_value` | Passed | Passed |
| `test_duplicate_last_wins` | Passed | Passed |

Both runs executed all five tests without skips, timeouts, or truncated output. `git diff --check` passed.

All 39 original files checked, including Git files, retained identical bytes and modes. Current tests and unrelated `notes.txt` changes were preserved. Comparison copies were removed; no harness or report file remains.

Evidence covers the existing five tests and samples. Quoting, interpolation, and malformed inputs remain outside the documented scope.
