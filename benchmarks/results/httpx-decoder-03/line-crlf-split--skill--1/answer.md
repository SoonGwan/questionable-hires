I’ll use the con-artist skill to trace the CRLF assertions and run one isolated carry-over mutation, leaving the original source and tests untouched.

The existing test explicitly splits `\r\n` between chunks at lines 338–339. I’ll disable the trailing-CR deferral in a disposable copy so that CR is processed immediately; this should produce an extra empty line at the split. The two unsplit CRLF assertions run before that assertion, providing nearby controls.

Existing coverage **detects the split-CRLF fault**. No additional test is needed for this mutation.

I removed only the trailing-CR deferral block in a disposable copy of `httpx/_decoders.py`, making CR terminate the line immediately. Using the specified interpreter and audit helper with pytest arguments `-q tests/test_decoders.py`:

- Correct code: **40 passed**, exit 0.
- Mutant: **39 passed, 1 failed**, exit 1.
- Detecting assertion: `tests/test_decoders.py:339`, in `test_line_decoder_crnl`. Chunks `[b"", b"a\r", b"\n\r\nb\r\nc"]` produced `["a", "", "", "b", "c"]` instead of `["a", "", "b", "c"]`.
- Both preceding unsplit CRLF assertions, with and without a final CRLF, passed under the mutation.

`Response.iter_lines()` calls the real `LineDecoder`; both implementation modules were verified as copied imports inside each test process. Disposable copies were removed, and original source, tests, and configuration remained unchanged.
