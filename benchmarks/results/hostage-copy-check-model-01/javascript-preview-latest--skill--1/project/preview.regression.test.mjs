import assert from 'node:assert/strict';
import test from 'node:test';
import { PreviewLoader } from './preview.mjs';
import { withControlledCalls } from './test-support/controlled_call.mjs';

// Copy fields, not the state object: an in-place stale mutation must fail too.
const snapshot = loader => ({ ...loader.state });
function stateIs(loader, status, value, error = null) {
  assert.equal(loader.state.status, status);
  assert.equal(loader.state.value, value);
  assert.equal(loader.state.error, error);
}
function unchanged(loader, before) {
  stateIs(loader, before.status, before.value, before.error);
}
async function seed(loader, scope) {
  const value = {};
  assert.equal(await scope.wait(scope.run(() => loader.load({}, () => ({}), () => value))), value);
  return value;
}
function request(loader, scope, key = {}, signal = new AbortController().signal) {
  const fetch = scope.call(), decode = scope.call();
  const bytes = {}, value = {};
  const displayed = loader.state.value;
  const task = scope.run(() => loader.load(key, (received, passed) => {
    stateIs(loader, 'loading', displayed);
    assert.equal(received, key);
    assert.equal(passed, signal);
    return fetch(received, passed);
  }, (received, passed) => {
    assert.equal(received, bytes);
    assert.equal(passed, signal);
    return decode(received, passed);
  }, signal));
  return { fetch, decode, bytes, value, task };
}
async function enterDecode(r) {
  (await r.fetch.started()).complete(r.bytes);
  return r.decode.started();
}
async function succeed(r, scope) {
  (await enterDecode(r)).complete(r.value);
  assert.equal(await scope.wait(r.task), r.value);
}

test('idle, loading in both phases, ready, error and recovery preserve displayed identities', () =>
  withControlledCalls(async scope => {
    const loader = new PreviewLoader();
    assert.deepEqual(loader.state, { status: 'idle', value: null, error: null });
    const first = request(loader, scope);
    stateIs(loader, 'loading', null);
    const decode = await enterDecode(first);
    stateIs(loader, 'loading', null);
    decode.complete(first.value);
    assert.equal(await scope.wait(first.task), first.value);
    stateIs(loader, 'ready', first.value);
    const failed = request(loader, scope), reason = {};
    stateIs(loader, 'loading', first.value);
    (await failed.fetch.started()).fail(reason);
    await assert.rejects(scope.wait(failed.task), error => error === reason);
    assert.equal(failed.decode.calls.length, 0);
    stateIs(loader, 'error', first.value, reason);
    const recovery = request(loader, scope);
    stateIs(loader, 'loading', first.value);
    await succeed(recovery, scope);
    stateIs(loader, 'ready', recovery.value);
  }));

for (const oldPhase of ['fetch', 'decode']) {
  for (const newPhase of ['fetch', 'decode', 'ready', 'error']) {
    for (const outcome of ['success', 'fetch failure', 'decode failure']) {
      if (oldPhase === 'decode' && outcome === 'fetch failure') continue;
      test(`stale ${oldPhase} / ${outcome} leaves newer ${newPhase} unchanged, even with identical keys`, () =>
        withControlledCalls(async scope => {
          const loader = new PreviewLoader(), key = {};
          const displayed = await seed(loader, scope);
          const old = request(loader, scope, key);
          const oldEntry = oldPhase === 'fetch' ? await old.fetch.started() : await enterDecode(old);
          const newest = request(loader, scope, key);
          const newFetch = await newest.fetch.started();
          let newDecode;
          const newReason = {};
          if (newPhase === 'error') {
            newFetch.fail(newReason);
            await assert.rejects(scope.wait(newest.task), error => error === newReason);
            stateIs(loader, 'error', displayed, newReason);
          } else if (newPhase !== 'fetch') {
            newFetch.complete(newest.bytes);
            newDecode = await newest.decode.started();
            if (newPhase === 'ready') {
              newDecode.complete(newest.value);
              assert.equal(await scope.wait(newest.task), newest.value);
              stateIs(loader, 'ready', newest.value);
            } else stateIs(loader, 'loading', displayed);
          } else stateIs(loader, 'loading', displayed);

          const before = snapshot(loader), oldReason = {};
          let oldDecode = oldPhase === 'decode' ? oldEntry : undefined;
          if (outcome === 'fetch failure') oldEntry.fail(oldReason);
          else {
            if (oldPhase === 'fetch') {
              oldEntry.complete(old.bytes);
              oldDecode = await old.decode.started();
              unchanged(loader, before);
            }
            if (outcome === 'success') oldDecode.complete(old.value);
            else oldDecode.fail(oldReason);
          }
          if (outcome === 'success') assert.equal(await scope.wait(old.task), old.value);
          else await assert.rejects(scope.wait(old.task), error => error === oldReason);
          if (outcome === 'fetch failure') assert.equal(old.decode.calls.length, 0);
          unchanged(loader, before);

          if (newPhase === 'fetch' || newPhase === 'decode') {
            if (newPhase === 'fetch') {
              newFetch.complete(newest.bytes);
              newDecode = await newest.decode.started();
            }
            newDecode.complete(newest.value);
            assert.equal(await scope.wait(newest.task), newest.value);
            stateIs(loader, 'ready', newest.value);
          }
        }));
    }
  }
}

