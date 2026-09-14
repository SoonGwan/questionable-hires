import assert from 'node:assert/strict';
import test from 'node:test';
import { controlledCall } from '../skills/hostage-negotiator/assets/controlled_call.mjs';

test('records actual arguments/receiver and preserves object identity', async () => {
  const save = controlledCall();
  const receiver = { save }, payload = {}, result = {};
  const task = receiver.save(payload, 3);
  const call = await save.started();
  assert.equal(call.receiver, receiver);
  assert.equal(call.args[0], payload);
  assert.equal(call.args[1], 3);
  assert.equal(call.released, false);
  call.complete(result);
  assert.equal(await task, result);
  assert.equal(call.released, true);
  assert.throws(() => call.complete(), /already released/);
  assert.throws(() => call.fail(new Error()), /already released/);
});

test('identical arguments retain distinct handles and reverse completion', async () => {
  const save = controlledCall(), payload = {};
  const first = save(payload), second = save(payload);
  const a = await save.started(), b = await save.started();
  assert.notEqual(a, b);
  assert.deepEqual(save.calls, [a, b]);
  b.complete('second');
  assert.equal(await second, 'second');
  assert.equal(a.released, false);
  a.complete('first');
  assert.equal(await first, 'first');
});

test('failure preserves reason identity without affecting sibling', async () => {
  const save = controlledCall(), error = new Error('write failed');
  const failed = save(), sibling = save();
  const rejection = assert.rejects(failed, reason => reason === error);
  const a = await save.started(), b = await save.started();
  a.fail(error);
  await rejection;
  b.complete();
  assert.equal(await sibling, undefined);
});

test('waiters are FIFO and a timed-out waiter cannot consume later entry', async () => {
  const save = controlledCall();
  await assert.rejects(save.started(5), /Timed out/);
  const firstEntry = save.started(), secondEntry = save.started();
  const a = save('a'), b = save('b');
  const first = await firstEntry, second = await secondEntry;
  assert.deepEqual(first.args, ['a']);
  assert.deepEqual(second.args, ['b']);
  first.complete(); second.complete();
  await Promise.all([a, b]);
});

test('invalid deadlines fail before consuming an existing entry', async () => {
  const save = controlledCall(), task = save();
  for (const timeout of [0, -1, Infinity, NaN, '5', null, 30001]) {
    assert.throws(() => save.started(timeout), RangeError);
  }
  (await save.started()).complete();
  await task;
});

test('ordinary Promise thenable resolution is not advertised as cancellation', async () => {
  const save = controlledCall(), result = {};
  const task = save();
  (await save.started()).complete(Promise.resolve(result));
  assert.equal(await task, result);
});

// A separate application owner: helper does not implement pending/duplicates.
class Form {
  pending = false;
  constructor(guard = true, cleanup = true) { this.guard = guard; this.cleanup = cleanup; }
  async submit(save) {
    if (this.guard && this.pending) return;
    this.pending = true;
    try { return await save(); }
    finally { if (this.cleanup) this.pending = false; }
  }
}

async function verifyForm(form) {
  const save = controlledCall(), result = {};
  const task = form.submit(save);
  const tasks = [task];
  try {
    await save.started();
    assert.equal(form.pending, true);
    const duplicate = form.submit(save);
    tasks.push(duplicate);
    // submit invokes the callback synchronously up to its first await.
    assert.equal(save.calls.length, 1, 'duplicate must not invoke save');
    assert.equal(await duplicate, undefined);
    save.calls[0].complete(result);
    assert.equal(await task, result);
    assert.equal(form.pending, false, 'pending must clear after success');
  } finally {
    for (const call of save.calls) if (!call.released) call.complete();
    await Promise.allSettled(tasks);
  }
}

test('real owner check accepts valid and rejects missing guard/cleanup', async () => {
  await verifyForm(new Form());
  await assert.rejects(verifyForm(new Form(false)), { code: 'ERR_ASSERTION', actual: 2, expected: 1 });
  await assert.rejects(verifyForm(new Form(true, false)), { code: 'ERR_ASSERTION', actual: true, expected: false });
});
