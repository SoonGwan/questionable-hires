I’ll inspect the decoder tests, then use a disposable copy inside the repository to test one finalization fault without changing existing files.

The existing streaming assertion uses only ASCII. The UTF-8 autodetection case contains complete text and reads the response before iterating it. I’m testing whether either catches a one-flag mutation that prevents the text decoder from finalizing at EOF, alongside focused truncated and valid split-sequence cases.

Coverage is missing. Changing only `TextDecoder.flush()` from `decode(b"", True)` to `decode(b"", False)` leaves all 40 existing decoder tests passing.

Focused assertions exercised both `iter_text()` and `aiter_text()`:

| Case | Correct | Mutated |
|---|---|---|
| Incomplete UTF-8 at EOF: expects `"prefix �"` | Both pass | Both fail: returns `"prefix "` |
| Valid `€` split across chunks | Both pass | Both pass |

The existing streaming test checks ASCII; the UTF-8 autodetection test uses complete input read before iteration.

Original source and tests were verified unchanged. All runs used the specified interpreter. [Report, mutation, and logs](project/.decoder-finalization-audit/REPORT.md).
