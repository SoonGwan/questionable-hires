I’ll use the hostage-negotiator skill to keep the fix focused, preserve the existing tests and license, and verify the behavior with native regression tests.

The regression tests reproduced the bug: removing `''` clears unrelated string and symbol events, even when `''` is absent. I’ll change the condition to check for `undefined` explicitly.

Fixed `removeAllListeners` to treat `''` as a specific event. Absent empty events are a no-op; no argument or `undefined` still clears all events.

Added seven regression tests covering event preservation, fluent returns, and listener consistency. `node --test *.test.cjs`: **8 passed**.

Existing tests and license remain unchanged. No commits or publication.
