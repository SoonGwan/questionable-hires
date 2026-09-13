I’ll inspect the decoder tests, then use a disposable copy to test one narrow finalization mutation without changing existing files.

The tests cover ASCII streaming and complete multibyte text, but I found no incomplete UTF-8 sequence at end of stream. I’ll change only the finalization flag in the disposable copy, then check whether the existing suite detects it and whether a focused assertion does.

Coverage is missing: `tests/test_decoders.py` passes all 40 tests with both correct and faulty behavior.

The isolated mutation changes `TextDecoder.flush()` from `decode(b"", True)` to `decode(b"", False)`, preventing end-of-stream finalization.

Focused checks exercised synchronous streaming and asynchronous streaming under asyncio and trio:

| Input chunks | Correct | Faulty |
|---|---|---|
| `b"prefix \xe2"`, `b"\x82"` | Emits `"prefix �"` | Loses trailing replacement character; assertion fails |
| Same chunks plus `b"\xac"` | Emits `"prefix €"` | Passes normal control |

All six focused checks passed against correct behavior. Against the mutation, the three incomplete-sequence checks failed and all three controls passed.

[Assertions and diagnostic artifacts](project/.decoder-finalization-audit/test_utf8_finalization.py) are in `.decoder-finalization-audit/`. All commands used the specified interpreter; integrity checks confirmed existing repository files were unchanged.
