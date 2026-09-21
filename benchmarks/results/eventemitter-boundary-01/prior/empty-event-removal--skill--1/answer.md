I’ll use the hostage-negotiator skill to keep the fix focused, preserve the existing tests and license, and verify the event-removal behavior with native regression tests.

The regression tests reproduced the bug: removing `''` clears unrelated string and symbol events, even when `''` is absent. I’ll change the condition to check explicitly for `undefined`, preserving the existing clear-all behavior for omitted arguments.

Fixed `removeAllListeners` in `index.js` to treat `''` as a specific event. Omitted arguments and `undefined` still clear all events.

Added six regression tests covering preservation of other events, absent-event no-ops, fluent returns, counts, and reuse.

`node --test *.test.cjs`: all 7 tests passed. Existing tests and license unchanged. No commits or publication.
