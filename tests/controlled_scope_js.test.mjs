import assert from 'node:assert/strict';
import test from 'node:test';
import { withControlledCalls } from '../skills/hostage-negotiator/assets/controlled_call.mjs';

test('scope preserves invocation timing, receiver, values and body result', async () => {
  const value = {}, result = {};
  assert.equal(await withControlledCalls(async ({ call, run, wait }) => {
    const owner = { save: call() };
    const task = run(() => owner.save(value));
    assert.equal(owner.save.calls.length, 1);
    const entry = await owner.save.started();
    assert.equal(entry.receiver, owner);
    assert.equal(entry.args[0], value);
    entry.complete(result);
    assert.equal(await wait(task), result);
    return value;
  }), value);
});

test('scope observes rejections promptly but preserves reasons for assertions', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const save = call(), reason = {};
    const task = run(() => save());
    (await save.started()).fail(reason);
    await new Promise(resolve => setImmediate(resolve));
    await assert.rejects(wait(task), error => error === reason);
    const sync = run(() => { throw reason; });
    await assert.rejects(wait(sync), error => error === reason);
  });
});

test('failed assertion releases existing and later entries, draining application finally', async () => {
  const expected = new Error('application assertion failed');
  let save, finished = false;
  await assert.rejects(withControlledCalls(async scope => {
    save = scope.call();
    scope.run(async () => {
      try { await save('first'); await save('later'); }
      finally { finished = true; }
    });
    await save.started();
    throw expected;
  }), error => error === expected);
  assert.equal(finished, true);
  assert.deepEqual(save.calls.map(entry => entry.args[0]), ['first', 'later']);
  assert.ok(save.calls.every(entry => entry.released));
});

test('missing release times out body then drains owned tasks', async () => {
  let finished = false;
  await assert.rejects(withControlledCalls(async ({ call, run, wait }) => {
    const save = call();
    const task = run(async () => { await save(); finished = true; });
    await wait(task);
  }, { timeoutMs: 15 }), /deadline exceeded/);
  assert.equal(finished, true);
});

test('uncontrolled never-settled task produces bounded cleanup failure', async () => {
  await assert.rejects(withControlledCalls(({ run }) => {
    run(() => new Promise(() => {}));
  }, { timeoutMs: 15 }), /deadline exceeded/);
});

test('scope closes long entry waits without keeping their timers or consuming future entries', async () => {
  let save, entryFailure;
  await assert.rejects(withControlledCalls(async ({ call }) => {
    save = call();
    try { await save.started(30000); }
    catch (error) { entryFailure = error; throw error; }
  }, { timeoutMs: 15 }), /deadline exceeded/);
  assert.match(entryFailure.message, /scope is closed/);
  assert.throws(() => save.started(), /scope is closed/);
  assert.equal(await save('late'), undefined);
  assert.deepEqual(save.calls[0].args, ['late']);
  assert.equal(save.calls[0].released, true);
});

test('body and cleanup failures are both retained, including non-Error reasons', async () => {
  await assert.rejects(withControlledCalls(({ run }) => {
    run(() => new Promise(() => {}));
    throw undefined;
  }, { timeoutMs: 15 }), error => {
    assert.ok(error instanceof AggregateError);
    assert.equal(error.errors[0], undefined);
    assert.match(error.errors[1].message, /deadline exceeded/);
    return true;
  });
});

test('released unresolved thenable is not falsely reported as drained', async () => {
  await assert.rejects(withControlledCalls(async ({ call, run }) => {
    const save = call();
    run(() => save());
    (await save.started()).complete(new Promise(() => {}));
  }, { timeoutMs: 15 }), /deadline exceeded/);
});

test('closed scope rejects new ownership and invalid deadline does not run body', async () => {
  let scope, invoked = false;
  await withControlledCalls(value => { scope = value; });
  assert.throws(() => scope.call(), /scope is closed/);
  assert.throws(() => scope.run(() => { invoked = true; }), /scope is closed/);
  for (const timeoutMs of [0, -1, Infinity, NaN, '5', null, 30001]) {
    await assert.rejects(withControlledCalls(() => { invoked = true; }, { timeoutMs }), RangeError);
  }
  assert.equal(invoked, false);
});

test('scope cleans up without replacing real owner assertions or masking faults', async () => {
  async function check(guard, cleanup) {
    let pending = false;
    async function submit(save) {
      if (guard && pending) return;
      pending = true;
      try { return await save(); }
      finally { if (cleanup) pending = false; }
    }
    await withControlledCalls(async ({ call, run, wait }) => {
      const save = call(), value = {};
      const first = run(() => submit(save));
      await save.started();
      assert.equal(pending, true);
      const duplicate = run(() => submit(save));
      assert.equal(save.calls.length, 1);
      assert.equal(await wait(duplicate), undefined);
      save.calls[0].complete(value);
      assert.equal(await wait(first), value);
      assert.equal(pending, false);
    });
  }
  await check(true, true);
  await assert.rejects(check(false, true), { code: 'ERR_ASSERTION', actual: 2, expected: 1 });
  await assert.rejects(check(true, false), { code: 'ERR_ASSERTION', actual: true, expected: false });
});

test('failed body drains a controlled async finally without replacing its error', async () => {
  const failure = new Error('body assertion failed');
  let operation, cleanup, finalized = false;
  await assert.rejects(withControlledCalls(async scope => {
    operation = scope.call();
    cleanup = scope.call();
    scope.run(async () => {
      try { await operation('work'); }
      finally {
        await cleanup('release resource');
        finalized = true;
      }
    });
    await operation.started();
    assert.equal(cleanup.calls.length, 0);
    throw failure;
  }), error => error === failure);
  assert.equal(finalized, true);
  assert.equal(operation.calls.length, 1);
  assert.equal(cleanup.calls.length, 1);
  assert.deepEqual(cleanup.calls[0].args, ['release resource']);
  assert.equal(cleanup.calls[0].released, true);
});

test('one failing scope does not release or close a concurrently active scope', async () => {
  let notifyReady, allowBody;
  const ready = new Promise(resolve => { notifyReady = resolve; });
  const proceed = new Promise(resolve => { allowBody = resolve; });
  const payload = {}, result = {};
  let siblingEntry, siblingTask, siblingFinished = false;
  const sibling = withControlledCalls(async scope => {
    const save = scope.call();
    siblingTask = scope.run(async () => {
      const value = await save(payload);
      siblingFinished = true;
      return value;
    });
    siblingEntry = await save.started();
    notifyReady();
    await proceed;
    assert.equal(await scope.wait(siblingTask), result);
  });
  // Observe rejection immediately even if an assertion below fails first.
  const observedSibling = sibling.then(() => null, error => error);
  try {
    await ready;
    const failure = new Error('other scope failed');
    await assert.rejects(withControlledCalls(async scope => {
      const save = scope.call();
      scope.run(() => save(payload));
      await save.started();
      throw failure;
    }), error => error === failure);
    assert.equal(siblingEntry.released, false);
    assert.equal(siblingEntry.args[0], payload);
    assert.equal(siblingFinished, false);
    siblingEntry.complete(result);
    allowBody();
    assert.equal(await observedSibling, null);
    assert.equal(siblingFinished, true);
  } finally {
    if (siblingEntry && !siblingEntry.released) siblingEntry.complete(result);
    allowBody();
    await observedSibling;
  }
});
