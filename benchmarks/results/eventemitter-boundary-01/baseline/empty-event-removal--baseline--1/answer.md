I’ll check the implementation and existing tests, fix the empty-string handling, and add and run native regression tests.

Fixed `removeAllListeners` to check `event !== undefined`. Empty-string events now remove only their own listeners; absent empty events are a no-op. No argument and `undefined` still clear everything.

Added native regression tests for string/symbol preservation, fluent returns, and event/listener consistency. All 6 tests pass with `node --test *.test.cjs`.

Existing tests and license remain unchanged. No commits or publication.
