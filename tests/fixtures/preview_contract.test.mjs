// Author-only native contract; never included in model-visible files.
import assert from 'node:assert/strict';
import test from 'node:test';
import { PreviewLoader } from './preview.mjs';

function assertState(actual, expected) {
  assert.equal(actual.status, expected.status, 'state status');
  assert.equal(actual.value, expected.value, 'displayed value identity');
  assert.equal(actual.error, expected.error, 'error reason identity');
}

async function enteredOrFailure(entry, task) {
  await bounded(Promise.race([entry, task.then(
    () => assert.fail('application settled before expected callback entry'),
    error => { throw error; },
  )]));
}

async function bounded(promise) {
  let timer;
  try {
    return await Promise.race([promise, new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error('preview contract deadline')), 1000);
    })]);
  } finally { clearTimeout(timer); }
}

async function scenario(check) {
  const gates = [], tasks = [];
  const own = {
    gate() {
      let resolve, reject;
      const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
      promise.catch(() => {});
      const gate = { promise, resolve, reject };
      gates.push(gate);
      return gate;
    },
    track(promise) { promise.catch(() => {}); tasks.push(promise); return promise; },
  };
  try { await check(own); }
  finally {
    for (const gate of gates) gate.resolve();
    await bounded(Promise.allSettled(tasks));
  }
}

test('initial state, immediate loading and preserving displayed value across failure/recovery', () => scenario(async own => {
  const loader = new PreviewLoader(), prior = {}, next = {}, failure = {};
  assertState(loader.state, { status: 'idle', value: null, error: null });
  assert.equal(await bounded(loader.load('seed', () => ({}), () => prior)), prior);
  const held = own.gate();
  const task = own.track(loader.load('next', () => {
    assertState(loader.state, { status: 'loading', value: prior, error: null });
    return held.promise;
  }, () => assert.fail('decode after failed fetch')));
  assert.equal(loader.state.status, 'loading');
  held.reject(failure);
  await assert.rejects(bounded(task), error => error === failure);
  assertState(loader.state, { status: 'error', value: prior, error: failure });
  assert.equal(await bounded(loader.load('retry', () => {
    assertState(loader.state, { status: 'loading', value: prior, error: null });
    return {};
  }, () => next)), next);
  assertState(loader.state, { status: 'ready', value: next, error: null });
}));

for (const oldPhase of ['fetch', 'decode']) {
  for (const newestState of ['loading', 'ready', 'error']) {
    for (const oldOutcome of ['success', 'failure']) {
  test(`old ${oldPhase} ${oldOutcome} cannot overwrite newer ${newestState}, identical keys`, () => scenario(async own => {
    const loader = new PreviewLoader(), key = {}, bytes = {}, olderValue = {}, newerValue = {};
    const signal = new AbortController().signal;
    const held = own.gate(), entered = own.gate(), newFetch = own.gate();
    const oldError = {}, newError = {};
    const old = own.track(loader.load(key, (actualKey, actualSignal) => {
      assert.equal(actualKey, key); assert.equal(actualSignal, signal);
      if (oldPhase === 'fetch') { entered.resolve(); return held.promise; }
      return bytes;
    }, (actualBytes, actualSignal) => {
      if (oldPhase === 'fetch' && oldOutcome === 'failure') assert.fail('decode after failed fetch');
      assert.equal(actualBytes, bytes); assert.equal(actualSignal, signal);
      if (oldPhase === 'decode') { entered.resolve(); return held.promise; }
      return olderValue;
    }, signal));
    await enteredOrFailure(entered.promise, old);
    const newer = own.track(loader.load(key, () => newFetch.promise, () => newerValue));
    if (newestState === 'ready') {
      newFetch.resolve({});
      assert.equal(await bounded(newer), newerValue);
    }
    if (newestState === 'error') {
      newFetch.reject(newError);
      await assert.rejects(bounded(newer), error => error === newError);
    }
    const expected = { ...loader.state };
    assert.equal(expected.status, newestState);
    if (oldOutcome === 'success') {
      held.resolve(oldPhase === 'fetch' ? bytes : olderValue);
      assert.equal(await bounded(old), olderValue, 'stale callers still receive their own value');
    } else {
      held.reject(oldError);
      await assert.rejects(bounded(old), error => error === oldError);
    }
    assertState(loader.state, expected);
  }));
    }
  }
}

test('synchronous/asynchronous failures in either phase preserve Promise API and recover', async () => {
  for (const phase of ['fetch', 'decode']) for (const sync of [false, true]) {
    const loader = new PreviewLoader(), error = {}, value = {};
    const fail = sync ? () => { throw error; } : async () => { throw error; };
    let task;
    assert.doesNotThrow(() => {
      task = loader.load('key', phase === 'fetch' ? fail : () => ({}),
        phase === 'decode' ? fail : () => assert.fail('decode after fetch failure'));
    });
    await assert.rejects(bounded(task), reason => reason === error);
    assertState(loader.state, { status: 'error', value: null, error });
    assert.equal(await bounded(loader.load('retry', () => ({}), () => value)), value);
    assertState(loader.state, { status: 'ready', value, error: null });
  }
});

test('separate instances remain independent', () => scenario(async own => {
  const first = new PreviewLoader(), second = new PreviewLoader(), held = own.gate();
  const firstValue = {}, secondValue = {};
  const task = own.track(first.load('x', () => held.promise, () => firstValue));
  assert.equal(await bounded(second.load('x', () => ({}), () => secondValue)), secondValue);
  assert.equal(first.state.status, 'loading');
  held.resolve({});
  assert.equal(await bounded(task), firstValue);
  assertState(first.state, { status: 'ready', value: firstValue, error: null });
  assertState(second.state, { status: 'ready', value: secondValue, error: null });
}));

test('actual callback-owned abort in decode propagates reason and permits retry', () => scenario(async own => {
  const loader = new PreviewLoader(), controller = new AbortController();
  const held = own.gate(), entered = own.gate(), reason = {}, value = {};
  let listener;
  try {
    const task = own.track(loader.load('x', (_, signal) => {
      assert.equal(signal, controller.signal); return {};
    }, (_, signal) => {
      assert.equal(signal, controller.signal);
      listener = () => held.reject(signal.reason);
      signal.addEventListener('abort', listener, { once: true });
      entered.resolve(); return held.promise;
    }, controller.signal));
    await enteredOrFailure(entered.promise, task);
    controller.abort(reason);
    await assert.rejects(bounded(task), error => error === reason);
    assertState(loader.state, { status: 'error', value: null, error: reason });
    assert.equal(await bounded(loader.load('retry', () => ({}), () => value)), value);
  } finally { if (listener) controller.signal.removeEventListener('abort', listener); }
}));
