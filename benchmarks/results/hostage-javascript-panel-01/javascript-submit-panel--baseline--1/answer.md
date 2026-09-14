I’ll read the requirements and existing tests, implement `pending`, and add native regression tests for the requested concurrency and cleanup behavior.

The API is small: `submit(save, signal)` returns the callback’s result or error. I’ll add an instance-level guard and clear it in `finally`. The new tests will use controlled promises, bounded waits, and cleanup that settles callbacks even if an assertion fails; the two existing tests will stay unchanged.

Implemented `SubmitPanel.pending` with duplicate suppression per instance and cleanup after success or failure, preserving the existing API.

Added five rerunnable native regression tests covering the requested states, concurrency, identities, retries, and abort cleanup. Waits are bounded, rejections handled promptly, and owned callbacks settled during cleanup.

`node --test`: all 7 tests pass. Both existing tests remain unchanged.
