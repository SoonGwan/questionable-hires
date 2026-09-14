import assert from 'node:assert/strict';
import test from 'node:test';
import { PreviewLoader } from './preview.mjs';
import { withControlledCalls } from './test-support/controlled_call.mjs';

function state(loader, status, value, ...errors) {
  const error = errors.length ? errors[0] : null;
  assert.equal(loader.state.status, status);
  assert.equal(loader.state.value, value);
  assert.equal(loader.state.error, error);
  assert.deepEqual(Object.keys(loader.state).sort(), ['error', 'status', 'value']);
}

function begin(scope, loader, key = {}, signal = new AbortController().signal) {
  const fetch = scope.call(), decode = scope.call(), bytes = {}, value = {};
  const task = scope.run(() => loader.load(key, fetch, decode, signal));
  return { fetch, decode, bytes, value, task, key, signal };
}

async function fetchEntry(request) {
  const entry = await request.fetch.started(1000);
  assert.equal(entry.args.length, 2);
  assert.equal(entry.args[0], request.key);
  assert.equal(entry.args[1], request.signal);
  return entry;
}

async function decodeEntry(request) {
  const entry = await request.decode.started(1000);
  assert.equal(entry.args.length, 2);
  assert.equal(entry.args[0], request.bytes);
  assert.equal(entry.args[1], request.signal);
  return entry;
}

async function finish(scope, request, entry, phase, outcome, reason) {
  if (outcome === 'failure') {
    entry.fail(reason);
    await assert.rejects(scope.wait(request.task), error => error === reason);
    if (phase === 'fetch') assert.equal(request.decode.calls.length, 0);
  } else {
    if (phase === 'fetch') {
      entry.complete(request.bytes);
      entry = await decodeEntry(request);
    }
    entry.complete(request.value);
    assert.equal(await scope.wait(request.task), request.value);
  }
}

async function seed(scope, loader) {
  const value = {};
  assert.equal(await scope.wait(scope.run(() => loader.load({}, () => ({}), () => value))), value);
  return value;
}

test('initial, loading before fetch, loading during decode, and ready preserve identities', async () => {
  await withControlledCalls(async scope => {
    const loader = new PreviewLoader(), key = {}, bytes = {}, value = {};
    state(loader, 'idle', null);
    const fetch = scope.call(), decode = scope.call();
    const task = scope.run(() => loader.load(key, (...args) => {
      state(loader, 'loading', null);
      return fetch(...args);
    }, decode));
    const request = { fetch, decode, key, bytes, signal: undefined };
    state(loader, 'loading', null);
    (await fetchEntry(request)).complete(bytes);
    const entry = await decodeEntry(request);
    state(loader, 'loading', null);
    entry.complete(value);
    assert.equal(await scope.wait(task), value);
    state(loader, 'ready', value);
  });
});

// Cross both overlap entry phases with every newer pending/settled state.
// Identical keys still represent distinct invocations and run both pipelines.
for (const sameKey of [false, true]) {
  for (const oldPhase of ['fetch', 'decode']) {
    for (const oldOutcome of ['success', 'failure']) {
      for (const newPhase of ['fetch', 'decode', 'ready', 'error']) {
        test(`stale ${oldPhase} ${oldOutcome}, newer ${newPhase}, ${sameKey ? 'identical' : 'distinct'} keys`, async () => {
          await withControlledCalls(async scope => {
            const loader = new PreviewLoader();
            const displayed = await seed(scope, loader);
            const old = begin(scope, loader);
            let oldEntry = await fetchEntry(old);
            if (oldPhase === 'decode') {
              oldEntry.complete(old.bytes);
              oldEntry = await decodeEntry(old);
            }
            state(loader, 'loading', displayed);
            const newest = begin(scope, loader, sameKey ? old.key : {});
            let newEntry = await fetchEntry(newest);
            assert.equal(old.signal.aborted, false);
            assert.equal(newest.signal.aborted, false);
            if (newPhase === 'decode' || newPhase === 'ready') {
              newEntry.complete(newest.bytes);
              newEntry = await decodeEntry(newest);
            }
            const newError = {}, oldError = {};
            if (newPhase === 'ready') {
              await finish(scope, newest, newEntry, 'decode', 'success');
              state(loader, 'ready', newest.value);
            } else if (newPhase === 'error') {
              await finish(scope, newest, newEntry, 'fetch', 'failure', newError);
              state(loader, 'error', displayed, newError);
            } else {
              state(loader, 'loading', displayed);
            }
            const protectedState = loader.state;
            await finish(scope, old, oldEntry, oldPhase, oldOutcome, oldError);
            assert.equal(loader.state, protectedState);
            if (newPhase === 'fetch' || newPhase === 'decode') {
              await finish(scope, newest, newEntry, newPhase, 'success');
              state(loader, 'ready', newest.value);
            }
          });
        });
      }
    }
  }
}

