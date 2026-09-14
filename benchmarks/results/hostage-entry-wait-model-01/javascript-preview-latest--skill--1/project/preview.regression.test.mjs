import assert from 'node:assert/strict';
import test from 'node:test';
import { PreviewLoader } from './preview.mjs';
import { withControlledCalls } from './test-support/controlled_call.mjs';

// Copy fields, retaining contractual payload/error identities, without aliasing state.
const snapshot = loader => ({ ...loader.state });
function stateIs(loader, status, value, error = null) {
  assert.equal(loader.state.status, status);
  assert.equal(loader.state.value, value);
  assert.equal(loader.state.error, error);
}
function unchanged(loader, before) {
  stateIs(loader, before.status, before.value, before.error);
}
function request(scope, loader, key = {}, signal = new AbortController().signal) {
  const fetch = scope.call(), decode = scope.call();
  const bytes = {}, value = {};
  const task = scope.run(() => loader.load(key, fetch, decode, signal));
  return { fetch, decode, bytes, value, task, key, signal };
}
async function fetched(r) {
  const entry = await r.fetch.startedBefore(r.task);
  assert.equal(entry.args[0], r.key);
  assert.equal(entry.args[1], r.signal);
  return entry;
}
async function decoded(r) {
  const entry = await r.decode.startedBefore(r.task);
  assert.equal(entry.args[0], r.bytes);
  assert.equal(entry.args[1], r.signal);
  return entry;
}
async function succeed(scope, r) {
  (await fetched(r)).complete(r.bytes);
  (await decoded(r)).complete(r.value);
  assert.equal(await scope.wait(r.task), r.value);
}
async function rejects(scope, task, reason) {
  await assert.rejects(scope.wait(task), error => error === reason);
}

test('idle, loading in both phases, ready and reload preserve exact displayed value', () =>
  withControlledCalls(async scope => {
    const loader = new PreviewLoader();
    assert.deepEqual(loader.state, { status: 'idle', value: null, error: null });
    for (let invocation = 0; invocation < 2; invocation++) {
      const previous = loader.state.value;
      const r = request(scope, loader);
      stateIs(loader, 'loading', previous);
      (await fetched(r)).complete(r.bytes);
      const decode = await decoded(r);
      stateIs(loader, 'loading', previous);
      decode.complete(r.value);
      assert.equal(await scope.wait(r.task), r.value);
      stateIs(loader, 'ready', r.value);
    }
  }));

for (const phase of ['fetch', 'decode']) {
  for (const mode of ['throw', 'reject']) {
    for (const seeded of [false, true]) {
      test(`${phase} ${mode}, displayed=${seeded}: exact failure and recovery`, () =>
        withControlledCalls(async scope => {
          const loader = new PreviewLoader();
          if (seeded) await succeed(scope, request(scope, loader));
          const displayed = loader.state.value, reason = { phase, mode };
          const key = {}, bytes = {}, signal = new AbortController().signal;
          const failure = scope.call();
          let decodeCount = 0;
          const fail = () => {
            stateIs(loader, 'loading', displayed);
            if (mode === 'throw') throw reason;
            return failure();
          };
          let task;
          assert.doesNotThrow(() => {
            task = loader.load(key, (received, passed) => {
              assert.equal(received, key); assert.equal(passed, signal);
              return phase === 'fetch' ? fail() : bytes;
            }, (received, passed) => {
              decodeCount++;
              assert.equal(received, bytes); assert.equal(passed, signal);
              return fail();
            }, signal);
          });
          scope.run(() => task);
          assert.ok(task instanceof Promise);
          if (mode === 'reject') (await failure.startedBefore(task)).fail(reason);
          await rejects(scope, task, reason);
          assert.equal(decodeCount, phase === 'fetch' ? 0 : 1);
          stateIs(loader, 'error', displayed, reason);
          const recovery = request(scope, loader);
          stateIs(loader, 'loading', displayed);
          await succeed(scope, recovery);
          stateIs(loader, 'ready', recovery.value);
        }));
    }
  }
}

