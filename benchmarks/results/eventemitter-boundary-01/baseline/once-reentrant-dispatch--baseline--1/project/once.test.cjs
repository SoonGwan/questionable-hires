'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');

for (const event of ['event', Symbol('event')]) {
  for (const single of [false, true]) {
    for (let arity = 0; arity <= 7; arity++) {
      test(`recursive once: ${String(event)}, single=${single}, arity=${arity}`, () => {
        const e = new E(), context = {}, calls = [];
        const outer = Array.from({ length: arity }, () => ({}));
        const inner = Array.from({ length: arity }, () => ({}));
        let nested = false;
        function earlier() {
          if (nested) return;
          nested = true;
          if (single) e.off(event, earlier);
          assert.equal(e.emit(event, ...inner), true);
        }
        e.on(event, earlier);
        e.once(event, function (...args) {
          assert.equal(this, context);
          args.forEach((arg, i) => assert.equal(arg, inner[i]));
          assert.equal(args.length, arity);
          calls.push(args);
        }, context);
        assert.equal(e.emit(event, ...outer), true);
        assert.equal(calls.length, 1);
        assert.equal(e.listenerCount(event), single ? 0 : 1);
        assert.equal(e.emit(event, ...outer), !single);
        assert.equal(calls.length, 1);
      });
    }
  }
}

for (const single of [false, true]) {
  for (const caught of [false, true]) {
    test(`throwing nested once: single=${single}, caught=${caught}`, () => {
      const e = new E(), error = {}, payload = {};
      let nested = false, calls = 0;
      function earlier() {
        if (nested) return;
        nested = true;
        if (single) e.off('event', earlier);
        if (caught) assert.throws(() => e.emit('event', payload), value => value === error);
        else e.emit('event', payload);
      }
      e.on('event', earlier);
      e.once('event', value => {
        calls++;
        assert.equal(value, payload);
        throw error;
      });
      if (caught) assert.equal(e.emit('event'), true);
      else assert.throws(() => e.emit('event'), value => value === error);
      assert.equal(calls, 1);
      assert.equal(e.emit('event'), !single);
      assert.equal(calls, 1);
    });
  }
}

test('duplicate once registrations retain their contexts and recursive turn', () => {
  const e = new E(), a = {}, b = {}, outer = {}, inner = {}, calls = [];
  function listener(payload) {
    calls.push([this, payload]);
    if (calls.length === 1) {
      assert.equal(e.listenerCount('event'), 2);
      assert.equal(e.emit('event', inner), true);
    }
  }
  e.once('event', listener, a);
  e.once('event', listener, a);
  e.once('event', listener, b);
  assert.equal(e.emit('event', outer), true);
  assert.deepEqual(calls, [[a, outer], [a, inner], [b, inner]]);
  calls.forEach(([context, payload], i) => {
    assert.equal(context, i === 2 ? b : a);
    assert.equal(payload, i === 0 ? outer : inner);
  });
  assert.equal(e.emit('event'), false);
  assert.deepEqual(e.eventNames(), []);
});

test('a throwing duplicate leaves the other registration available', () => {
  const e = new E(), error = new Error('once');
  let calls = 0;
  function listener() { if (++calls === 1) throw error; }
  e.once('event', listener);
  e.once('event', listener);
  assert.throws(() => e.emit('event'), value => value === error);
  assert.equal(e.listenerCount('event'), 1);
  assert.equal(e.emit('event'), true);
  assert.equal(calls, 2);
  assert.equal(e.emit('event'), false);
});

test('consumed listeners can register again during overlapping dispatch', () => {
  const e = new E();
  let nested = false, calls = 0;
  e.on('event', () => {
    if (!nested) {
      nested = true;
      e.emit('event');
    }
  });
  function listener() {
    assert.equal(this, e);
    if (++calls === 1) e.once('event', listener);
  }
  e.once('event', listener);
  assert.equal(e.emit('event'), true);
  assert.equal(calls, 1);
  assert.equal(e.listenerCount('event'), 2);
  assert.equal(e.emit('event'), true);
  assert.equal(calls, 2);
  assert.equal(e.listenerCount('event'), 1);
});

test('removal and addition preserve ordinary dispatch snapshots', () => {
  const e = new E(), calls = [];
  function added() { calls.push('added'); }
  e.on('event', () => {
    calls.push('earlier');
    e.removeAllListeners('event');
    e.on('event', added);
  });
  e.on('event', () => calls.push('ordinary'));
  e.once('event', () => calls.push('once'));
  assert.equal(e.emit('event'), true);
  assert.deepEqual(calls, ['earlier', 'ordinary', 'once']);
  assert.deepEqual(e.listeners('event'), [added]);
  assert.equal(e.emit('event'), true);
  assert.deepEqual(calls, ['earlier', 'ordinary', 'once', 'added']);
});

test('shared callbacks remain independent across events, instances and ordinary listeners', () => {
  const a = new E(), b = new E(), event = Symbol('event'), calls = [];
  function listener() { calls.push(this); }
  a.once(event, listener);
  a.on(event, listener);
  a.once('other', listener);
  b.once(event, listener);
  assert.equal(a.emit(event), true);
  assert.equal(a.emit(event), true);
  assert.equal(a.emit('other'), true);
  assert.equal(b.emit(event), true);
  assert.deepEqual(calls, [a, a, a, a, b]);
  assert.equal(b.emit(event), false);
  assert.equal(a.emit('other'), false);
  assert.deepEqual(a.eventNames(), [event]);
});
