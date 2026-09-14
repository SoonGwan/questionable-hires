I’ll use the hostage-negotiator skill to keep the fix focused, read the project requirements and existing tests, and add controlled regression tests around the actual PreviewLoader class.

PreviewLoader currently writes every success to state and has no loading or error transitions. I’ll add a per-instance request token to guard state updates while preserving every caller’s fetch, decode, result, and error. The regression tests will cover both overlap phases and use bounded waits with cleanup that releases and drains pending callbacks.

Fixed PreviewLoader so only the latest request per instance updates state, preserving the API and exact callback/result/error identities.

Added 52 controlled regression tests covering transitions, overlaps, identical keys, recovery, isolation, and actual abort rejection, with bounded waits and cleanup. Both existing tests remain unchanged.

`node --test`: all 54 tests passed.