for (const phase of ['fetch', 'decode']) {
  for (const synchronous of [true, false]) {
    for (const hasValue of [false, true]) {
      test(`${phase} ${synchronous ? 'throw' : 'rejection'} with ${hasValue ? 'displayed value' : 'no value'} recovers`, () =>
        withControlledCalls(async scope => {
          const loader = new PreviewLoader();
          const displayed = hasValue ? await seed(loader, scope) : null;
          // Non-Error reasons must also survive unchanged.
          const reason = {}, key = {}, bytes = {}, signal = new AbortController().signal;
          let decodeCalls = 0;
          const fail = () => {
            stateIs(loader, 'loading', displayed);
            if (synchronous) throw reason;
            return Promise.reject(reason);
          };
          let task;
          assert.doesNotThrow(() => {
            task = loader.load(key, (received, passed) => {
              assert.equal(received, key); assert.equal(passed, signal);
              return phase === 'fetch' ? fail() : bytes;
            }, (received, passed) => {
              decodeCalls++;
              assert.equal(received, bytes); assert.equal(passed, signal);
              return fail();
            }, signal);
          });
          scope.run(() => task);
          assert.ok(task instanceof Promise);
          await assert.rejects(scope.wait(task), error => error === reason);
          assert.equal(decodeCalls, phase === 'fetch' ? 0 : 1);
          stateIs(loader, 'error', displayed, reason);
          const recovery = request(loader, scope);
          stateIs(loader, 'loading', displayed);
          await succeed(recovery, scope);
          stateIs(loader, 'ready', recovery.value);
        }));
    }
  }
}

test('loader instances own independent request state', () => withControlledCalls(async scope => {
  const a = new PreviewLoader(), b = new PreviewLoader();
  const ar = request(a, scope), ad = await enterDecode(ar);
  const br = request(b, scope), bf = await br.fetch.started();
  const bBefore = snapshot(b);
  ad.complete(ar.value);
  assert.equal(await scope.wait(ar.task), ar.value);
  stateIs(a, 'ready', ar.value);
  unchanged(b, bBefore);
  const aBefore = snapshot(a), reason = {};
  bf.fail(reason);
  await assert.rejects(scope.wait(br.task), error => error === reason);
  stateIs(b, 'error', null, reason);
  unchanged(a, aBefore);
}));

for (const phase of ['fetch', 'decode']) {
  test(`a newer load invoked inside ${phase} survives the older synchronous throw`, () =>
    withControlledCalls(async scope => {
      const loader = new PreviewLoader(), reason = {};
      const displayed = await seed(loader, scope);
      let next, before;
      const fail = () => {
        next = request(loader, scope);
        before = snapshot(loader);
        throw reason;
      };
      const task = scope.run(() => loader.load({}, phase === 'fetch' ? fail : () => ({}),
        phase === 'decode' ? fail : () => assert.fail('decode after fetch failure')));
      await assert.rejects(scope.wait(task), error => error === reason);
      unchanged(loader, before);
      stateIs(loader, 'loading', displayed);
      await succeed(next, scope);
      stateIs(loader, 'ready', next.value);
    }));
}

test('aborting a signal does not force an ignoring callback to fail or skip decode', () =>
  withControlledCalls(async scope => {
    const loader = new PreviewLoader(), controller = new AbortController();
    const r = request(loader, scope, {}, controller.signal);
    const before = snapshot(loader);
    controller.abort({});
    unchanged(loader, before);
    await succeed(r, scope);
    stateIs(loader, 'ready', r.value);
  }));

for (const phase of ['fetch', 'decode']) {
  for (const newer of ['none', 'fetch', 'ready', 'error']) {
    test(`actual abort rejection during ${phase}, newer request: ${newer}`, () =>
      withControlledCalls(async scope => {
        const loader = new PreviewLoader(), controller = new AbortController();
        const displayed = await seed(loader, scope);
        const fetch = scope.call(), decode = scope.call(), reason = {};
        const key = {}, bytes = {};
        let abortEntry, listener, abortCalls = 0;
        const abortable = callback => (argument, signal) => {
          assert.equal(signal, controller.signal);
          const promise = callback(argument, signal);
          abortEntry = callback.calls.at(-1);
          listener = () => {
            abortCalls++;
            abortEntry.fail(signal.reason);
          };
          signal.addEventListener('abort', listener, { once: true });
          return promise;
        };
        const fetchCallback = phase === 'fetch' ? abortable(fetch) : fetch;
        const decodeCallback = phase === 'decode' ? abortable(decode) : decode;
        try {
          const task = scope.run(() => loader.load(key, fetchCallback, decodeCallback, controller.signal));
          const fe = await fetch.started();
          assert.equal(fe.args[0], key); assert.equal(fe.args[1], controller.signal);
          if (phase === 'decode') {
            fe.complete(bytes);
            const de = await decode.started();
            assert.equal(de.args[0], bytes); assert.equal(de.args[1], controller.signal);
          }
          let next;
          if (newer !== 'none') {
            next = request(loader, scope);
            if (newer === 'ready') await succeed(next, scope);
            if (newer === 'error') {
              const newReason = {};
              (await next.fetch.started()).fail(newReason);
              await assert.rejects(scope.wait(next.task), error => error === newReason);
              stateIs(loader, 'error', displayed, newReason);
            }
          }
          const before = snapshot(loader);
          assert.equal(controller.signal.aborted, false);
          controller.abort(reason);
          await assert.rejects(scope.wait(task), error => error === reason);
          assert.equal(abortCalls, 1);
          if (phase === 'fetch') assert.equal(decode.calls.length, 0);
          if (newer === 'none') stateIs(loader, 'error', displayed, reason);
          else unchanged(loader, before);
          if (newer === 'fetch') {
            await succeed(next, scope);
            stateIs(loader, 'ready', next.value);
          } else if (newer === 'none') {
            const recovery = request(loader, scope);
            await succeed(recovery, scope);
            stateIs(loader, 'ready', recovery.value);
          }
        } finally {
          if (listener) controller.signal.removeEventListener('abort', listener);
        }
      }));
  }
}
