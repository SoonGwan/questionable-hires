# Git physical-line integrity — 2026-09-14

Local runtime correction against parent `c7683ca`; not a model benchmark or a
token/time saving. Historical experiments and featured charts are unchanged.

## Reproduction and correction

The collector used Python `splitlines()` for current source, blame and numbered
patch parsing, plus universal-newline decoding. Git counts LF-delimited rows.
Embedded separators therefore silently shifted current excerpts and truncated
blame text; CR content could also be rewritten before parsing.

`tests/test_history_helper.py` adds a real committed Git fixture matrix: nine
embedded separators (VT, FF, FS, GS, RS, NEL, Unicode LS/PS and CR), each with LF,
CRLF or absent final newline. Before correction, all 27 subcases fail with
actual/expected source mismatches (24 test methods, 27 failures).

The runtime now explicitly decodes UTF-8 bytes without newline translation and
uses LF-only splitting in all three paths, discarding only the empty terminal
split item. The matrix verifies exact current/blame text and current numbering,
successful numbered excerpts from native Git patches, unchanged source bytes,
and rejection of a nonexistent third line. Existing read-only, shallow-history,
configuration, patch-budget and malformed-patch tests remain in the suite.

After correction: 24 history-helper tests pass in 7.667s, including all 27
subcases. This establishes source integrity for the exercised inputs, not model
adoption, general task success or efficiency. No new model sessions were run.

Full regression suite: 481 tests passed in 68.185s with no failures/skips.
Skill validation, repository link/metadata validation and featured bilingual
synchronization checks also pass.
