Buffer accepts opaque item objects; order and item identity matter.
queued is the tuple of waiting items; its backing container identity is private.
add appends synchronously, including while a flush is awaiting send.
flush on an idle nonempty buffer detaches exactly its current queued items and
invokes the supplied send once with a tuple containing those exact objects.
busy is True during that operation. While busy, another flush returns literal
False immediately without invoking its send or changing any buffer state.
An idle empty flush also returns literal False without invoking send.
Successful send returns its exact receipt object (including None or False).
That batch stays removed; items added while waiting remain queued in order.
On synchronous send failure, async failure or application-task cancellation,
restore the detached batch BEFORE all items added meanwhile, without loss or
duplication, then propagate the failure. Ordinary exception identity is preserved;
task cancellation requires CancelledError propagation, not exception identity.
After either outcome busy is False and a new flush can proceed. Instances are
independent. Internal counters/container identities are not public contracts.
Callbacks are cooperative asyncio operations, no I/O/threads. No automatic retry,
background flushing, item copying, deferred execution of suppressed calls or
cancellation of another flush.
