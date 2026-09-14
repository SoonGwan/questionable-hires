I’ll use the receipt skill to compare HEAD and the working parser in disposable project-local copies, preserving the original files and running the same current tests and samples in both.

The patch changes `split("=")` to `split("=", 1)`, matching the requirement to preserve equals signs within values. The current suite has five tests: two exercise this defect, and three check whitespace/comments, empty values, and duplicate keys. I’ll run all five in each copy and use the helper’s whole-project guard to check that originals remain unchanged.

Verified: the existing fix preserves equals signs within values.

- Before: HEAD `1877068eeac6ccbd648ab48ad3dc6e18b2458644`.
- After: working `src/settings/parser.py`, SHA-256 `5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`.
- Change: `line.split("=")` → `line.split("=", 1)`.

The receipt comparison helper ran Python unittest `-v checks.test_parser` in separate project-local copies using identical current tests and sample files.

| Test | HEAD | Working |
|---|---|---|
| `test_token_padding` | Failed: returned `abc`, expected `abc==` | Passed |
| `test_query_value` | Failed: truncated URL at `?x` | Passed with full `?x=1&y=2` |
| `test_whitespace_and_comments` | Passed | Passed |
| `test_empty_value` | Passed | Passed |
| `test_duplicate_last_wins` | Passed | Passed |

Both runs executed all five tests without skips, timeouts, or truncated output. Same-process checks confirmed implementation and test imports resolved inside their respective copies, with `src` preceding the copy root.

The whole-project guard reported unchanged originals, including current tests and unrelated `notes.txt` edits. `git diff --check` passed. Comparison copies were removed; no harness or report file was retained.

Evidence covers these five supplied cases. Quoting, interpolation, and malformed inputs remain outside the documented scope.
