# JavaScript controlled callbacks — local capability validation

Resource `8ca9e70`, 2026-09-14. Optional ES-module asset extends Hostage's callback
test support beyond Python; it is not a claim of improved model efficiency.
The existing Python asset and behavior remain unchanged. Routing selects only
the actual runtime's asset when equivalent project support is absent.

`controlledCall()` returns a Promise-returning function. `started(timeoutMs)`
observes actual entry; unique handles retain argument/receiver references and
allow explicit success/failure in any order. Repeat arguments do not merge calls.
Timed-out entry waiters are removed, so they cannot consume future calls.
Releasing a call twice fails explicitly; normal Promise thenable resolution
remains intact. The copied module has no repository or installed-skill dependency.

Native Node v24.16.0: seven tests pass, covering identity, repeated calls/reversed
completion, failure isolation, FIFO/expired waiters, invalid deadlines, thenable
resolution and separate application-owner controls. The owner is an authored
local Form fixture, not an organic application or browser. Its valid path passes;
missing guard yields native actual 2/expected 1, missing cleanup true/false.
These intentional assertion failures are verified as failures, not support errors.

Python integration checks run the Node suite under a 15-second process deadline
and verify an unchanged standalone copy under a 10-second deadline: two tests
pass in 0.128s. Fifteen installer tests pass in 1.691s. If Node is absent, the
native integration tests explicitly skip; that is not JavaScript validation.

Limits: the helper does not assert application state, automatically cancel
Promises, intercept AbortSignal, bound application waits or drain owned work.
Tests must handle rejections promptly, settle unreleased calls and drain tasks;
use application cancellation contracts and process bounds where needed. Timers
cannot interrupt blocking JS. `released` means completion was requested, not
that an assimilated thenable has settled. No rendering/network/production proof.

Next evidence needed: actual model delivery in a JavaScript project, retained
native regressions including error/retry and cancellation when contracted, and
a matched baseline comparison. Do not reuse Python benchmark numbers to claim
JavaScript adoption, speedup, browser coverage or TypeScript integration.
