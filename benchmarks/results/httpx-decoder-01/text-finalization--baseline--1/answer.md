I’ll inspect the decoder tests, then run a narrow mutation in a disposable project copy using the specified interpreter. Original files will remain untouched.

The streaming text test covers only ASCII. The UTF-8 autodetection case contains complete characters and reads the response before iterating text. I’ll change only `TextDecoder.flush()`’s finalization flag in the disposable copy and check whether the existing tests catch the lost trailing replacement character.

Coverage is missing: `tests/test_decoders.py` passed all **40 tests on both correct and faulty behavior**.

The isolated mutation changed only `TextDecoder.flush()` from `decode(b"", True)` to `decode(b"", False)`, preventing finalization.

Focused assertions exercised unread synchronous and asynchronous streams:

| Input chunks | Correct behavior | Faulty behavior |
|---|---|---|
| `b"prefix:\xe2"`, `b"\x82"` — incomplete at EOF | `["prefix:", "�"]` | `["prefix:"]` |
| `b"prefix:\xe2"`, `b"\x82\xac"` — valid split `€` | `["prefix:", "€"]` | Same |

The focused tests passed **6/6** against correct behavior. Against the mutation, all **3 incomplete-sequence checks failed**, while all **3 valid controls passed** (sync, asyncio, trio).

Existing streaming coverage uses ASCII; the UTF-8 autodetection case contains complete characters and reads the response first.

[Assertions, mutation, and logs](commands.json) are retained locally. All Python/pytest commands used the specified interpreter. Hash verification confirmed existing repository files were unchanged.
