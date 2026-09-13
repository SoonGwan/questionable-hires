I’ll use the con-artist skill to trace the finalization checks, run one isolated mutation, and verify a focused assertion if coverage is missing. All existing files will stay unchanged.

The streaming test covers only ASCII. The UTF-8 autodetection case uses a complete sequence and reads the body before iterating text. I’ll change only the decoder’s EOF flag from `True` to `False`, then check for a missing replacement character at EOF and confirm that a valid character split across chunks still decodes correctly.

Coverage is missing: `tests/test_decoders.py` survived the EOF fault.

The isolated mutation changed `TextDecoder.flush()` from `decode(b"", True)` to `decode(b"", False)`, suppressing finalization of buffered UTF-8 bytes.

Using the prescribed interpreter and audit helper with pytest:

| Check | Correct | Mutated |
|---|---:|---:|
| `tests/test_decoders.py` | 40 passed | 40 passed |
| Focused assertions | 6 passed | 3 passed, 3 failed |

The focused checks covered synchronous streaming and asynchronous streaming on asyncio and Trio. All incomplete-EOF checks failed because the mutant returned `"A"` instead of `"A\ufffd"`. Valid split-sequence controls passed in both versions.

Proposed focused assertion, verified in disposable copies:

```python
@pytest.mark.parametrize("chunks, expected", [
    ((b"A\xe2", b"\x82"), "A\ufffd"),
    ((b"A\xe2", b"\x82\xac"), "A\u20ac"),
])
def test_utf8_stream_finalization(chunks, expected):
    response = httpx.Response(200, content=iter(chunks))
    assert "".join(response.iter_text()) == expected
```

Existing streaming coverage uses ASCII; the autodetection test reads a complete UTF-8 body before iterating text. Neither detects this fault.

Copied imports and actual caller bindings were verified. Disposable copies were removed; original source and tests remained unchanged.
