const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');

for (const single of [false, true]) {
  for (let arity = 0; arity <= 6; arity++) {
    test(`recursive once dispatch: ${single ? 'single' : 'array'} nested path, ${arity} arguments`, () => {
      const e = new E(), event = Symbol('event'), context = {};
      const outer = Array.from({ length: arity }, () => ({}));
      const nested = Array.from({ length: arity }, () => ({}));
      const seen = [];
      let recursing = false;
      function earlier() {
        if (recursing) return;
        recursing = true;
        if (single) e.removeListener(event, earlier);
        assert.equal(e.emit(event, ...nested), true);
      }
      e.on(event, earlier);
      e.once(event, function (...args) { seen.push([this, args]); }, context);
      assert.equal(e.emit(event, ...outer), true);
      assert.equal(seen.length, 1);
      assert.equal(seen[0][0], context);
      assert.equal(seen[0][1].length, arity);
      nested.forEach((value, i) => assert.equal(seen[0][1][i], value));
      assert.equal(e.listenerCount(event), single ? 0 : 1);
      assert.equal(e.emit(event), !single);
      assert.equal(seen.length, 1);
    });
  }
}

for (const single of [false, true]) {
  for (const caught of [false, true]) {
    test(`throwing nested once: ${single ? 'single' : 'array'} path, ${caught ? 'caught' : 'propagated'}`, () => {
      const e = new E(), error = {}, payload = {}, context = {}, seen = [];
      let recursing = false;
      function earlier() {
        if (recursing) return;
        recursing = true;
        if (single) e.removeListener('event', earlier);
        if (caught) assert.throws(() => e.emit('event', payload), value => value === error);
        else e.emit('event', payload);
      }
      e.on('event', earlier);
      e.once('event', function (value) {
        assert.equal(this, context);
        assert.equal(value, payload);
        seen.push(value);
        throw error;
      }, context);
      if (caught) assert.equal(e.emit('event', payload), true);
      else assert.throws(() => e.emit('event', payload), value => value === error);
      assert.deepEqual(seen, [payload]);
      assert.equal(e.listenerCount('event'), single ? 0 : 1);
      assert.equal(e.emit('event', payload), !single);
      assert.deepEqual(seen, [payload]);
    });
  }
}

test('duplicate once registrations remain distinct during recursion, including contexts', () => {
  const e = new E(), first = {}, second = {}, outer = {}, nested = {}, seen = [];
  function listener(value) {
    seen.push([this, value]);
    if (seen.length === 1) {
      assert.equal(e.listenerCount('event'), 2);
      assert.equal(e.emit('event', nested), true);
    }
  }
  e.once('event', listener, first);
  e.once('event', listener, first);
  e.once('event', listener, second);
  assert.equal(e.emit('event', outer), true);
  assert.equal(seen.length, 3);
  for (const [i, context, value] of [[0, first, outer], [1, first, nested], [2, second, nested]]) {
    assert.equal(seen[i][0], context);
    assert.equal(seen[i][1], value);
  }
  assert.deepEqual(e.eventNames(), []);
  assert.equal(e.emit('event'), false);
});

test('re-registering a consumed callback survives stale snapshots and thrown calls', () => {
  const e = new E(), error = {}, outer = {}, nested = {}, later = {}, seen = [];
  function listener(value) {
    assert.equal(this, e);
    seen.push(value);
    if (seen.length === 1) {
      e.once('event', listener);
      throw error;
    }
  }
  function earlier() {
    e.removeListener('event', earlier);
    assert.throws(() => e.emit('event', nested), value => value === error);
  }
  e.on('event', earlier);
  e.once('event', listener);
  assert.equal(e.emit('event', outer), true);
  assert.deepEqual(seen, [nested]);
  assert.equal(seen[0], nested);
  assert.deepEqual(e.listeners('event'), [listener]);
  assert.equal(e.emit('event', later), true);
  assert.deepEqual(seen, [nested, later]);
  assert.equal(seen[1], later);
  assert.equal(e.emit('event'), false);
});

test('a throwing duplicate leaves unconsumed registrations available', () => {
  const e = new E(), error = {}, seen = [];
  function listener(value) {
    seen.push(value);
    if (seen.length === 1) throw error;
  }
  e.once('event', listener);
  e.once('event', listener);
  assert.throws(() => e.emit('event', 'first'), value => value === error);
  assert.deepEqual(e.listeners('event'), [listener]);
  assert.equal(e.emit('event', 'second'), true);
  assert.deepEqual(seen, ['first', 'second']);
  assert.equal(e.emit('event'), false);
});

test('removal and addition preserve the active listener snapshot', () => {
  const e = new E(), seen = [];
  function ordinary(value) { seen.push(['ordinary', value]); }
  function once(value) { seen.push(['once', value]); }
  function added(value) { seen.push(['added', value]); }
  e.on('event', () => {
    e.removeAllListeners('event');
    e.on('event', added);
  });
  e.on('event', ordinary);
  e.once('event', once);
  assert.equal(e.emit('event', 'outer'), true);
  assert.deepEqual(seen, [['ordinary', 'outer'], ['once', 'outer']]);
  assert.deepEqual(e.listeners('event'), [added]);
  assert.equal(e.emit('event', 'later'), true);
  assert.deepEqual(seen, [['ordinary', 'outer'], ['once', 'outer'], ['added', 'later']]);
});

test('ordinary listeners still run in both overlapping snapshots', () => {
  const e = new E(), seen = [];
  e.once('event', () => {
    assert.equal(e.emit('event', 'nested'), true);
  });
  e.on('event', value => seen.push(['ordinary', value]));
  e.once('event', value => seen.push(['once', value]));
  assert.equal(e.emit('event', 'outer'), true);
  assert.deepEqual(seen, [['ordinary', 'nested'], ['once', 'nested'], ['ordinary', 'outer']]);
});

test('consumption belongs to a registration, not its callback, event or emitter', () => {
  const a = new E(), b = new E(), event = Symbol('event'), other = Symbol('event'), seen = [];
  function listener(value) { seen.push([this, value]); }
  a.once(event, () => {
    assert.equal(a.emit(event, 'nested'), true);
    assert.equal(b.emit(event, 'other emitter'), true);
    assert.equal(a.emit(other, 'other event'), true);
  });
  a.once(event, listener);
  a.once(other, listener);
  b.once(event, listener);
  assert.equal(a.emit(event, 'outer'), true);
  assert.deepEqual(seen, [[a, 'nested'], [b, 'other emitter'], [a, 'other event']]);
  assert.equal(seen[0][0], a);
  assert.equal(seen[1][0], b);
  assert.equal(seen[2][0], a);
  assert.deepEqual(a.eventNames(), []);
  assert.deepEqual(b.eventNames(), []);
  a.once(event, listener);
  assert.equal(a.emit(event, 'registered again'), true);
  assert.equal(seen.length, 4);
  assert.equal(seen[3][0], a);
  assert.equal(seen[3][1], 'registered again');
});
