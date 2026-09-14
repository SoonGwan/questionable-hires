import assert from 'node:assert/strict';
import test from 'node:test';
import { SubmitPanel } from './panel.mjs';
import { controlledCall } from './test-support/controlled_call.mjs';

const deadlineMs = 1000;

async function bounded(promise) {
  let timer;
  try {
    return await Promise.race([
      promise,
      new Promise((_, reject) => {
        timer = setTimeout(() => reject(new Error('Timed out waiting for submission')), deadlineMs);
      }),
    ]);
  } finally {
    clearTimeout(timer);
  }
}

// Observe rejection immediately. Cleanup also releases callbacks entered while
// draining (for example, if a broken implementation queues a duplicate).
function scenario(t) {
  const saves = [], tasks = [];
  let cleaning = false;
  t.after(async () => {
    cleaning = true;
    for (const save of saves) {
      for (const call of save.calls) {
        if (!call.released) call.complete(undefined);
      }
    }
    await bounded(Promise.all(tasks));
  });
  return {
    save() {
      const controlled = controlledCall();
      saves.push(controlled);
      const save = (...args) => {
        const promise = controlled(...args);
        if (cleaning) controlled.calls.at(-1).complete(undefined);
        return promise;
      };
      save.calls = controlled.calls;
      save.started = () => controlled.started(deadlineMs);
      return save;
    },
    submit(panel, save, signal) {
      const outcome = panel.submit(save, signal).then(
        value => ({ status: 'fulfilled', value }),
        reason => ({ status: 'rejected', reason }),
      );
      tasks.push(outcome);
      return outcome;
    },
  };
}

async function fulfilled(task, value) {
  const outcome = await bounded(task);
  assert.equal(outcome.status, 'fulfilled');
  assert.equal(outcome.value, value);
}

async function rejected(task, reason) {
  const outcome = await bounded(task);
  assert.equal(outcome.status, 'rejected');
  assert.equal(outcome.reason, reason);
}

test('pending surrounds save, preserves identities, and suppresses overlapping submissions', async t => {
  const s = scenario(t), panel = new SubmitPanel();
  const save = s.save(), duplicate = s.save();
  const signal = new AbortController().signal, result = {};
  assert.equal(panel.pending, false);
  let pendingAtEntry;
  const task = s.submit(panel, received => {
    pendingAtEntry = panel.pending;
    return save(received);
  }, signal);
  assert.equal(panel.pending, true);
  const call = await save.started();
  assert.equal(pendingAtEntry, true);
  assert.equal(call.args[0], signal);
  await fulfilled(s.submit(panel, duplicate, signal), undefined);
  assert.equal(duplicate.calls.length, 0);
  assert.equal(save.calls.length, 1);
  assert.equal(panel.pending, true);
  call.complete(result);
  await fulfilled(task, result);
  assert.equal(panel.pending, false);
  assert.equal(duplicate.calls.length, 0);
});

test('separate instances can save concurrently and finish independently', async t => {
  const s = scenario(t), first = new SubmitPanel(), second = new SubmitPanel();
  const saveFirst = s.save(), saveSecond = s.save();
  const firstResult = {}, secondResult = {};
  const firstTask = s.submit(first, saveFirst);
  const secondTask = s.submit(second, saveSecond);
  const firstCall = await saveFirst.started();
  const secondCall = await saveSecond.started();
  assert.equal(first.pending, true);
  assert.equal(second.pending, true);
  secondCall.complete(secondResult);
  await fulfilled(secondTask, secondResult);
  assert.equal(second.pending, false);
  assert.equal(first.pending, true);
  firstCall.complete(firstResult);
  await fulfilled(firstTask, firstResult);
  assert.equal(first.pending, false);
});

test('asynchronous failure preserves error identity and allows retry', async t => {
  const s = scenario(t), panel = new SubmitPanel(), save = s.save();
  const error = new Error('asynchronous failure'), result = {};
  const task = s.submit(panel, save);
  const call = await save.started();
  assert.equal(panel.pending, true);
  call.fail(error);
  await rejected(task, error);
  assert.equal(panel.pending, false);
  const retry = s.submit(panel, save);
  const retryCall = await save.started();
  assert.equal(panel.pending, true);
  retryCall.complete(result);
  await fulfilled(retry, result);
  assert.equal(panel.pending, false);
  assert.equal(save.calls.length, 2);
});

test('synchronous invocation failure preserves error identity and allows retry', async t => {
  const s = scenario(t), panel = new SubmitPanel(), save = s.save();
  const error = new Error('synchronous failure'), result = {};
  let pendingAtEntry;
  const task = s.submit(panel, () => {
    pendingAtEntry = panel.pending;
    throw error;
  });
  await rejected(task, error);
  assert.equal(pendingAtEntry, true);
  assert.equal(panel.pending, false);
  const retry = s.submit(panel, save);
  const call = await save.started();
  assert.equal(panel.pending, true);
  call.complete(result);
  await fulfilled(retry, result);
  assert.equal(panel.pending, false);
});

test('abort-triggered callback rejection clears pending and allows retry', async t => {
  const s = scenario(t), panel = new SubmitPanel(), save = s.save();
  const controller = new AbortController(), reason = new Error('cancel save');
  let removeListener = () => {};
  try {
    const task = s.submit(panel, signal => {
      const promise = save(signal);
      const call = save.calls.at(-1);
      const onAbort = () => { if (!call.released) call.fail(signal.reason); };
      signal.addEventListener('abort', onAbort, { once: true });
      removeListener = () => signal.removeEventListener('abort', onAbort);
      return promise;
    }, controller.signal);
    const call = await save.started();
    assert.equal(call.args[0], controller.signal);
    assert.equal(controller.signal.aborted, false);
    assert.equal(panel.pending, true);
    controller.abort(reason);
    await rejected(task, reason);
    assert.equal(panel.pending, false);
    const retrySignal = new AbortController().signal, result = {};
    const retry = s.submit(panel, save, retrySignal);
    const retryCall = await save.started();
    assert.equal(retryCall.args[0], retrySignal);
    assert.equal(panel.pending, true);
    retryCall.complete(result);
    await fulfilled(retry, result);
    assert.equal(panel.pending, false);
  } finally {
    removeListener();
  }
});
