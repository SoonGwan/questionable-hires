I’ll inspect the CRLF coverage, then run an isolated mutation in a disposable copy inside the repository. I’ll leave the original source and tests unchanged.

The existing test detects the fault: its split-CRLF assertion gets an extra empty line. The correct copy passes all 40 tests; the mutated copy fails only `test_line_decoder_crnl`. I’ll check the nearby unsplit cases separately, including the one after the failing assertion, and verify that the original files are unchanged.

Yes—existing coverage protects split CRLF. No additional test is needed.

The detecting assertion is in [tests/test_decoders.py:339](project/tests/test_decoders.py#L339):

```python
response = httpx.Response(200, content=[b"", b"a\r", b"\n\r\nb\r\nc"])
assert list(response.iter_lines()) == ["a", "", "b", "c"]
```

One isolated mutation changed the carried-over CR into LF: `text = "\r" + text` → `text = "\n" + text`.

- Correct copy: **40 passed**.
- Mutated copy: **39 passed, 1 failed**, at that assertion; actual output was `["a", "", "", "b", "c"]`.
- All three nearby unsplit CRLF cases produced identical correct results in both copies.

Used only the specified interpreter. Original files were verified unchanged; copies, mutation diff, and diagnostic logs remain in `.crlf-audit/`.
