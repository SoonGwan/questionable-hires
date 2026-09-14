I’ll use the hostage-negotiator skill to keep the fix focused, read the project requirements, and add regression coverage while preserving the API and existing tests.

The loader currently publishes every completed decode and has no loading or error transitions. I’ll add a per-instance request token to guard state updates while preserving each caller’s result or failure, then test overlaps during both fetch and decode with controlled callbacks.

All 42 tests pass, including the two unchanged originals. The new tests cover stale completions and failures against newer pending, ready, and error states, plus actual signal-driven rejection. I’m checking the final diff and adding coverage for callbacks that synchronously start a newer request before throwing.

Fixed PreviewLoader with per-instance request tracking so only the newest request updates state. Preserved the API, exact result/error identities, and both original tests unchanged.

Added regression coverage for transitions, overlaps, identical keys, isolation, failures, recovery, and actual abort rejection, with bounded waits and cleanup.

`node --test`: **45 passed**, none skipped.
