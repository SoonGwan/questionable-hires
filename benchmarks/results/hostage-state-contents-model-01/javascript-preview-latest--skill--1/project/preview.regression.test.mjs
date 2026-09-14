import assert from 'node:assert/strict';
import test from 'node:test';
import { PreviewLoader } from './preview.mjs';
import { withControlledCalls } from './test-support/controlled_call.mjs';

function state(loader, status, value, error = null) {
  assert.equal(loader.state.status, status);
  assert.equal(loader.state.value, value);
  assert.equal(loader.state.error, error);
}
function snapshot(loader) {
  return { status: loader.state.status, value: loader.state.value, error: loader.state.error };
}
function unchanged(loader, before) {
  state(loader, before.status, before.value, before.error);
}
function request(scope, loader, key = {}, signal = new AbortController().signal) {
  const fetch = scope.call(), decode = scope.call(), bytes = {}, value = {};
  const displayed = loader.state.value;
  const task = scope.run(() => loader.load(key, (received, passed) => {
    state(loader, 'loading', displayed);
    return fetch(received, passed);
  }, decode, signal));
  return { fetch, decode, bytes, value, task, key, signal };
}
async function fetched(r) {
  const entry = await r.fetch.started();
  assert.equal(entry.args[0], r.key);
  assert.equal(entry.args[1], r.signal);
  return entry;
}
async function decoded(r) {
  const entry = await r.decode.started();
  assert.equal(entry.args[0], r.bytes);
  assert.equal(entry.args[1], r.signal);
  return entry;
}
async function finish(scope, r) {
  (await fetched(r)).complete(r.bytes);
  (await decoded(r)).complete(r.value);
  assert.equal(await scope.wait(r.task), r.value);
}
async function rejects(scope, task, reason) {
  await assert.rejects(scope.wait(task), error => error === reason);
}

test('idle, loading, ready, error, and recovery retain exact displayed values', () => withControlledCalls(async scope => {
  const loader = new PreviewLoader();
  assert.deepEqual(loader.state, { status: 'idle', value: null, error: null });
  const first = request(scope, loader);
  state(loader, 'loading', null);
  await finish(scope, first);
  state(loader, 'ready', first.value);
  const next = request(scope, loader);
  state(loader, 'loading', first.value);
  (await fetched(next)).complete(next.bytes);
  state(loader, 'loading', first.value);
  const reason = {};
  (await decoded(next)).fail(reason);
  await rejects(scope, next.task, reason);
  state(loader, 'error', first.value, reason);
  const recovery = request(scope, loader);
  state(loader, 'loading', first.value);
  await finish(scope, recovery);
  state(loader, 'ready', recovery.value);
}));

for (const phase of ['fetch', 'decode']) {
  for (const newerState of ['fetch', 'decode', 'ready', 'error']) {
    for (const outcome of ['success', 'fetch failure', 'decode failure']) {
      if (phase === 'decode' && outcome === 'fetch failure') continue;
      for (const sameKey of [false, true]) {
        test(`older ${phase}: ${outcome}, newer ${newerState}, ${sameKey ? 'identical' : 'distinct'} keys`, () => withControlledCalls(async scope => {
          const loader = new PreviewLoader(), displayed = {};
          await scope.wait(scope.run(() => loader.load({}, () => ({}), () => displayed)));
          const key = {};
          const older = request(scope, loader, key);
          const oldFetch = await fetched(older);
          let oldDecode;
          if (phase === 'decode') {
            oldFetch.complete(older.bytes);
            oldDecode = await decoded(older);
          }
          const newer = request(scope, loader, sameKey ? key : {});
          const newFetch = await fetched(newer);
          let newDecode;
          if (newerState !== 'fetch') {
            newFetch.complete(newer.bytes);
            newDecode = await decoded(newer);
          }
          const newReason = {};
          if (newerState === 'ready') {
            newDecode.complete(newer.value);
            assert.equal(await scope.wait(newer.task), newer.value);
            state(loader, 'ready', newer.value);
          } else if (newerState === 'error') {
            newDecode.fail(newReason);
            await rejects(scope, newer.task, newReason);
            state(loader, 'error', displayed, newReason);
          } else state(loader, 'loading', displayed);
          const before = snapshot(loader), oldReason = {};
          if (outcome === 'fetch failure') {
            oldFetch.fail(oldReason);
            await rejects(scope, older.task, oldReason);
            assert.equal(older.decode.calls.length, 0);
          } else {
            if (!oldDecode) {
              oldFetch.complete(older.bytes);
              oldDecode = await decoded(older);
              unchanged(loader, before);
            }
            if (outcome === 'success') {
              oldDecode.complete(older.value);
              assert.equal(await scope.wait(older.task), older.value);
            } else {
              oldDecode.fail(oldReason);
              await rejects(scope, older.task, oldReason);
            }
          }
          unchanged(loader, before);
          if (newerState === 'fetch') {
            newFetch.complete(newer.bytes);
            newDecode = await decoded(newer);
          }
          if (newerState === 'fetch' || newerState === 'decode') {
            newDecode.complete(newer.value);
            assert.equal(await scope.wait(newer.task), newer.value);
            state(loader, 'ready', newer.value);
          }
        }));
      }
    }
  }
}

