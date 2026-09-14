I’ll use the receipt skill to compare HEAD and the working parser in disposable project-local copies, run the same current tests and samples in both, and verify that the original files remain unchanged.

The patch changes `split("=")` to `split("=", 1)`, preserving equals signs within values. The five current tests cover token padding, query strings, whitespace/comments, empty values, and duplicate keys. I’ll run all five with identical sample bytes in both copies and check imports in each test process.

Verified: the existing fix preserves equals signs within values.

Before: HEAD `1877068eeac6ccbd648ab48ad3dc6e18b2458644`.
After: working `src/settings/parser.py`, SHA-256 `5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`, changing `split("=")` to `split("=", 1)`.

The receipt comparison helper ran Python 3.9.6 `unittest -v checks.test_parser` in separate project-local copies with identical current tests and samples. Each copy’s `src` preceded its root; same-process checks confirmed implementation and test imports resolved inside that copy.

| Test | HEAD observation | Working result |
|---|---|---|
| `test_token_padding` | Failed: returned `abc`, expected `abc==` | Passed |
| `test_query_value` | Failed: URL truncated at `?x`, losing `=1&y=2` | Passed |
| `test_whitespace_and_comments` | Passed | Passed |
| `test_empty_value` | Passed | Passed |
| `test_duplicate_last_wins` | Passed | Passed |

Both runs executed all five methods without skips, timeouts, or truncated output. `git diff --check` passed.

All original file contents and modes remained unchanged, including current tests and unrelated `notes.txt` changes. Comparison copies were removed; no harness, report, or other added paths remain.

This is retrospective evidence for the five supplied cases. Quoting, interpolation, and malformed inputs remain outside the documented scope.