for (const oldPhase of ['fetch', 'decode']) {
  for (const outcome of ['success', 'fetch failure', 'decode failure']) {
    if (oldPhase === 'decode' && outcome === 'fetch failure') continue;
    for (const newerPhase of ['fetch', 'decode', 'ready', 'error']) {
      test(`overlap during ${oldPhase}: stale ${outcome} leaves newer ${newerPhase} unchanged (same key)`, () =>
        withControlledCalls(async scope => {
          const loader = new PreviewLoader();
          await succeed(scope, request(scope, loader));
          const displayed = loader.state.value, key = {};
          const old = request(scope, loader, key);
          let oldEntry = await fetched(old);
          if (oldPhase === 'decode') {
            oldEntry.complete(old.bytes);
            oldEntry = await decoded(old);
          }
          const newest = request(scope, loader, key);
          let newEntry = await fetched(newest);
          stateIs(loader, 'loading', displayed);
          if (newerPhase === 'decode' || newerPhase === 'ready') {
            newEntry.complete(newest.bytes);
            newEntry = await decoded(newest);
          }
          const newReason = {};
          if (newerPhase === 'ready') {
            newEntry.complete(newest.value);
            assert.equal(await scope.wait(newest.task), newest.value);
            stateIs(loader, 'ready', newest.value);
          } else if (newerPhase === 'error') {
            newEntry.fail(newReason);
            await rejects(scope, newest.task, newReason);
            stateIs(loader, 'error', displayed, newReason);
          }
          const before = snapshot(loader), oldReason = {};
          if (outcome === 'fetch failure') {
            oldEntry.fail(oldReason);
          } else {
            if (oldPhase === 'fetch') {
              oldEntry.complete(old.bytes);
              oldEntry = await decoded(old); // stale successful fetch must still decode
              unchanged(loader, before);
            }
            if (outcome === 'success') oldEntry.complete(old.value);
            else oldEntry.fail(oldReason);
          }
          if (outcome === 'success') assert.equal(await scope.wait(old.task), old.value);
          else await rejects(scope, old.task, oldReason);
          unchanged(loader, before);
          assert.equal(old.fetch.calls.length, 1);
          assert.equal(old.decode.calls.length, outcome === 'fetch failure' ? 0 : 1);
          if (newerPhase === 'fetch') {
            newEntry.complete(newest.bytes);
            newEntry = await decoded(newest);
          }
          if (newerPhase === 'fetch' || newerPhase === 'decode') {
            newEntry.complete(newest.value);
            assert.equal(await scope.wait(newest.task), newest.value);
            stateIs(loader, 'ready', newest.value);
          }
        }));
    }
  }
}

test('requests and state are isolated between instances', () =>
  withControlledCalls(async scope => {
    const left = new PreviewLoader(), right = new PreviewLoader(), key = {};
    const a = request(scope, left, key), b = request(scope, right, key);
    const rightPending = snapshot(right);
    await succeed(scope, a);
    stateIs(left, 'ready', a.value);
    unchanged(right, rightPending);
    const leftReady = snapshot(left), reason = {};
    (await fetched(b)).fail(reason);
    await rejects(scope, b.task, reason);
    stateIs(right, 'error', null, reason);
    unchanged(left, leftReady);
    const rightError = snapshot(right);
    const c = request(scope, left, key);
    await succeed(scope, c);
    unchanged(right, rightError);
    await succeed(scope, request(scope, right, key));
    stateIs(left, 'ready', c.value);
  }));

