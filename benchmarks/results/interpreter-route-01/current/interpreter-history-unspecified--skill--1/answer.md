I’ll use the necromancer skill to trace the local history and contract, then compare both implementations with bounded behavioral probes in disposable project-local copies.

The local fix replaced a child queue getter with an availability notification to protect requests during waiter cancellation. That behavior is explicitly required by requirements.md. I’ll test cancellation during wakeup separately from cancellation after a handle has already been delivered.

**Reject the proposed restoration.** On Python 3.11.6, it swallowed cancellation of a pending `started` waiter, violating [requirements.md:4](project/requirements.md#L4). Keep the current implementation; another mechanism could be acceptable if it preserves the required behavior.

Local history establishes:

- `6b682e0f229176b1d6dc7d1c308909d0b17c219d` introduced the earlier `await asyncio.wait_for(self.calls.get(), timeout)` implementation.
- `5cb5d783822530cb2dac826e72e82ef669922fb3` introduced the event notification, cancellation cleanup, and synchronous dequeue now in [controlled_fetch.py:35](project/controlled_fetch.py#L35). Its diff explains the purpose: avoid a child queue getter consuming a request during waiter cancellation.
- These are **reconstructed local source snapshots**, not complete original repository ancestry. Their SHA-256 values matched both snapshots recorded in [source-origin.json](project/source-origin.json#L2). No external history was consulted.

I inspected the complete implementation and imported complete disposable modules, retaining their module bindings. Only `started` changed in the proposal copy: its AST matched the historical method, and all surrounding source bytes—including the current constructor and `__call__`—remained unchanged.

Each behavioral case ran in its own Python process:

| Case | Observed assertions | Current exit | Proposal exit |
|---|---|---:|---:|
| Ordinary request | Correct key; application returns the exact completed object; queue empty | 0 | 0 |
| Repeated keys, reversed completion | Distinct handles and futures; second returns its object while first remains pending; first subsequently returns its object | 0 | 0 |
| Cancellation during wakeup | Detailed below | 0 | **1** |
| Cancellation after delivery | Owner cancelled; handle remains consumed; completing it still returns the exact object to the application | 0 | 0 |

For deterministic wakeup cancellation, I first established that `started` was waiting. The application then enqueued its request; a queued cancellation callback ran while the waiter was still pending and before its child wakeup completed. Progress used `call_soon` and bounds of 64 cooperative turns, with no sleeps or wall-clock delays.

Observed values:

| Value | Current | Proposal |
|---|---|---|
| `cancel()` accepted | `True` | `True` |
| Waiter cancelled | `True` | **`False`** |
| Queue size | `1` | `0` |
| Application pending / cancelled | `True / False` | `True / False` |
| Waiter returned a handle | `False` | **`True`** |

Current code additionally passed recovery through a subsequent `started` and exact-object completion. The proposal failed `assert cancelled`: cancellation was swallowed. **This observation is not a cancelled waiter losing a handle**—the proposal returned one despite cancellation. The separate already-delivered-handle case passed for both implementations.

Commands used included:

```text
git log --format=fuller --stat HEAD -- controlled_fetch.py requirements.md source-origin.json
git blame -L 24,60 -- controlled_fetch.py
git show 5cb5d783822530cb2dac826e72e82ef669922fb3 -- controlled_fetch.py
git show 6b682e0f229176b1d6dc7d1c308909d0b17c219d:controlled_fetch.py
/opt/homebrew/bin/python3 -B - <<'PY' …
```

The coordinator executed eight commands in this form, one for each table cell:

```text
/opt/homebrew/opt/python@3.11/bin/python3.11 -B <scratch>/probe.py <scratch>/<current|proposal>.py <case>
```

History commands and the coordinator exited `0`; individual probe exits are preserved above. Scratch was project-local and removed in `finally`. File hashes confirmed all originals, LICENSE, Git HEAD/index, and skill resources unchanged. No harness or report files remain.
