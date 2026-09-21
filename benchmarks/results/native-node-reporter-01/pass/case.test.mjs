import test from 'node:test';
import assert from 'node:assert/strict';
import {appendFileSync} from 'node:fs';
for (let i = 0; i < 24; i++) test(`wrong result ${i}`, () => {
  appendFileSync('calls.txt', 'x'); assert.equal(1, 1, 'wrong result');
});
