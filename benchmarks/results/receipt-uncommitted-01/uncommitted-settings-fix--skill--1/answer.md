I’m using the receipt skill to compare HEAD and the working implementation in disposable project-local copies, with the same current tests and samples. I’ll verify import locations and preserve the original files.

The patch changes splitting to stop at the first `=`, preserving later equals signs in values. The current suite has five tests: token padding and query values exercise that defect; the other three check comments/whitespace, empty values, and duplicate keys. I’ll run all five against both implementations and check original-file integrity afterward.

Verified: the existing fix preserves equals signs within values by changing `line.split("=")` to `line.split("=", 1)`.

Both disposable project-local copies ran `python3 -B -m unittest -v checks.test_parser` using Python 3.9.6, identical current tests, support files, and samples. Parser and test imports resolved inside their respective copies.

| Existing test | HEAD | Working implementation |
|---|---|---|
| `test_token_padding` | FAIL: returned `abc`, expected `abc==` | PASS |
| `test_query_value` | FAIL: truncated URL at `?x`, losing `=1&y=2` | PASS |
| `test_whitespace_and_comments` | PASS | PASS |
| `test_empty_value` | PASS | PASS |
| `test_duplicate_last_wins` | PASS | PASS |

All five executed without skips: HEAD had two assertion failures; working implementation passed all five.

Before commit: `8eb4af505251831800639a7a647a63c72601852c`  
Current uncommitted `settings/parser.py` SHA-256: `5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`

`git diff --check` passed. All 37 original files retained identical bytes and permissions, including current tests and unrelated `notes.txt` changes. Copies were removed; nothing was implemented or committed.

Limits: this is a retrospective comparison covering the five supplied cases. Quoting, interpolation, and malformed inputs remain outside scope per `requirements.md`.
