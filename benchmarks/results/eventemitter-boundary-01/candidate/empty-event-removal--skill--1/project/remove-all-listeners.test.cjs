const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');

for (const count of [0, 1, 2]) {
  test(`removing an empty-string event with ${count} listeners preserves other events`, () => {
    const e = new E(), symbol = Symbol('event'), seen = [];
    const stringListener = () => seen.push('string');
    const symbolListener = () => seen.push(symbol);
    e.on('other', stringListener).on(symbol, symbolListener);
    for (let i = 0; i < count; i++) e.on('', () => assert.fail('removed listener ran'));
    assert.equal(e.listenerCount(''), count);

    assert.equal(e.removeAllListeners(''), e);
    assert.equal(e.removeAllListeners(''), e);
    assert.deepEqual(e.eventNames(), ['other', symbol]);
    assert.equal(e.listenerCount(''), 0);
    assert.deepEqual(e.listeners(''), []);
    assert.equal(e.emit(''), false);
    assert.equal(e.listenerCount('other'), 1);
    assert.equal(e.listenerCount(symbol), 1);
    assert.deepEqual(e.listeners('other'), [stringListener]);
    assert.deepEqual(e.listeners(symbol), [symbolListener]);
    assert.equal(e.emit('other'), true);
    assert.equal(e.emit(symbol), true);
    assert.deepEqual(seen, ['string', symbol]);
  });
}

test('removing the sole empty-string event leaves a reusable emitter', () => {
  const e = new E(), listener = () => {};
  assert.equal(e.removeAllListeners(''), e);
  e.on('', listener);
  assert.equal(e.removeAllListeners(''), e);
  assert.deepEqual(e.eventNames(), []);
  assert.equal(e.listenerCount(''), 0);
  assert.equal(e.removeAllListeners(''), e);
  e.on('', listener);
  assert.deepEqual(e.eventNames(), ['']);
  assert.equal(e.listenerCount(''), 1);
  assert.deepEqual(e.listeners(''), [listener]);
  assert.equal(e.emit(''), true);
});

for (const args of [[], [undefined]]) {
  test(`removeAllListeners with ${args.length ? 'undefined' : 'no argument'} clears every event`, () => {
    const e = new E(), symbol = Symbol('event');
    const events = ['', 'other', symbol];
    for (const event of events) e.on(event, () => assert.fail('removed listener ran'));
    assert.equal(e.removeAllListeners(...args), e);
    assert.deepEqual(e.eventNames(), []);
    for (const event of events) {
      assert.equal(e.listenerCount(event), 0);
      assert.deepEqual(e.listeners(event), []);
      assert.equal(e.emit(event), false);
    }
  });
}

test('specific string and symbol removal preserves the empty-string event', () => {
  const e = new E(), symbol = Symbol('event'), listener = () => {};
  e.on('', listener).on('other', listener).on(symbol, listener);
  assert.equal(e.removeAllListeners('other'), e);
  assert.deepEqual(e.eventNames(), ['', symbol]);
  assert.equal(e.listenerCount('other'), 0);
  assert.equal(e.removeAllListeners(symbol), e);
  assert.deepEqual(e.eventNames(), ['']);
  assert.equal(e.listenerCount(symbol), 0);
  assert.equal(e.listenerCount(''), 1);
  assert.equal(e.emit(''), true);
});
