import assert from 'node:assert/strict';
import test from 'node:test';
import { SubmitPanel } from './panel.mjs';

test('preserves result and signal identity', async () => {
  const panel = new SubmitPanel(), signal = new AbortController().signal, result = {};
  assert.equal(await panel.submit(async received => { assert.equal(received, signal); return result; }, signal), result);
});

test('preserves callback rejection identity', async () => {
  const error = new Error('save failed');
  await assert.rejects(new SubmitPanel().submit(async () => { throw error; }), reason => reason === error);
});
