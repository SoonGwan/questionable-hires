I’ll inspect the decoder tests and CR carry-over logic, then run one isolated mutation in a disposable project directory without changing existing files.

The third assertion in `test_line_decoder_crnl` explicitly covers a split CRLF. I’ll test its sensitivity by changing only the copied decoder’s carried CR to LF; that should produce an extra blank line when the next chunk starts with LF, while preserving unsplit CRLF behavior.

Yes—existing coverage detects this fault. The assertion at [tests/test_decoders.py:339](project/tests/test_decoders.py#L339) tests:

```python
response = httpx.Response(200, content=[b"", b"a\r", b"\n\r\nb\r\nc"])
assert list(response.iter_lines()) == ["a", "", "b", "c"]
```

In an isolated copy, I changed only CR carry-over from `text = "\r" + text` to `text = "\n" + text`. This prevents the carried CR from combining with the next LF.

- Correct copy: **40 passed**.
- Mutated copy: **39 passed, 1 failed**, at that assertion; output was `["a", "", "", "b", "c"]`.
- Nearby unsplit CRLF cases, with and without a final CRLF, retained correct output in both copies. The unsplit Issue #1033 case also remained correct.

No additional test is needed for this fault. All commands used the specified interpreter; original files were hash-verified unchanged. Copies, mutation diff, and logs are in [crlf-audit-7bnacrgg](commands.json).
