I’m using the receipt skill to compare HEAD and the working implementation in disposable project-local copies, preserving the original files and patch.

The patch changes the parser to split only at the first `=`. The current suite has two regression cases for embedded equals signs and three checks for neighboring behavior. I’ll run all five with identical current samples in both copies and verify that imports resolve within each copy.

Verified the existing fix: `line.split("=", 1)` preserves equals signs within values.

- Before: HEAD `1877068eeac6ccbd648ab48ad3dc6e18b2458644`.
- After: uncommitted `src/settings/parser.py`, SHA-256 `5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`.

The receipt comparison helper ran Python `unittest -v checks.test_parser` in separate project-local copies, using identical current tests and samples, with each copy’s `src` before its root. Implementation and test imports were verified inside each comparison process.

| Test method | HEAD | Working |
|---|---|---|
| `test_token_padding` | Failed: returned `abc`, expected `abc==` | Passed |
| `test_query_value` | Failed: truncated URL at `?x` | Passed |
| `test_whitespace_and_comments` | Passed | Passed |
| `test_empty_value` | Passed | Passed |
| `test_duplicate_last_wins` | Passed | Passed |

Both runs executed all five tests without skips, timeouts, or truncated output. `git diff --check` passed.

Original file hashes and modes remained unchanged, including current tests and `notes.txt`; Git status remained unchanged. Comparison copies were removed. No implementation edits, commits, stashes, resets, extra harness, or report files were created.

Evidence is retrospective and limited to the current suite and samples. Quoting, interpolation, and malformed inputs remain outside the documented scope.