for (const phase of ['fetch', 'decode']) {
  for (const synchronous of [true, false]) {
    test(`${phase} ${synchronous ? 'throw' : 'rejection'} preserves reason and recovers`, () => withControlledCalls(async scope => {
      const loader = new PreviewLoader(), value = {}, reason = {};
      await scope.wait(scope.run(() => loader.load({}, () => ({}), () => value)));
      const gate = scope.call();
      let decodes = 0, task;
      const failure = synchronous ? () => { throw reason; } : gate;
      assert.doesNotThrow(() => {
        task = loader.load({}, phase === 'fetch' ? failure : () => ({}), (...args) => {
          decodes++;
          return failure(...args);
        });
      });
      scope.run(() => task);
      assert.ok(task instanceof Promise);
      if (!synchronous) (await gate.started()).fail(reason);
      await rejects(scope, task, reason);
      assert.equal(decodes, phase === 'fetch' ? 0 : 1);
      state(loader, 'error', value, reason);
      const recovery = request(scope, loader);
      await finish(scope, recovery);
      state(loader, 'ready', recovery.value);
    }));
  }
}

test('request ownership is isolated per instance', () => withControlledCalls(async scope => {
  const a = new PreviewLoader(), b = new PreviewLoader();
  const first = request(scope, a), second = request(scope, b);
  await finish(scope, first);
  state(a, 'ready', first.value);
  state(b, 'loading', null);
  const before = snapshot(a);
  const reason = {};
  (await fetched(second)).fail(reason);
  await rejects(scope, second.task, reason);
  state(b, 'error', null, reason);
  unchanged(a, before);
}));

for (const phase of ['fetch', 'decode']) {
  for (const newerState of ['none', 'fetch', 'decode', 'ready', 'error']) {
    test(`actual abort rejection in ${phase}, newer ${newerState}`, () => withControlledCalls(async scope => {
      const loader = new PreviewLoader(), controller = new AbortController();
      const gate = scope.call(), bytes = {}, key = {}, reason = {};
      let entry, listener, decodeCount = 0;
      const aborting = (arg, signal) => {
        assert.equal(arg, phase === 'fetch' ? key : bytes);
        assert.equal(signal, controller.signal);
        const pending = gate(arg, signal);
        entry = gate.calls.at(-1);
        listener = () => { if (!entry.released) entry.fail(signal.reason); };
        signal.addEventListener('abort', listener, { once: true });
        return pending;
      };
      const task = scope.run(() => loader.load(key, phase === 'fetch' ? aborting : () => bytes,
        (...args) => { decodeCount++; return aborting(...args); }, controller.signal));
      try {
        await gate.started();
        let newer;
        if (newerState !== 'none') {
          newer = request(scope, loader);
          if (newerState === 'ready') await finish(scope, newer);
          else if (newerState === 'error') {
            const newerReason = {};
            (await fetched(newer)).fail(newerReason);
            await rejects(scope, newer.task, newerReason);
          } else if (newerState === 'decode') {
            (await fetched(newer)).complete(newer.bytes);
            // Keep the decode pending until after the older request aborts.
            const pending = await decoded(newer);
            newer.pendingDecode = pending;
          }
        }
        const before = snapshot(loader);
        controller.abort(reason);
        await rejects(scope, task, reason);
        assert.equal(controller.signal.reason, reason);
        assert.equal(decodeCount, phase === 'fetch' ? 0 : 1);
        if (newer) unchanged(loader, before);
        else state(loader, 'error', null, reason);
        if (newerState === 'fetch') await finish(scope, newer);
        if (newerState === 'decode') {
          newer.pendingDecode.complete(newer.value);
          assert.equal(await scope.wait(newer.task), newer.value);
        }
        const recovery = request(scope, loader);
        await finish(scope, recovery);
        state(loader, 'ready', recovery.value);
      } finally {
        if (listener) controller.signal.removeEventListener('abort', listener);
      }
    }));
  }
}
