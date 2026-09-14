/**
 * Copy into permitted JavaScript test support when no equivalent exists.
 * No dependencies or application implementation; uses ordinary ES modules.
 *
 * const save = controlledCall();
 * const task = form.submit(save); // register rejection handling/cleanup now
 * const call = await save.started(1000); // actual entry, timeout in milliseconds
 * call.complete(result); // or call.fail(error); then await the application task
 *
 * Each call has unique identity even for identical args. args and receiver keep
 * references, not snapshots. save.calls records all entries. released means a
 * completion/failure was requested; Promise resolution still assimilates thenables.
 * Releasing twice throws. Test synchronous invocation errors with a normal
 * throwing function, not this Promise-returning double.
 *
 * Tests own application assertions, bounded application waits and cleanup:
 * handle rejected tasks promptly, release every unreleased call, then drain tasks.
 * A started timeout removes only that waiter; it does NOT cancel application
 * work. Promises have no implicit cancellation. Use the application's AbortSignal
 * path when testing cancellation. Timers cannot interrupt blocking JS; use runner
 * process deadlines where needed. No browser/network/rendering evidence is supplied.
 */
export function controlledCall() {
  const calls = [];
  const entries = [];
  const waiters = [];

  function callback(...args) {
    let resolve, reject;
    const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
    let released = false;
    function release(action, value) {
      if (released) throw new Error('Controlled call already released');
      released = true;
      action(value);
    }
    const call = {
      args, receiver: this,
      get released() { return released; },
      complete(value) { release(resolve, value); },
      fail(error) { release(reject, error); },
    };
    calls.push(call);
    const waiter = waiters.shift();
    if (waiter) {
      clearTimeout(waiter.timer);
      waiter.resolve(call);
    } else {
      entries.push(call);
    }
    return promise;
  }

  callback.calls = calls;
  callback.started = (timeoutMs = 1000) => {
    if (!Number.isFinite(timeoutMs) || timeoutMs <= 0 || timeoutMs > 30000) {
      throw new RangeError('timeoutMs must be in (0, 30000]');
    }
    if (entries.length) return Promise.resolve(entries.shift());
    return new Promise((resolve, reject) => {
      const waiter = { resolve, timer: undefined };
      waiter.timer = setTimeout(() => {
        waiters.splice(waiters.indexOf(waiter), 1);
        reject(new Error('Timed out waiting for callback entry'));
      }, timeoutMs);
      waiters.push(waiter);
    });
  };
  return callback;
}
