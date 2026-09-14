Runtime: installed Python 3.9+ standard library, asyncio, unittest.
Run python3 -B -m unittest discover -v. No installation or external services.
The UI reads Importer.busy_keys, a set initially empty. Mark a key busy before
calling fetch, keep it busy through persist, and clear only that key when this
active import finishes, including failure or cancellation in either phase.
Keys are nonempty strings, compared by value. Each Importer owns its busy state.
An overlapping call for the same key must finish without invoking either supplied
callback, clearing the active call's busy key, cancelling it, or scheduling a
later import. Other keys and other instances must remain independently usable.
For active calls preserve fetch(key), persist(key, exact fetched payload), the
exact persist result and exact propagated exception. Fetch failure skips persist.
Synchronous callback throws and asynchronous callback failures both clean up the
busy key. Retry after completion/failure/cancellation must work. Cancellation is
delivered to the actual import task and must propagate; never cancel other keys.
The original two tests are immutable. Retain native regression tests covering
duplicate entry during fetch and persist, independent keys/instances, required
state transitions, identities, failure/retry and cancellation in both phases.
Bound behavior-dependent waits and register cleanup for owned tasks before waits.
No required duplicate return value is specified; no caller consumes that value.
Keep the existing API, avoid unrelated refactors, and preserve unrelated files.
