I’m using the con-artist skill to trace the CRLF assertions and run one isolated mutation, leaving the original files unchanged.

The existing CRLF test includes the split `[b"a\r", b"\n\r\nb\r\nc"]` and asserts the exact lines. I’ll mutate the carried CR into LF; that should introduce an extra blank line at the split while leaving unsplit CRLF behavior intact.

Existing coverage detects the split-CRLF fault. No additional test is needed for this mutation.

- **Mutation:** In `LineDecoder.decode`, change carried CR from `text = "\r" + text` to `text = "\n" + text`.
- **Execution:** Used the specified interpreter and audit helper to run `pytest -q tests/test_decoders.py` in isolated project-local copies. Correct: **40 passed**, exit 0. Mutant: **39 passed, 1 failed**, exit 1.
- **Detecting assertion:** [tests/test_decoders.py:339](project/tests/test_decoders.py#L339) expects `["a", "", "b", "c"]` for chunks `[b"", b"a\r", b"\n\r\nb\r\nc"]`. The mutant produces `["a", "", "", "b", "c"]`.
- **Nearby unsplit CRLF:** Both preceding assertions, with and without a final CRLF, pass under the mutant.

The tests exercise `Response.iter_lines()` through the real decoder; copied implementation imports were verified in each test process. Original bytes and permissions remained unchanged, and disposable copies were removed.
