# Native Python request control

Adapt [controlled_fetch.py](../assets/controlled_fetch.py) only when equivalent
project support is absent. The copy needs no installed skill.

`await fetch.started(key)` checks actual entry/key and returns a unique handle,
even for repeated keys. Call `request.complete(payload)` or
`request.fail_request(error)` directly, without TestCase wrappers.

Tests own component assertions and bounded task cancellation/draining, including
after failed entry checks; the asset does neither. Do not shadow runner methods:
transport failure is `fail_request`, not `unittest.TestCase.fail`.

For new assertion plumbing, exercise an isolated deliberate mismatch. Confirm
actual/expected assertion evidence, not a support exception; green cases alone
cannot validate the failure path.
