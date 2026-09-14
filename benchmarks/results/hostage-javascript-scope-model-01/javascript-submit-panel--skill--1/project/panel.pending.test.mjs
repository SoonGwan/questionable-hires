import assert from 'node:assert/strict';
import test from 'node:test';
import { SubmitPanel } from './panel.mjs';
import { withControlledCalls } from './test-support/controlled_call.mjs';

async function successfulRetry(panel, { call, run, wait }) {
  assert.equal(panel.pending, false);
  const save = call(), result = {};
  const task = run(() => panel.submit(save));
  const entry = await save.started();
  assert.equal(panel.pending, true);
  entry.complete(result);
  assert.equal(await wait(task), result);
  assert.equal(panel.pending, false);
  assert.equal(save.calls.length, 1);
}

test('pending brackets save, suppresses duplicates promptly, and permits reuse', async () => {
  await withControlledCalls(async scope => {
    const { call, run, wait } = scope;
    const panel = new SubmitPanel();
    const signal = new AbortController().signal, result = {};
    const save = call(), duplicate = call();
    assert.equal(panel.pending, false);
    const task = run(() => panel.submit(received => {
      assert.equal(panel.pending, true);
      return save(received);
    }, signal));
    assert.equal(panel.pending, true);
    const entry = await save.started();
    assert.equal(entry.args[0], signal);

    const overlap = run(() => panel.submit(duplicate, signal));
    assert.equal(await wait(overlap), undefined);
    assert.equal(duplicate.calls.length, 0);
    assert.equal(entry.released, false);
    assert.equal(panel.pending, true);
    entry.complete(result);
    assert.equal(await wait(task), result);
    assert.equal(panel.pending, false);
    assert.equal(save.calls.length, 1);
    assert.equal(duplicate.calls.length, 0);
    await successfulRetry(panel, scope);
  });
});

test('separate instances save concurrently and clear pending independently', async () => {
  await withControlledCalls(async ({ call, run, wait }) => {
    const first = new SubmitPanel(), second = new SubmitPanel();
    const saveFirst = call(), saveSecond = call();
    const firstResult = {}, secondResult = {};
    assert.equal(first.pending, false);
    assert.equal(second.pending, false);
    const firstTask = run(() => first.submit(saveFirst));
    const firstEntry = await saveFirst.started();
    const secondTask = run(() => second.submit(saveSecond));
    const secondEntry = await saveSecond.started();
    assert.equal(first.pending, true);
    assert.equal(second.pending, true);
    secondEntry.complete(secondResult);
    assert.equal(await wait(secondTask), secondResult);
    assert.equal(second.pending, false);
    assert.equal(first.pending, true);
    firstEntry.complete(firstResult);
    assert.equal(await wait(firstTask), firstResult);
    assert.equal(first.pending, false);
  });
});

test('asynchronous failure preserves its reason, clears pending, and permits retry', async () => {
  await withControlledCalls(async scope => {
    const { call, run, wait } = scope;
    const panel = new SubmitPanel(), save = call();
    const error = new Error('asynchronous save failure');
    const task = run(() => panel.submit(save));
    const entry = await save.started();
    assert.equal(panel.pending, true);
    entry.fail(error);
    await assert.rejects(wait(task), reason => reason === error);
    await successfulRetry(panel, scope);
  });
});

test('synchronous invocation failure preserves its reason and permits retry', async () => {
  await withControlledCalls(async scope => {
    const { run, wait } = scope;
    const panel = new SubmitPanel(), signal = new AbortController().signal;
    const error = new Error('synchronous save failure');
    let calls = 0;
    // Do not let run() conceal a change from a rejected Promise to a sync throw.
    let task;
    assert.doesNotThrow(() => {
      task = panel.submit(received => {
        calls++;
        assert.equal(panel.pending, true);
        assert.equal(received, signal);
        throw error;
      }, signal);
      run(() => task);
    });
    await assert.rejects(wait(task), reason => reason === error);
    assert.equal(calls, 1);
    await successfulRetry(panel, scope);
  });
});

test('callback rejection on abort preserves reason, clears pending, and permits retry', async () => {
  const controller = new AbortController();
  let onAbort;
  try {
    await withControlledCalls(async scope => {
      const { call, run, wait } = scope;
      const panel = new SubmitPanel(), save = call();
      const reason = new Error('caller cancelled save');
      const task = run(() => panel.submit(signal => {
        assert.equal(signal, controller.signal);
        assert.equal(panel.pending, true);
        const result = save(signal);
        const entry = save.calls.at(-1);
        onAbort = () => { if (!entry.released) entry.fail(signal.reason); };
        signal.addEventListener('abort', onAbort, { once: true });
        return result;
      }, controller.signal));
      const entry = await save.started();
      assert.equal(controller.signal.aborted, false);
      assert.equal(panel.pending, true);
      controller.abort(reason);
      await assert.rejects(wait(task), error => error === reason);
      assert.equal(entry.released, true);
      assert.equal(controller.signal.reason, reason);
      await successfulRetry(panel, scope);
    });
  } finally {
    if (onAbort) controller.signal.removeEventListener('abort', onAbort);
  }
});
