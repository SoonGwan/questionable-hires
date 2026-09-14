import assert from 'node:assert/strict';
import test from 'node:test';
import { SubmitPanel } from './panel.mjs';
import { withControlledCalls } from './test-support/controlled_call.mjs';

test('pending surrounds save, suppresses duplicates, and preserves identities', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const panel = new SubmitPanel();
    const signal = new AbortController().signal;
    const result = {};
    const save = call();
    assert.equal(panel.pending, false);
    const task = run(() => panel.submit(received => {
      assert.equal(panel.pending, true);
      return save(received);
    }, signal));
    const entry = await save.started(1000);
    assert.equal(entry.args[0], signal);
    assert.equal(panel.pending, true);

    const duplicate = call();
    assert.equal(await wait(run(() => panel.submit(duplicate, signal))), undefined);
    assert.equal(duplicate.calls.length, 0);
    assert.equal(save.calls.length, 1);
    assert.equal(panel.pending, true);

    entry.complete(result);
    assert.equal(await wait(task), result);
    assert.equal(panel.pending, false);
  });
});

test('different panel instances can save concurrently and settle independently', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const first = new SubmitPanel();
    const second = new SubmitPanel();
    const saveFirst = call();
    const saveSecond = call();
    const firstTask = run(() => first.submit(saveFirst));
    const firstEntry = await saveFirst.started(1000);
    const secondTask = run(() => second.submit(saveSecond));
    const secondEntry = await saveSecond.started(1000);
    assert.equal(first.pending, true);
    assert.equal(second.pending, true);

    const secondResult = {};
    secondEntry.complete(secondResult);
    assert.equal(await wait(secondTask), secondResult);
    assert.equal(second.pending, false);
    assert.equal(first.pending, true);

    const firstResult = {};
    firstEntry.complete(firstResult);
    assert.equal(await wait(firstTask), firstResult);
    assert.equal(first.pending, false);
  });
});

test('asynchronous failure preserves the error and allows a successful retry', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const panel = new SubmitPanel();
    const save = call();
    const task = run(() => panel.submit(save));
    const entry = await save.started(1000);
    assert.equal(panel.pending, true);
    const error = new Error('asynchronous save failure');
    entry.fail(error);
    await assert.rejects(wait(task), reason => reason === error);
    assert.equal(panel.pending, false);

    const retry = run(() => panel.submit(save));
    const retryEntry = await save.started(1000);
    assert.equal(panel.pending, true);
    assert.equal(save.calls.length, 2);
    const result = {};
    retryEntry.complete(result);
    assert.equal(await wait(retry), result);
    assert.equal(panel.pending, false);
  });
});

test('synchronous callback throws remain promise rejections and allow retry', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const panel = new SubmitPanel();
    const error = new Error('synchronous save failure');
    let task;
    assert.doesNotThrow(() => {
      task = panel.submit(() => {
        assert.equal(panel.pending, true);
        throw error;
      });
    });
    const observed = run(() => task);
    await assert.rejects(wait(observed), reason => reason === error);
    assert.equal(panel.pending, false);

    const save = call();
    const retry = run(() => panel.submit(save));
    const entry = await save.started(1000);
    assert.equal(panel.pending, true);
    const result = {};
    entry.complete(result);
    assert.equal(await wait(retry), result);
    assert.equal(panel.pending, false);
  });
});

test('callback rejection on abort preserves the reason, clears pending, and allows retry', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const panel = new SubmitPanel();
    const controller = new AbortController();
    const save = call();
    let removeListener = () => {};
    try {
      const task = run(() => panel.submit(signal => {
        assert.equal(signal, controller.signal);
        assert.equal(panel.pending, true);
        const promise = save(signal);
        const entry = save.calls.at(-1);
        const onAbort = () => entry.fail(signal.reason);
        signal.addEventListener('abort', onAbort, { once: true });
        removeListener = () => signal.removeEventListener('abort', onAbort);
        return promise;
      }, controller.signal));
      await save.started(1000);
      assert.equal(controller.signal.aborted, false);
      assert.equal(panel.pending, true);
      const reason = new Error('caller cancelled');
      controller.abort(reason);
      await assert.rejects(wait(task), error => error === reason);
      assert.equal(panel.pending, false);

      const retrySignal = new AbortController().signal;
      const retry = run(() => panel.submit(save, retrySignal));
      const entry = await save.started(1000);
      assert.equal(entry.args[0], retrySignal);
      assert.equal(panel.pending, true);
      const result = {};
      entry.complete(result);
      assert.equal(await wait(retry), result);
      assert.equal(panel.pending, false);
    } finally {
      removeListener();
    }
  });
});
