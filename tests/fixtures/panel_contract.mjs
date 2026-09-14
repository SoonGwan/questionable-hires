// Author-only contract probe, never copied into the model-visible fixture.
import assert from 'node:assert/strict';
import { SubmitPanel } from './panel.mjs';

async function bounded(promise) {
  let timer;
  try {
    return await Promise.race([promise, new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error('contract wait timed out')), 1000);
    })]);
  } finally { clearTimeout(timer); }
}

const panel = new SubmitPanel(), sibling = new SubmitPanel();
const controller = new AbortController(), signal = controller.signal;
const result = {}, calls = [], tasks = [];
let finish;
const held = new Promise(resolve => { finish = resolve; });
try {
  assert.equal(panel.pending, false, 'initial pending');
  const task = panel.submit(received => {
    assert.equal(received, signal, 'signal identity');
    assert.equal(panel.pending, true, 'pending before callback');
    calls.push(received);
    return held;
  }, signal);
  tasks.push(task);
  // Register handling before any later check can fail.
  task.catch(() => {});
  assert.equal(panel.pending, true, 'pending while held');
  const duplicate = panel.submit(() => { calls.push('duplicate'); return result; });
  tasks.push(duplicate);
  duplicate.catch(() => {});
  assert.equal(await bounded(duplicate), undefined, 'duplicate return');
  assert.equal(calls.length, 1, 'duplicate callback count');
  assert.equal(await bounded(sibling.submit(async () => result)), result);
  assert.equal(sibling.pending, false);
  assert.equal(panel.pending, true, 'independent instance');
  finish(result);
  assert.equal(await bounded(task), result);
  assert.equal(panel.pending, false, 'success cleanup');
  for (const synchronous of [true, false]) {
    const error = new Error('expected save error');
    const fail = synchronous ? () => { throw error; } : async () => { throw error; };
    await assert.rejects(bounded(panel.submit(fail)), reason => reason === error);
    assert.equal(panel.pending, false, 'error cleanup');
    assert.equal(await bounded(panel.submit(async () => result)), result, 'error retry');
  }
  const reason = new Error('caller aborted');
  let listener;
  const aborted = panel.submit(received => {
    assert.equal(received, signal);
    return new Promise((_, reject) => {
      listener = () => reject(received.reason);
      received.addEventListener('abort', listener, { once: true });
    });
  }, signal);
  tasks.push(aborted);
  const rejected = assert.rejects(bounded(aborted), error => error === reason);
  try {
    assert.equal(panel.pending, true);
    controller.abort(reason);
    await rejected;
  } finally {
    signal.removeEventListener('abort', listener);
    if (!signal.aborted) controller.abort(reason);
    await rejected;
  }
  assert.equal(panel.pending, false, 'abort cleanup');
  assert.equal(await bounded(panel.submit(async () => result)), result, 'abort retry');
  console.log('all panel transitions passed');
} finally {
  finish(result);
  await bounded(Promise.allSettled(tasks));
}
