# Native Python request control

Adapt [controlled_fetch.py](../assets/controlled_fetch.py) only when equivalent
project support is absent. The copy needs no installed skill.

`await fetch.started(key)` checks actual entry/key and returns a unique handle,
even for repeated keys. Call `request.complete(payload)` or
`request.fail_request(error)` directly, without TestCase wrappers.
Cancelling or timing out the entry wait leaves unconsumed requests and application
tasks untouched; a later waiter can observe the pending request. A returned handle
is already consumed. These are cooperative same-loop waits, not process deadlines.

Tests own component assertions and bounded task cancellation/draining, including
after failed entry checks; the asset does neither. Do not shadow runner methods:
transport failure is `fail_request`, not `unittest.TestCase.fail`.

For custom assertion plumbing you introduce, exercise an isolated deliberate
mismatch and confirm actual/expected evidence, not a support exception. Ordinary
unmodified framework assertions do not need a separate test of the assertion
library. Add repeated-key cases when identity/reuse is relevant to the contract or
implementation, not merely because the transport supports them. Keep all distinct
required state transitions, including intervening retention checkpoints.
