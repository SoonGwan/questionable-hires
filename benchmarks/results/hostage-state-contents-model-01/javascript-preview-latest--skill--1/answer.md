I’ll use the hostage-negotiator skill to keep the fix focused, read the project requirements and existing tests, then add controlled regression coverage for request ownership through fetch and decode.

The loader currently writes every successful result to state and has no loading or error transitions. I’ve added a per-invocation token so only the newest request can update state, while every caller still receives its own result or failure. I’m adding overlap tests for both phases, including identical keys and stale completions against newer pending and settled states.

All 58 tests pass, including both unchanged original tests. The added tests cover both overlap phases, newer loading/ready/error states, exact payload and error identities, recovery, per-instance isolation, and callback rejection triggered by abort. Controlled callbacks are released and registered tasks drained on failure, with deadlines on waits.

Fixed `PreviewLoader` so only the newest invocation can update state during fetch or decode. Existing API, argument/result/error identities, and both original tests remain unchanged.

Added 56 native regression tests with bounded waits and callback cleanup covering the requested states, overlaps, failures, recovery, isolation, and actual abort rejection.

`node --test`: **58 passed, 0 failed**.
