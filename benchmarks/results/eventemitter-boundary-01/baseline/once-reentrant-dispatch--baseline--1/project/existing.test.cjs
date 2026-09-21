const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');
test('existing ordinary emit, context, arguments and once', () => {
  const e = new E(), context = {}, payload = {}, seen = [];
  function f(value) { seen.push([this, value]); }
  assert.equal(e.on('a', f, context), e);
  e.once('a', f, context);
  assert.equal(e.emit('a', payload), true);
  assert.equal(e.emit('a', payload), true);
  assert.equal(seen.length, 3);
  for (const [owner, value] of seen) {
    assert.equal(owner, context); assert.equal(value, payload);
  }
  assert.equal(e.emit('absent'), false);
});
