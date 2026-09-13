I’ll use the con-artist skill to trace the finalization checks and run one isolated mutation, keeping the original source and tests unchanged.

The streaming check uses only ASCII. The UTF-8 autodetection test reads and combines the bytes before iterating text, and its sequence is complete. I’ll mutate `TextDecoder.flush()` to omit finalization, then check whether the suite notices the lost replacement character at an incomplete UTF-8 ending.

Coverage is missing: all 40 tests in `tests/test_decoders.py` pass with UTF-8 finalization broken.

The isolated mutation changed `TextDecoder.flush()` from `decode(b"", True)` to `decode(b"", False)`. This silently drops an incomplete trailing sequence. Existing streaming assertions use ASCII or complete text; the UTF-8 autodetection test reads the response before streaming.

Using the specified interpreter and the audit helper with pytest:

| Check | Correct | Mutated |
|---|---:|---:|
| `tests/test_decoders.py` | 40 passed, exit 0 | 40 passed, exit 0 |
| Focused assertions | 8 passed, exit 0 | 4 passed, 4 failed, exit 1 |

The focused assertions exercised `iter_text()` and `aiter_text()` under asyncio and Trio, checking exact joined output:

```python
# Incomplete at EOF: must emit a replacement character.
data = (b"ok \xe2", b"\x82")
expected = "ok \ufffd"

# Normal control: valid character split across chunks.
data = (b"ok \xe2", b"\x82\xac")
expected = "ok \u20ac"

assert actual == expected
```

Every incomplete-ending case failed on the mutant with `'ok ' != 'ok �'`; every valid control passed.

Copied imports and the actual caller’s decoder binding were verified. Original files remained unchanged, and disposable copies were removed.
