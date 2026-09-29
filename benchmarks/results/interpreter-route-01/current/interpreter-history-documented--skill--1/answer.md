I’m using the necromancer skill to trace the local history and contract, then test both versions through the real request path in disposable project-local copies. I’ll leave the originals and Git state unchanged.


The local fix replaced a queue-consuming child task with an availability notification. That matters because the contract requires cancellation to reach a pending waiter without consuming its request. The checkout uses Python 3.11.6; I’ll test cancellation during wakeup separately from cancellation after a handle has already been delivered.


Reject the proposed restoration: it violates the pending-waiter cancellation requirement on the documented interpreter, Python 3.11.6.

Local history establishes the purpose:

- `8a50709` introduced per-request handles and the earlier `wait_for(self.calls.get(), timeout)` implementation.
- `cc6b5f9` introduced the event notification and synchronous dequeue in [controlled_fetch.py:35](project/controlled_fetch.py#L35), specifically to preserve requests during waiter cancellation.
- [requirements.md:4](project/requirements.md#L4) still requires cancellation to reach a pending waiter without consuming an undelivered request or cancelling its application task.

These are **reconstructed local snapshot commits**, not complete original repository ancestry, as [source-origin.json](project/source-origin.json) explicitly records. Both source SHA256 values matched its snapshot metadata. Original upstream ancestry was not inspected.

I loaded complete disposable modules, retaining their module bindings. Only `started` changed in the proposal; its AST matched the historical method, and all other source—including the current constructor and `__call__`—remained unchanged.

Observed assertions:

| Check | Current | Proposal |
|---|---|---|
| Ordinary request returns exact completed object | Pass | Pass |
| Repeated keys have independent handles/futures | Pass | Pass |
| Second request completed first; first remained pending; both returned exact objects | Pass | Pass |
| Cancellation after handle delivery leaves queue empty and handle usable | Pass | Pass |
| Cancellation during pending request wakeup propagates and preserves request | Pass | **Fail** |

The deterministic wakeup check queued the actual application call followed by a cancellation callback. At cancellation, both versions had `waiter.done() == False`, queue size `1`, and `cancel() == True`.

- **Current:** waiter cancelled, queue size `1`; a subsequent `started` recovered the request.
- **Proposal:** waiter **not cancelled**, queue size `0`; it returned `Request(key='race')`, swallowing cancellation.
- Both application tasks remained pending and subsequently returned the exact completed object.

This differs from cancellation **after delivery**, which correctly leaves the handle consumed. Scheduling used `call_soon` and at most 64 cooperative checkpoints per wait, without wall-clock delays.

Commands and individual exits, relative to the project:

```text
python3 -B .necromancer-review-wmr_1icp/probe.py current   → 0
python3 -B .necromancer-review-wmr_1icp/probe.py proposal  → 1
python3 -B -   # setup, subprocess execution, cleanup    → 0
```

History evidence came from `git log HEAD -- …`, `git blame -L 1,240 -- controlled_fetch.py`, and `git show` of the cited commits.

Keep the current implementation. Its cancellation behavior remains required; another mechanism could satisfy that contract, but this proposal does not. Scratch was removed, and file inventory/hash checks confirmed originals, license, skills, Git HEAD and index unchanged. No harness or report was retained.
