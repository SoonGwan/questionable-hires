I’ll use the receipt skill to capture the five-test suite’s failures before editing, fix `Decoder.feed`, then rerun the unchanged suite and review the focused diff.

The baseline ran all five tests: three passed and two failed. Both partial-payload tests returned `[]` instead of the expected messages because `feed` removed the header before the full payload arrived. I’ll retain the header until the entire frame is available.

Fixed `packet.py`: `Decoder.feed` now retains the header and partial payload until the complete frame arrives. Public API preserved.

Ran `python3 -B -m unittest discover -s tests -v` before and after:

- **Before:** 3 passed, 2 failed. Partial-payload cases returned `[]` instead of `[b'hello']` and `[b'world', b'last']`.
- **After:** all 5 unchanged tests passed.

Reviewed the focused diff; only `packet.py` changed. Tests and requirements remain unchanged. `git diff --check` passed.
