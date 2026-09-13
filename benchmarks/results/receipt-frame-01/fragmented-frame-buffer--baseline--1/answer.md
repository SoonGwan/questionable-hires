I’ll read the requirements and decoder, run the five-test suite before editing, then fix the header handling and review the focused diff.

The baseline ran all five tests: three passed and two failed. Both failures returned `[]` instead of the completed payloads: `[b'hello']` and `[b'world', b'last']`. The decoder deletes the header before checking whether the payload is complete; I’ll move that deletion after the completeness check.

Fixed `Decoder.feed` to retain the header until the entire payload is available, preserving the public API.

Ran `python3 -B -m unittest discover -s tests -v` before and after:

- **Before:** 3 passed, 2 failed. `test_partial_payload_with_empty_feed` returned `[]` instead of `[b'hello']`; `test_complete_then_partial_then_multiple` returned `[]` instead of `[b'world', b'last']`.
- **After:** all 5 passed.

Reviewed the focused diff: only `packet.py` changed, moving header deletion after the completeness check. Tests and requirements remain unchanged. `git diff --check` passed.
