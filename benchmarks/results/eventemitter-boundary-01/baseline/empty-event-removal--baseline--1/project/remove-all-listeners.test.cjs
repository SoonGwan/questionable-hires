const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');

test('removing empty-string listeners preserves other string and symbol events', () => {
  const e = new E();
  const symbol = Symbol('event');
  const seen = [];
  const empty = () => seen.push('empty');
  const ordinary = () => seen.push('ordinary');
  const symbolic = () => seen.push('symbol');
  e.on('', empty).once('', empty).on('ordinary', ordinary).on(symbol, symbolic);

  assert.equal(e.listenerCount(''), 2);
  assert.equal(e.removeAllListeners(''), e);
  assert.deepEqual(e.eventNames(), ['ordinary', symbol]);
  assert.equal(e.listenerCount(''), 0);
  assert.deepEqual(e.listeners(''), []);
  assert.equal(e.emit(''), false);
  for (const [event, listener] of [['ordinary', ordinary], [symbol, symbolic]]) {
    assert.equal(e.listenerCount(event), 1);
    assert.deepEqual(e.listeners(event), [listener]);
    assert.equal(e.emit(event), true);
  }
  assert.deepEqual(seen, ['ordinary', 'symbol']);

  assert.equal(e.removeAllListeners('ordinary'), e);
  assert.deepEqual(e.eventNames(), [symbol]);
  assert.equal(e.listenerCount('ordinary'), 0);
  assert.equal(e.removeAllListeners(symbol), e);
  assert.deepEqual(e.eventNames(), []);
  assert.equal(e.listenerCount(symbol), 0);
});

test('removing an absent empty-string event is a fluent no-op', () => {
  const e = new E();
  const symbol = Symbol('event');
  const listener = () => {};
  assert.equal(e.removeAllListeners(''), e);
  assert.deepEqual(e.eventNames(), []);
  e.on('ordinary', listener).on(symbol, listener);
  for (let i = 0; i < 2; i++) {
    assert.equal(e.removeAllListeners(''), e);
    assert.deepEqual(e.eventNames(), ['ordinary', symbol]);
    assert.equal(e.listenerCount(''), 0);
    for (const event of ['ordinary', symbol]) {
      assert.equal(e.listenerCount(event), 1);
      assert.deepEqual(e.listeners(event), [listener]);
      assert.equal(e.emit(event), true);
    }
  }
});

test('removing the sole empty-string event allows subsequent registration', () => {
  const e = new E();
  const listener = () => {};
  e.on('', listener);
  assert.equal(e.removeAllListeners(''), e);
  assert.deepEqual(e.eventNames(), []);
  assert.equal(e.listenerCount(''), 0);
  assert.equal(e.emit(''), false);
  assert.equal(e.on('', listener), e);
  assert.deepEqual(e.eventNames(), ['']);
  assert.equal(e.listenerCount(''), 1);
  assert.equal(e.emit(''), true);
});

for (const args of [[], [undefined]]) {
  test(`removeAllListeners with ${args.length ? 'undefined' : 'no argument'} clears all events`, () => {
    const e = new E();
    const symbol = Symbol('event');
    const listener = () => {};
    const events = ['', 'ordinary', symbol];
    for (const event of events) e.on(event, listener).once(event, listener);
    assert.equal(e.removeAllListeners(...args), e);
    assert.deepEqual(e.eventNames(), []);
    for (const event of events) {
      assert.equal(e.listenerCount(event), 0);
      assert.deepEqual(e.listeners(event), []);
      assert.equal(e.emit(event), false);
    }
    assert.equal(e.on('new', listener), e);
    assert.deepEqual(e.eventNames(), ['new']);
    assert.equal(e.listenerCount('new'), 1);
  });
}
