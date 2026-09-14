# Controlled Python callback tests

For asyncio callback-based behavior without equivalent project test support,
copy [controlled_call.py](../assets/controlled_call.py) into an allowed test-support
location. Use the real application owner and runner; do not create another app
implementation. No installed skill is needed to rerun the copied support.

`save = ControlledCall()` is an async callback accepting positional/keyword
arguments, including none. Start the actual application coroutine using your
test's owned-task cleanup. `call = await save.started(timeout=1)` waits for its
actual callback entry. Then assert the application's pending state/other required
behavior. `call.args`/`call.kwargs` record argument references, not deep snapshots;
`save.calls` lists all entries, even identical arguments, for call-count checks.

`call.complete(value)` returns that exact object; `call.fail(error)` raises that
exact exception when awaited. Await the application task with a bound and assert
its state/result/error. Each call has its own future: sibling completions and
cancellations remain separate. Completing a finished/cancelled handle raises
`asyncio.InvalidStateError`; do not silently hide accidental double completion.

This controls the callback only. Assert duplicate suppression, instance isolation,
cleanup and recovery through actual application behavior when required. A recorded
entry is not proof of those properties. Cancellation must target the application
task, not just its response future. Synchronous failure while calling a callback
needs an ordinary raising function, not this async double.

Register cancellation and draining of owned tasks before waiting for entry; a
failed entry wait does not clean them. Bound application waits too. Async timeouts
cannot interrupt blocking code or guarantee termination of cancellation-resistant
tasks; use a process-level bound when needed. This is not network, thread, browser,
transaction or production evidence. Keep existing project fixtures when suitable.
