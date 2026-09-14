I’ll use the hostage-negotiator skill to keep the fix focused and add controlled regression tests while preserving the API and existing tests.



The fix gives each load call its own identity and uses it to guard state updates. Every call still runs its callbacks and returns its own result or error. I’m adding tests for both overlap phases, newer pending and settled states, and signal-driven rejection.



Fixed PreviewLoader so only the newest request can update state, while preserving callback arguments, results, errors, and the existing API.

Both original tests remain unchanged. Added 41 regression tests covering transitions, overlaps, identities, isolation, failures, recovery, and actual abort rejection, with bounded waits and cleanup.

`node --test`: all 43 tests pass.
