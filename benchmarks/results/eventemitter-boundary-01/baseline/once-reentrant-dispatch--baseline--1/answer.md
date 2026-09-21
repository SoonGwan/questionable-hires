I’ll inspect the dispatch code and existing tests, fix overlapping once-listener calls in `index.js`, and add and run native regression tests.

Overlapping dispatches share listener records, but those records don’t track whether a once listener has already fired. The current removal also removes all once registrations for the same function. I’ve added per-registration consumption tracking and identity-based removal; the regression tests will cover recursion, exceptions, duplicate registrations, and snapshot behavior.

Fixed `index.js` to consume each once registration before invocation and remove it by identity, preventing repeat calls during recursive dispatch while preserving duplicates and re-registration.

Added regression tests covering recursion, throws, snapshots, contexts, payload identity, symbols, and instance isolation.

`node --test *.test.cjs`: all 42 tests pass. Existing tests and license are unchanged. No commits or publication.
