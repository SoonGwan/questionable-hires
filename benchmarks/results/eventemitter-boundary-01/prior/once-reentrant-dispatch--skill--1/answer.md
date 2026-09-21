I’ll use the hostage-negotiator skill to keep the fix focused, inspect the dispatch code and existing tests, then add and run native regressions.

The outer dispatch retains listener objects that a nested emit has already invoked. I’ll track consumption on each once registration and remove that specific registration, so duplicate callbacks remain independent and ordinary listener snapshots keep working.

All 25 tests pass. The regressions cover recursive dispatch through both listener paths, caught and propagated throws, duplicate registrations, re-registration, and snapshot behavior. I’m checking the final diff and confirming the supplied tests and license are unchanged.

Fixed `index.js` to consume each once registration before invocation, preventing repeat calls across recursive dispatches and throws while preserving duplicate registrations and listener snapshots.

Added 24 native regressions. `node --test *.test.cjs`: **25 passed, 0 failed**.

Existing tests and license are unchanged. No commits or publication.
