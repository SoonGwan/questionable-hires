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
 *
 * Optional lifecycle ownership (same file, no test-runner dependency):
 * await withControlledCalls(async ({ call, run, wait }) => {
 *   const save = call();
 *   const task = run(() => form.submit(save)); // invokes now; observes rejection
 *   const entry = await save.started();
 *   // Assert application state/arguments here, then release the chosen entry.
 *   entry.complete(result);
 *   assert.equal(await wait(task), result);
 * });
 * The body and final drain each have a timeoutMs deadline (default 1000ms).
 * Exit rejects outstanding entry waits, releases unreleased owned calls,
 * including entries during drain, and drains registered tasks. Test-owned
 * listeners/resources still need finally.
 * Cleanup ignores task rejection reasons: assert expected outcomes in the body.
 * Body failures survive cleanup; if both fail, AggregateError contains both.
 * Deadlines do not cancel JS/application work or force-settle adopted thenables.
 */
export function controlledCall() {
  return createControlledCall().callback;
}

function createControlledCall() {
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
      const waiter = { resolve, reject, timer: undefined };
      waiter.timer = setTimeout(() => {
        waiters.splice(waiters.indexOf(waiter), 1);
        reject(new Error('Timed out waiting for callback entry'));
      }, timeoutMs);
      waiters.push(waiter);
    });
  };
  return {
    callback,
    closeEntries() {
      for (const waiter of waiters.splice(0)) {
        clearTimeout(waiter.timer);
        waiter.reject(new Error('Controlled-call scope is closed'));
      }
    },
  };
}

export async function withControlledCalls(body, { timeoutMs = 1000 } = {}) {
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0 || timeoutMs > 30000) {
    throw new RangeError('timeoutMs must be in (0, 30000]');
  }
  const owned = [], tasks = [];
  let closing = false;
  const requireOpen = () => {
    if (closing) throw new Error('Controlled-call scope is closed');
  };
  async function wait(task) {
    let timer;
    try {
      return await Promise.race([
        task,
        new Promise((_, reject) => {
          timer = setTimeout(() => reject(new Error('Controlled-call deadline exceeded')), timeoutMs);
        }),
      ]);
    } finally { clearTimeout(timer); }
  }
  const scope = {
    wait,
    call() {
      requireOpen();
      const { callback: controlled, closeEntries } = createControlledCall();
      function callback(...args) {
        const task = controlled.apply(this, args);
        if (closing) controlled.calls.at(-1).complete();
        return task;
      }
      callback.calls = controlled.calls;
      callback.started = (...args) => { requireOpen(); return controlled.started(...args); };
      owned.push({ callback, closeEntries });
      return callback;
    },
    run(operation) {
      requireOpen();
      let task;
      try { task = Promise.resolve(operation()); }
      catch (error) { task = Promise.reject(error); }
      // Observe immediately without converting the returned task into success.
      tasks.push(task.then(() => undefined, () => undefined));
      return task;
    },
  };
  let result, failure, failed = false;
  try { result = await wait(body(scope)); }
  catch (error) { failure = error; failed = true; }
  closing = true;
  try {
    for (const { callback, closeEntries } of owned) {
      closeEntries();
      for (const entry of callback.calls) if (!entry.released) entry.complete();
    }
    await wait(Promise.all(tasks));
  } catch (cleanupError) {
    if (failed) throw new AggregateError([failure, cleanupError], 'Body and controlled-call cleanup failed');
    throw cleanupError;
  }
  if (failed) throw failure;
  return result;
}