for (const phase of ['fetch', 'decode']) {
  for (const synchronous of [true, false]) {
    for (const initiallyReady of [false, true]) {
      test(`${phase} ${synchronous ? 'throw' : 'rejection'} from ${initiallyReady ? 'ready' : 'idle'} and recovery`, async () => {
        await withControlledCalls(async scope => {
          const loader = new PreviewLoader();
          const displayed = initiallyReady ? await seed(scope, loader) : null;
          // Include non-Error rejection reasons, including null/undefined.
          const reason = synchronous ? (initiallyReady ? null : {}) : (initiallyReady ? undefined : new Error('failure'));
          const gate = scope.call(), key = {}, bytes = {}, signal = new AbortController().signal;
          let decodeCalls = 0;
          const fail = (...args) => {
            state(loader, 'loading', displayed);
            if (synchronous) throw reason;
            return gate(...args);
          };
          let task;
          assert.doesNotThrow(() => {
            task = loader.load(key, (received, passed) => {
              assert.equal(received, key);
              assert.equal(passed, signal);
              return phase === 'fetch' ? fail(received, passed) : bytes;
            }, (received, passed) => {
              decodeCalls++;
              assert.equal(received, bytes);
              assert.equal(passed, signal);
              return phase === 'decode' ? fail(received, passed) : assert.fail('decode after fetch failure');
            }, signal);
          });
          scope.run(() => task);
          if (!synchronous) {
            const entry = await gate.started(1000);
            state(loader, 'loading', displayed);
            entry.fail(reason);
          }
          await assert.rejects(scope.wait(task), error => error === reason);
          assert.equal(decodeCalls, phase === 'fetch' ? 0 : 1);
          state(loader, 'error', displayed, reason);
          const recovery = begin(scope, loader);
          state(loader, 'loading', displayed);
          await finish(scope, recovery, await fetchEntry(recovery), 'fetch', 'success');
          state(loader, 'ready', recovery.value);
        });
      });
    }
  }
}

test('request ownership is isolated per instance', async () => {
  await withControlledCalls(async scope => {
    const a = new PreviewLoader(), b = new PreviewLoader();
    const first = begin(scope, a), second = begin(scope, b, first.key);
    const firstEntry = await fetchEntry(first), secondEntry = await fetchEntry(second);
    await finish(scope, first, firstEntry, 'fetch', 'success');
    state(a, 'ready', first.value);
    state(b, 'loading', null);
    const third = begin(scope, a);
    const thirdEntry = await fetchEntry(third), error = {};
    await finish(scope, second, secondEntry, 'fetch', 'failure', error);
    state(b, 'error', null, error);
    state(a, 'loading', first.value);
    await finish(scope, third, thirdEntry, 'fetch', 'success');
    state(a, 'ready', third.value);
    state(b, 'error', null, error);
  });
});

for (const phase of ['fetch', 'decode']) {
  for (const newerState of ['none', 'loading', 'ready', 'error']) {
    test(`actual abort rejection during ${phase}, newer ${newerState}`, async () => {
      await withControlledCalls(async scope => {
        const loader = new PreviewLoader(), displayed = await seed(scope, loader);
        const controller = new AbortController(), reason = {}, key = {}, bytes = {};
        const fetch = scope.call(), decode = scope.call();
        let listener;
        const abortable = callback => (arg, signal) => {
          const promise = callback(arg, signal);
          const entry = callback.calls.at(-1);
          listener = () => entry.fail(signal.reason);
          signal.addEventListener('abort', listener, { once: true });
          return promise;
        };
        try {
          const task = scope.run(() => loader.load(key,
            phase === 'fetch' ? abortable(fetch) : fetch,
            phase === 'decode' ? abortable(decode) : decode, controller.signal));
          const request = { fetch, decode, key, bytes, signal: controller.signal };
          const entry = await fetchEntry(request);
          if (phase === 'decode') {
            entry.complete(bytes);
            await decodeEntry(request);
          }
          let newest, pending;
          const newError = {};
          if (newerState !== 'none') {
            newest = begin(scope, loader);
            pending = await fetchEntry(newest);
            if (newerState !== 'loading') {
              await finish(scope, newest, pending, 'fetch', newerState === 'ready' ? 'success' : 'failure', newError);
            }
          }
          const protectedState = loader.state;
          assert.equal(controller.signal.aborted, false);
          controller.abort(reason);
          await assert.rejects(scope.wait(task), error => error === reason);
          if (phase === 'fetch') assert.equal(decode.calls.length, 0);
          if (newerState === 'none') {
            state(loader, 'error', displayed, reason);
            const recovery = begin(scope, loader);
            await finish(scope, recovery, await fetchEntry(recovery), 'fetch', 'success');
            state(loader, 'ready', recovery.value);
          } else {
            assert.equal(loader.state, protectedState);
            if (newerState === 'loading') {
              await finish(scope, newest, pending, 'fetch', 'success');
              state(loader, 'ready', newest.value);
            } else {
              state(loader, newerState, newerState === 'ready' ? newest.value : displayed, newerState === 'error' ? newError : null);
            }
          }
        } finally {
          if (listener) controller.signal.removeEventListener('abort', listener);
        }
      });
    });
  }
}

for (const phase of ['fetch', 'decode']) {
  test(`abort during ${phase} leaves ignoring callbacks under caller control`, async () => {
    await withControlledCalls(async scope => {
      const loader = new PreviewLoader(), controller = new AbortController();
      const request = begin(scope, loader, {}, controller.signal);
      let entry = await fetchEntry(request);
      if (phase === 'decode') {
        entry.complete(request.bytes);
        entry = await decodeEntry(request);
      }
      controller.abort({});
      state(loader, 'loading', null);
      await finish(scope, request, entry, phase, 'success');
      state(loader, 'ready', request.value);
    });
  });
}
