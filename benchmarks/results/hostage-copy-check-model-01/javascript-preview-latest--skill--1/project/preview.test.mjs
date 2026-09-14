import assert from 'node:assert/strict';
import test from 'node:test';
import { PreviewLoader } from './preview.mjs';

test('forwards both stages and preserves the returned value', async () => {
  const loader = new PreviewLoader(), key = {}, bytes = {}, value = {};
  const signal = new AbortController().signal;
  assert.equal(await loader.load(key, (received, passed) => {
    assert.equal(received, key); assert.equal(passed, signal); return bytes;
  }, (received, passed) => {
    assert.equal(received, bytes); assert.equal(passed, signal); return value;
  }, signal), value);
});

test('propagates failure from either stage by identity', async () => {
  const loader = new PreviewLoader(), reason = new Error('stage failed');
  await assert.rejects(loader.load('x', async () => { throw reason; }, () => assert.fail('decode after failed fetch')), error => error === reason);
  await assert.rejects(loader.load('x', () => ({}), async () => { throw reason; }), error => error === reason);
});
