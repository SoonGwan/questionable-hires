# Standalone controlled transport candidate

Prior [panel model evidence](results/mother-panel-01/README.md) retained custom
async TestCase.fail wrappers that broke intended assertion handling on faulty
code. Existing runner-method guidance remains. This candidate adds an optional
standalone [test-support asset](../skills/mother-in-law/assets/controlled_fetch.py)
for Python projects that do not already supply an adequate controlled transport.
Do not replace required support, change production, or copy assets where the
task only permits edits to existing tests. Earlier benchmark fixture inputs and
model results are unchanged.

Each awaited fetch publishes a Request with its own Future. `started(expected)`
checks the actual key with a bounded queue wait and returns that request handle.
`request.complete(payload)` and `request.fail_request(error)` act on the handle,
not on TestCase; repeated identical keys no longer need a key-indexed pending
dictionary or unique fake inputs. The model must still write actual component
state assertions and cancel/await its owned tasks in failure-safe cleanup. This
does not generate regression tests, guarantee UI correctness or supervise tasks.

Focused tests verify reversed completion of two identical keys with distinct
complete payloads, failure then recovery, actual/expected wrong-key AssertionError,
timeout and invalid bounds, cancellation without affecting a same-key sibling,
and refusal to complete cancelled/already-completed Futures. A subprocess test
copies only the asset into a path with spaces and runs using the standard library,
without an installed skill, checking cleanup of the owned task and no extra files.
All **6 focused tests pass (0.205s)**. No network, sleeps or dependencies are used.

This follows skill-creator's reusable-assets guidance and preserves native-project
delivery rather than introducing a runtime skill dependency. It adds optional
surface area and instruction bytes; real model adoption, net token/time savings
and avoiding assertion-wrapper collisions are **unmeasured**. Helper tests are
not a replacement for the all-eight developer-usefulness/performance objective.

Full suite before adding the final standalone subprocess test: **386 pass
(52.886s)**; the subsequent focused six-test run includes that new test.
Skill validation, catalog/local links, featured synchronization and whitespace
checks pass. The executable asset did not change during either test run.
