import assert from 'node:assert/strict';
import test from 'node:test';
import { controlledCall, withControlledCalls } from '../skills/hostage-negotiator/assets/controlled_call.mjs';

test('early settlement preserves fulfilled values and arbitrary rejection reasons', async () => {
  for (const value of [{}, undefined, null]) {
    for (const rejected of [false, true]) {
      const callback = controlledCall();
      const task = rejected ? Promise.reject(value) : Promise.resolve(value);
      await assert.rejects(callback.startedBefore(task, 30000), error => {
        assert.equal(error.code, 'ERR_CALLBACK_NOT_ENTERED');
        assert.equal(error.outcome.status, rejected ? 'rejected' : 'fulfilled');
        assert.equal(error.outcome[rejected ? 'reason' : 'value'], value);
        return true;
      });
      // A removed waiter must not consume the next real entry.
      const later = callback('later');
      const entry = await callback.started();
      assert.deepEqual(entry.args, ['later']);
      entry.complete(value);
      assert.equal(await later, value);
    }
  }
});

test('queued and future entries win without hiding task rejection', async () => {
  for (const queued of [true, false]) {
    const callback = controlledCall(), reason = {};
    let task;
    if (queued) task = callback();
    else task = Promise.resolve().then(() => callback());
    const entry = await callback.startedBefore(task);
    entry.fail(reason);
    await assert.rejects(task, error => error === reason);
  }
  const callback = controlledCall(), value = {};
  const pending = callback();
  const entry = await callback.startedBefore(Promise.reject(value));
  entry.complete();
  await pending;
  await new Promise(resolve => setImmediate(resolve));
});

test('settlement removes only its own waiter and retains FIFO entry order', async () => {
  const callback = controlledCall();
  const first = callback.started(1000);
  await assert.rejects(callback.startedBefore(Promise.resolve(), 1000),
                       { code: 'ERR_CALLBACK_NOT_ENTERED' });
  const task = callback('first');
  const entry = await first;
  assert.equal(entry.args[0], 'first');
  entry.complete();
  await task;
});

test('pending task keeps an entry deadline and does not steal later calls', async () => {
  const callback = controlledCall();
  await assert.rejects(callback.startedBefore(new Promise(() => {}), 5), /Timed out/);
  const task = callback();
  (await callback.started()).complete();
  await task;
  for (const timeout of [0, -1, NaN, Infinity, '1', 30001]) {
    assert.throws(() => callback.startedBefore(Promise.resolve(), timeout), RangeError);
  }
});

test('scope closure cancels the entry waiter while preserving owned cleanup', async () => {
  let callback, failure;
  await assert.rejects(withControlledCalls(async scope => {
    callback = scope.call();
    try { await callback.startedBefore(new Promise(() => {}), 30000); }
    catch (error) { failure = error; throw error; }
  }, { timeoutMs: 10 }), /deadline exceeded/);
  assert.match(failure.message, /scope is closed/);
  assert.throws(() => callback.startedBefore(Promise.resolve()), /scope is closed/);
});

test('two-stage application detects omitted entry without a deadline failure', async () => {
  async function check(skip) {
    return withControlledCalls(async scope => {
      const fetch = scope.call(), decode = scope.call(), bytes = {}, value = {};
      const task = scope.run(async () => {
        const received = await fetch();
        if (skip) return received;
        return decode(received);
      });
      (await fetch.startedBefore(task)).complete(bytes);
      const entry = await decode.startedBefore(task);
      assert.equal(entry.args[0], bytes);
      entry.complete(value);
      assert.equal(await scope.wait(task), value);
      return bytes;
    });
  }
  await check(false);
  await assert.rejects(check(true), error => {
    assert.equal(error.code, 'ERR_CALLBACK_NOT_ENTERED');
    assert.equal(error.outcome.status, 'fulfilled');
    assert.equal(typeof error.outcome.value, 'object');
    return true;
  });
});
