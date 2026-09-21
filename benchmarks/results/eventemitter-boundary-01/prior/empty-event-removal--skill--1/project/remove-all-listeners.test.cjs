const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');

for (const emptyListeners of [0, 1, 2]) {
  test(`removing an empty-string event with ${emptyListeners} listeners preserves other events`, () => {
    const e = new E(), symbol = Symbol('event'), seen = [];
    const empty = () => assert.fail('removed listener fired');
    const stringListener = () => seen.push('string');
    const symbolListener = () => seen.push(symbol);
    e.on('other', stringListener).on(symbol, symbolListener);
    for (let i = 0; i < emptyListeners; i++) e.on('', empty);
    assert.equal(e.listenerCount(''), emptyListeners);

    for (let i = 0; i < 2; i++) {
      assert.equal(e.removeAllListeners(''), e);
      assert.deepEqual(e.eventNames(), ['other', symbol]);
      assert.equal(e.listenerCount(''), 0);
      assert.deepEqual(e.listeners(''), []);
      assert.equal(e.emit(''), false);
      assert.equal(e.listenerCount('other'), 1);
      assert.equal(e.listenerCount(symbol), 1);
      assert.deepEqual(e.listeners('other'), [stringListener]);
      assert.deepEqual(e.listeners(symbol), [symbolListener]);
    }
    assert.equal(e.emit('other'), true);
    assert.equal(e.emit(symbol), true);
    assert.deepEqual(seen, ['string', symbol]);
    assert.equal(e.removeAllListeners('other'), e);
    assert.deepEqual(e.eventNames(), [symbol]);
    assert.equal(e.removeAllListeners(symbol), e);
    assert.deepEqual(e.eventNames(), []);
  });
}

test('removing the last empty-string event permits reuse', () => {
  const e = new E(), listener = () => {};
  e.on('', listener);
  assert.equal(e.removeAllListeners(''), e);
  assert.deepEqual(e.eventNames(), []);
  assert.equal(e.listenerCount(''), 0);
  assert.equal(e.removeAllListeners(''), e);
  assert.equal(e.on('', listener), e);
  assert.deepEqual(e.eventNames(), ['']);
  assert.equal(e.listenerCount(''), 1);
  assert.equal(e.emit(''), true);
});

for (const args of [[], [undefined]]) {
  test(`removeAllListeners with ${args.length ? 'undefined' : 'no argument'} clears all events`, () => {
    const e = new E(), symbol = Symbol('event');
    const names = ['', 'other', symbol];
    for (const name of names) e.on(name, () => assert.fail('removed listener fired'));
    assert.equal(e.removeAllListeners(...args), e);
    assert.deepEqual(e.eventNames(), []);
    for (const name of names) {
      assert.equal(e.listenerCount(name), 0);
      assert.deepEqual(e.listeners(name), []);
      assert.equal(e.emit(name), false);
    }
    assert.equal(e.removeAllListeners(...args), e);
    e.on('reused', () => {});
    assert.deepEqual(e.eventNames(), ['reused']);
    assert.equal(e.listenerCount('reused'), 1);
  });
}
