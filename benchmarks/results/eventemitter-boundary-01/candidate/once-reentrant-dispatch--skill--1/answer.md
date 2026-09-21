I’ll use the hostage-negotiator skill to keep the fix focused, add native regression tests, and verify the dispatch behavior.



The outer dispatch retains listener objects after a nested dispatch consumes them. I’ll track consumption on each registration and remove only that registration, so duplicate callbacks stay independent.

The tests will cover both dispatch paths, nested exceptions, re-registration, and ordinary listener snapshots.



Fixed `index.js` to consume once registrations before invocation and remove them by identity, preventing repeat calls across recursive dispatches and exceptions while preserving duplicates and snapshots.

Added 24 regression tests. `node --test *.test.cjs`: **25 passed, 0 failed**.

Existing tests and license unchanged. No commits or publication.
