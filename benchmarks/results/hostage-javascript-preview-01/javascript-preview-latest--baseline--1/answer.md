I’ll read the loader, requirements, and existing tests, then fix request ownership and add native regression coverage.

The loader now tracks each invocation separately and allows only the newest one to update state. All 32 tests pass so far, including overlaps during fetch and decode, identical keys, failure recovery, and callback rejection on abort. I’m checking the remaining identity assertions and cancellation behavior before the final run.

Fixed `PreviewLoader` so only the latest invocation can update state, while every caller retains its own result or error.

Preserved the API and both original tests unchanged. Added 31 native regression tests with controlled callbacks, bounded waits, prompt rejection handling, and cleanup.

Validation: `node --test` passes all 33 tests; `git diff --check` passes.
