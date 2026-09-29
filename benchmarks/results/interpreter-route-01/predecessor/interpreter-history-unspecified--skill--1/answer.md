I’m using the necromancer skill to trace the local history and compare both implementations against the requirements. I’ll keep the probes in disposable project-local scratch and leave the originals unchanged.


The local fix introduced the event to keep a child queue getter from consuming a request while cancellation reaches `started`. The current requirements explicitly preserve that behavior. I’ll test cancellation at that wakeup boundary and separately check cancellation after a handle has already been delivered.


**Reject the proposed restoration.** On Python 3.11.6, it swallowed cancellation of a pending `started` waiter and consumed the request. That violates [requirements.md:4](project/requirements.md#L4).

Local history establishes:

- `6b682e0f229176b1d6dc7d1c308909d0b17c219d` introduced the per-request transport with `await asyncio.wait_for(self.calls.get(), timeout)`.
- `5cb5d783822530cb2dac826e72e82ef669922fb3` introduced the event notification and synchronous dequeue in [controlled_fetch.py:35](project/controlled_fetch.py#L35). Its diff separates waiting for availability from consuming the request, preventing a child getter from consuming during cancellation.
- These are **reconstructed local source snapshots**, not complete original ancestry. [source-origin.json:14](project/source-origin.json#L14) states that limitation. Both historical source hashes matched its recorded snapshot hashes; no external ancestry was consulted.

I inspected the complete module and executed its actual `__call__`/`started` paths. The disposable proposal replaced exactly one `started` definition with the historical definition. All other source bytes, including the current constructor and `__call__`, remained intact. Full-module imports retained module bindings; AST checks confirmed the substitution.

Each probe used bounded cooperative scheduling: at most 40 turns driven by `call_soon`, with no sleeps or elapsed-time race setup. For cancellation, the waiter first registered its wait; the application entered `__call__`; cancellation was scheduled after the child’s wakeup but before `started` completed.

| Probe | Observations | Current exit | Proposal exit |
|---|---|---:|---:|
| Ordinary success | Exact response-object identity; queue empty | 0 | 0 |
| Repeated key | Distinct handles/futures; second completed first while first remained pending; both exact identities preserved | 0 | 0 |
| Cancellation during wakeup | Detailed below | 0 | **1** |
| Cancellation after delivery | Owner cancelled; queue remained empty; application remained pending; delivered handle still completed it with exact identity | 0 | 0 |

At wakeup cancellation:

- **Current:** `waiter_done=False`, queue size `1`; afterward `cancelled=True`, queue size `1`, application neither done nor cancelled. A subsequent `started` recovered the request and completed the application successfully.
- **Proposal:** `waiter_done=False`, queue size `0`; afterward `cancelled=False`, queue size `0`, application neither done nor cancelled. Assertion failed: **`pending waiter swallowed cancellation`**.

The proposal’s request was not already delivered when cancellation was requested. The separate post-delivery probe confirms that later cancellation correctly does **not** restore an already-delivered handle.

Commands included `git log HEAD -- controlled_fetch.py requirements.md`, `git blame -L 24,61 -- controlled_fetch.py`, and `git show` of both introducing snapshots and the fix. Probe commands were:

```text
python3.11 -B <scratch>/probe.py <scratch>/{current,proposal}.py <case>
```

Each combination’s individual exit is recorded above. The `python3 -B` orchestration exited `0`; the initial `python` lookup was unavailable.

Retain the current implementation. Its cancellation guarantees remain required, although another mechanism could satisfy them. Findings are verified on Python 3.11.6, not every supported interpreter.

Scratch was removed. Byte comparisons confirmed all originals—including license, skills, Git HEAD and index—unchanged. No harness or report was retained.
