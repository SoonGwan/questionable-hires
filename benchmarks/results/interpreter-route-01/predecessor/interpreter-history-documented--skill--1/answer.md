I’m using the necromancer skill to trace the local history and test both implementations against the current contract. I’ll keep the review probes disposable and leave the original files and Git state unchanged.


The local fix commit replaced the child queue getter with an event wait so cancellation cannot consume an undelivered request. `requirements.md` still requires that behavior. I’ll now compare both versions with cancellation scheduled during request wakeup, and check separately that cancellation after delivery does not restore the consumed handle.


**Reject the proposed restoration.** On Python 3.11.6, it violates the pending-waiter cancellation contract in [requirements.md](project/requirements.md#L4).

The local history explains the change:

- `8a5070903a33eeeb4d755d6b93c701a3c32f61b6` introduced per-call `Request` handles and `started` using `await asyncio.wait_for(self.calls.get(), timeout)`.
- `cc6b5f9480b1906731ff94e6fa4b3993aeea50ed` introduced the event notification mechanism. Its diff replaces the consuming child queue getter with an availability wait, followed by synchronous dequeue. This protects undelivered requests while cancellation reaches the waiter.
- `92e340bbc8c74eada805987a80bc90c8d3b35899` documents provenance. These are **reconstructed local source snapshots, not complete original repository ancestry**. Both source hashes matched [source-origin.json](project/source-origin.json#L1); its upstream identifiers are provenance claims, not independently inspected history.

I inspected the complete implementation and loaded complete disposable modules, retaining their globals and normal compilation semantics. Only `started` changed in the proposal; structural comparison verified that every other module element remained identical, including the current constructor and `__call__`.

Observed assertions:

| Check | Current | Proposal |
|---|---|---|
| Ordinary request returns exact chosen object | Pass | Pass |
| Repeated keys: distinct handles and futures | Pass | Pass |
| Complete second request first; first remains pending | Pass | Pass |
| Cancel empty pending waiter | Cancelled; queue `0` | Cancelled; queue `0` |
| Cancel after handle delivery | Queue `0`; handle usable; application unaffected | Same |
| Cancel during request wakeup | **Cancelled; queue `1`** | **Not cancelled; queue `0`** |

For the wakeup check, both versions reached the same cancellation point: waiter pending, application pending, one queued request, and `cancel()` returning `True`. Current code propagated cancellation and allowed a subsequent `started` to retrieve the request. The proposal instead returned a `Request`, despite cancellation count `1`, swallowing the pending waiter’s cancellation. Both application tasks remained unaffected and ultimately returned the exact completion object.

This distinguishes cancellation **before delivery** from cancellation after an already-delivered handle: only the former must preserve the queued request.

Commands included:

```text
git log HEAD -- controlled_fetch.py requirements.md
git blame -L 24,60 -- controlled_fetch.py
git show cc6b5f9 -- controlled_fetch.py
git show 8a50709:controlled_fetch.py
python3 -B --version
python3 -B .review-0oexllta/probe.py current
python3 -B .review-0oexllta/probe.py proposal
```

Inspection command batches exited `0`. Individual probe processes exited **current: `0`**, **proposal: `1`**, with the proposal failing the cancellation-contract assertion. The outer `python3 -B` controller exited `0`.

Scheduling used `call_soon` and bounded cooperative turns—no sleeps or elapsed-time triggers. All child tasks were cleaned up. Scratch was removed, and before/after file hashes confirmed originals, license, skills, and Git HEAD/index unchanged.

Keep the current implementation. This establishes that its protective behavior remains required; it does not prove that this particular mechanism is the only possible solution.
