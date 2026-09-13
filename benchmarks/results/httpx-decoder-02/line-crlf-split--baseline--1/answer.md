I’ll inspect the line decoder and its tests, then run an isolated mutation to check whether an existing assertion catches lost CR carry-over across chunks. All temporary copies and diagnostics will stay inside this repository.

The third assertion in `test_line_decoder_crnl` explicitly covers CR and LF arriving in separate chunks. I’ll test its sensitivity by changing only the carried CR to LF in a disposable copy. That should introduce an extra empty line in the split case while preserving nearby unsplit CRLF behavior.

Yes—existing coverage detects the fault. The third assertion in [tests/test_decoders.py:339](project/tests/test_decoders.py#L339) checks:

```python
response = httpx.Response(200, content=[b"", b"a\r", b"\n\r\nb\r\nc"])
assert list(response.iter_lines()) == ["a", "", "b", "c"]
```

In an isolated copy, I changed only CR carry-over from `text = "\r" + text` to `text = "\n" + text`.

- **Correct:** all 40 decoder tests passed.
- **Mutated:** 39 passed; that assertion failed with `["a", "", "", "b", "c"]`.
- Nearby unsplit CRLF cases, with and without a final CRLF, retained their expected output under both versions. The Issue #1033 unsplit case also remained correct.

No additional test is needed for this fault. Original files were verified unchanged. Copies, mutation diff, and diagnostic logs are in `.crlf-audit/`. All Python/pytest commands used the specified interpreter.
