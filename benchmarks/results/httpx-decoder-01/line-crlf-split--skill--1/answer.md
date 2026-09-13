I’ll use the con-artist skill to trace the CRLF assertions, run a baseline, and test one isolated CR carry-over mutation without changing existing files.

The baseline passes all 40 tests. `test_line_decoder_crnl` already checks a CRLF split between chunks, alongside two unsplit cases. I’ll disable trailing-CR deferral in the disposable copy to see whether that assertion catches the extra blank line it should produce.

Existing coverage **detects the split-CRLF fault**. No additional test is needed for this mutation.

In a disposable project-local copy, I disabled trailing-CR deferral in `LineDecoder.decode`, causing CR and the next chunk’s LF to be processed separately.

- **Baseline:** 40 passed; exit 0.
- **Mutant:** 39 passed, 1 failed; exit 1.
- **Detecting assertion:** [tests/test_decoders.py:339](project/tests/test_decoders.py#L339), using chunks `[b"", b"a\r", b"\n\r\nb\r\nc"]`. Expected `["a", "", "b", "c"]`; mutant returned `["a", "", "", "b", "c"]`.
- The preceding unsplit CRLF assertions, with and without a final CRLF, passed under both implementations.

Both runs used:
```sh
/tmp/qh-httpx-preflight.3Slnqw/venv/bin/python -B -m pytest -p no:cacheprovider -p audit_imports -q -s tests/test_decoders.py
```

The audit plugin verified copied imports and the actual `Response.iter_lines` decoder binding within pytest. All 130 pre-existing non-git files remained unchanged; disposable artifacts were removed.