// Abort the controller only in the test. The callback itself rejects on its signal.
for (const phase of ['fetch', 'decode']) {
  for (const newerPhase of ['none', 'fetch', 'decode', 'ready', 'error']) {
    test(`signal-driven ${phase} rejection with newer ${newerPhase}`, () =>
      withControlledCalls(async scope => {
        const loader = new PreviewLoader();
        await succeed(scope, request(scope, loader));
        const displayed = loader.state.value;
        const controller = new AbortController(), reason = {};
        const fetch = scope.call(), decode = scope.call(), key = {}, bytes = {};
        let removeListener = () => {}, abortCount = 0;
        const abortable = callback => (...args) => {
          const task = callback(...args), entry = callback.calls.at(-1);
          const signal = args[1];
          const onAbort = () => { abortCount++; entry.fail(signal.reason); };
          signal.addEventListener('abort', onAbort, { once: true });
          removeListener = () => signal.removeEventListener('abort', onAbort);
          return task;
        };
        try {
          const task = scope.run(() => loader.load(key,
            phase === 'fetch' ? abortable(fetch) : fetch,
            phase === 'decode' ? abortable(decode) : decode, controller.signal));
          const f = await fetch.startedBefore(task);
          assert.equal(f.args[0], key); assert.equal(f.args[1], controller.signal);
          if (phase === 'decode') {
            f.complete(bytes);
            const d = await decode.startedBefore(task);
            assert.equal(d.args[0], bytes); assert.equal(d.args[1], controller.signal);
          }
          let newer, pending;
          if (newerPhase !== 'none') {
            newer = request(scope, loader);
            pending = await fetched(newer);
            if (newerPhase === 'decode' || newerPhase === 'ready') {
              pending.complete(newer.bytes);
              pending = await decoded(newer);
            }
            if (newerPhase === 'ready') {
              pending.complete(newer.value);
              assert.equal(await scope.wait(newer.task), newer.value);
            } else if (newerPhase === 'error') {
              const newReason = {};
              pending.fail(newReason);
              await rejects(scope, newer.task, newReason);
              stateIs(loader, 'error', displayed, newReason);
            }
          }
          const before = snapshot(loader);
          assert.equal(controller.signal.aborted, false);
          controller.abort(reason);
          await rejects(scope, task, reason);
          assert.equal(abortCount, 1);
          assert.equal(decode.calls.length, phase === 'fetch' ? 0 : 1);
          if (newerPhase === 'none') stateIs(loader, 'error', displayed, reason);
          else unchanged(loader, before);
          if (newerPhase === 'fetch') {
            pending.complete(newer.bytes);
            pending = await decoded(newer);
          }
          if (newerPhase === 'fetch' || newerPhase === 'decode') {
            pending.complete(newer.value);
            assert.equal(await scope.wait(newer.task), newer.value);
            stateIs(loader, 'ready', newer.value);
          }
          const recovery = request(scope, loader);
          await succeed(scope, recovery);
          stateIs(loader, 'ready', recovery.value);
        } finally { removeListener(); }
      }));
  }
}

for (const phase of ['fetch', 'decode']) {
  test(`reentrant newer request survives synchronous stale ${phase} throw`, () =>
    withControlledCalls(async scope => {
      const loader = new PreviewLoader(), reason = {}, bytes = {};
      let newer, before, decodeCount = 0;
      const supersedeAndThrow = () => {
        newer = request(scope, loader);
        stateIs(loader, 'loading', null);
        before = snapshot(loader);
        throw reason;
      };
      const old = scope.run(() => loader.load({},
        phase === 'fetch' ? supersedeAndThrow : () => bytes,
        received => {
          decodeCount++;
          assert.equal(received, bytes);
          return supersedeAndThrow();
        }));
      await rejects(scope, old, reason);
      unchanged(loader, before);
      assert.equal(decodeCount, phase === 'fetch' ? 0 : 1);
      await succeed(scope, newer);
      stateIs(loader, 'ready', newer.value);
    }));
}

test('abort does not force callbacks that ignore the signal to reject or skip decode', () =>
  withControlledCalls(async scope => {
    const loader = new PreviewLoader(), controller = new AbortController();
    const r = request(scope, loader, {}, controller.signal);
    const f = await fetched(r);
    controller.abort({});
    f.complete(r.bytes);
    const d = await decoded(r);
    stateIs(loader, 'loading', null);
    d.complete(r.value);
    assert.equal(await scope.wait(r.task), r.value);
    stateIs(loader, 'ready', r.value);
  }));
