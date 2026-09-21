"""Author-selected changes to pinned upstream source; no model execution here."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'benchmarks/fixtures/eventemitter3-5.0.1'
HASHES = {'index.js': '1560f251de5d28d2c15ff070215d2c5c0fa06f1a92e8d6522bbee37e06d2a6b5',
          'LICENSE': '3aecc12b1cb28832b5f65ab64291de96568c3f236a74d646281b4491f7bcadbf'}

EXISTING = '''const test = require('node:test');
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
'''

REENTRY_ORACLE = '''const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');
test('earlier listener re-entry consumes once only once', () => {
  const e = new E(); let entered = false, hits = 0;
  e.on('x', () => { if (!entered) { entered = true; e.emit('x'); } });
  e.once('x', () => hits++);
  e.emit('x'); assert.equal(hits, 1);
});
test('nested single-listener path updates the outer snapshot', () => {
  const e = new E(); let hits = 0;
  function earlier() { e.off('x', earlier); e.emit('x'); }
  e.on('x', earlier); e.once('x', () => hits++);
  e.emit('x'); assert.equal(hits, 1); assert.equal(e.listenerCount('x'), 0);
});
test('throwing nested once stays consumed and preserves exact error', () => {
  const e = new E(), error = new Error('once failure'); let nested = false, hits = 0;
  e.on('x', () => {
    if (!nested) {
      nested = true;
      assert.throws(() => e.emit('x'), actual => actual === error);
    }
  });
  e.once('x', () => { hits++; throw error; });
  assert.equal(e.emit('x'), true); assert.equal(hits, 1);
});
test('duplicates, contexts, symbols, instances and variadic payloads', () => {
  const e = new E(), other = new E(), name = Symbol('x'), a = {}, b = {}, value = {};
  const seen = [];
  function f(...args) { seen.push([this, args]); }
  e.once(name, f, a); e.once(name, f, b); other.once(name, f, a);
  e.emit(name, value, 2, 3, 4, 5, 6, 7); other.emit(name, value);
  assert.equal(seen.length, 3); assert.equal(seen[0][0], a); assert.equal(seen[1][0], b);
  assert.deepEqual(seen[0][1], [value, 2, 3, 4, 5, 6, 7]);
  assert.equal(seen[0][1][0], value); assert.equal(e.emit(name), false);
  e.once(name, f, b); e.emit(name, value); assert.equal(seen.length, 4);
});
test('ordinary snapshot removal and additions retain existing behavior', () => {
  const e = new E(), seen = [];
  function old() { seen.push('old'); }
  function added() { seen.push('added'); }
  e.on('x', () => { seen.push('first'); e.off('x', old); e.on('x', added); });
  e.on('x', old); e.emit('x');
  assert.deepEqual(seen, ['first', 'old']);
  seen.length = 0; e.emit('x'); assert.deepEqual(seen, ['first', 'added']);
});
'''

EMPTY_ORACLE = '''const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('./index.js');
test('empty name removes only that event and preserves other registrations', () => {
  const e = new E(), symbol = Symbol('keep'), fn = () => {};
  e.on('', fn); e.on('', fn); e.once('keep', fn); e.on(symbol, fn);
  assert.equal(e.removeAllListeners(''), e);
  assert.equal(e.listenerCount(''), 0); assert.equal(e.listenerCount('keep'), 1);
  assert.equal(e.listenerCount(symbol), 1); assert.equal(e._eventsCount, 2);
  assert.deepEqual(e.eventNames(), ['keep', symbol]);
  e.removeAllListeners(''); assert.equal(e._eventsCount, 2);
});
test('absent empty name is no-op; undefined/no arguments still clear all', () => {
  const e = new E(), fn = () => {};
  e.on('keep', fn); e.removeAllListeners(''); assert.equal(e.listenerCount('keep'), 1);
  e.removeAllListeners(undefined); assert.deepEqual(e.eventNames(), []);
  e.on('', fn); e.on('keep', fn); e.removeAllListeners();
  assert.equal(e._eventsCount, 0); assert.deepEqual(e.eventNames(), []);
  e.on('fresh', fn); assert.equal(e.emit('fresh'), true);
});
'''


def files():
    result = {}
    for name, expected in HASHES.items():
        data = (SOURCE / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Upstream source identity changed: ' + name)
        result[name] = data.decode()
    result['existing.test.cjs'] = EXISTING
    result['AGENTS.md'] = ('Use Node and `node --test *.test.cjs` in this root. '
        'Keep existing tests and license unchanged; add native regression tests. '
        'Implementation changes belong in index.js. No dependencies, network, '
        'commits, declarations/build changes or unrelated refactoring.\n')
    return result


def cases():
    common = ' Preserve the supplied existing tests and license; add native regression assertions and run them. No commits or publication.'
    return [dict(id='once-reentrant-dispatch', skill='hostage-negotiator', files=files(),
        task='Fix once-listener dispatch in this EventEmitter3 source excerpt. If an earlier listener recursively emits the same event, each once registration must be invoked at most once across the overlapping dispatches, including when the nested call sees only one remaining listener or throws. Preserve ordinary listener snapshot behavior, distinct duplicate registrations, contexts, payload/error identity, symbols, instance isolation and existing emit return values. Re-registering a consumed listener must work.' + common,
        criteria=[
            'Once registrations execute at most once across reentrant single/multiple-listener dispatch paths.',
            'Throwing once listeners remain consumed with exact error propagation; fresh registrations still work.',
            'Preserves duplicate registrations, contexts, symbols, payloads, instance isolation, ordinary snapshots and emit results.',
            'Meaningful native assertions exercise the delivered local emitter and preserve existing tests.',
            'Scoped edits, preserved license/instructions and final report consistent with original execution.']),
        dict(id='empty-event-removal', skill='hostage-negotiator', files=files(),
        task='Fix removeAllListeners in this EventEmitter3 source excerpt so an empty-string event name is a specific event, not a request to remove all events. Other string and symbol events must remain registered; removing an absent empty event is a no-op. Calls with no argument or undefined must still remove all events. Preserve fluent returns, eventNames/listenerCount consistency and the other APIs.' + common,
        criteria=[
            'Empty-string removal affects only that event, including multiple registrations.',
            'Absent empty event is a no-op; no-argument and undefined removal still clear all events.',
            'Preserves string/symbol siblings, fluent returns, counts, eventNames and reuse after clearing.',
            'Meaningful native assertions exercise the delivered local emitter and preserve existing tests.',
            'Scoped edits, preserved license/instructions and final report consistent with original execution.'])]


def corrected(source, task, partial=False):
    if task == 'empty-event-removal':
        assert source.count('if (event) {') == 1
        return source.replace('if (event) {', "if (event || event === '') {")
    single = 'if (listeners.once) this.removeListener(event, listeners.fn, undefined, true);'
    multi = 'if (listeners[i].once) this.removeListener(event, listeners[i].fn, undefined, true);'
    assert source.count(single) == source.count(multi) == 1
    if not partial:
        source = source.replace(single, '''if (listeners.once) {
      if (listeners.fired) return true;
      listeners.fired = true;
      this.removeListener(event, listeners.fn, undefined, true);
    }''')
    return source.replace(multi, '''if (listeners[i].once) {
        if (listeners[i].fired) continue;
        listeners[i].fired = true;
        this.removeListener(event, listeners[i].fn, undefined, true);
      }''')


def preflight():
    initial = files()
    observations = []
    for task, oracle in [('once-reentrant-dispatch', REENTRY_ORACLE), ('empty-event-removal', EMPTY_ORACLE)]:
        variants = [('upstream', initial['index.js'], 1),
                    ('corrected', corrected(initial['index.js'], task), 0)]
        if task == 'once-reentrant-dispatch':
            variants.append(('partial-multi-path-only', corrected(initial['index.js'], task, partial=True), 1))
        for variant, source, expected in variants:
            with tempfile.TemporaryDirectory(prefix='qh-emitter-control-') as folder:
                project = Path(folder)
                for name, body in initial.items(): (project / name).write_text(body)
                (project / 'index.js').write_text(source)
                (project / 'contract.test.cjs').write_text(oracle)
                proc = subprocess.run([shutil.which('node'), '--test', 'existing.test.cjs', 'contract.test.cjs'],
                    cwd=project, text=True, capture_output=True, timeout=15)
                if proc.returncode != expected or (expected and 'AssertionError' not in proc.stdout):
                    raise AssertionError((task, variant, proc.returncode, proc.stdout, proc.stderr))
                observations.append(dict(task=task, variant=variant, exit_code=proc.returncode,
                    source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                    output=proc.stdout.replace(folder, '<CONTROL>'), stderr=proc.stderr.replace(folder, '<CONTROL>')))
    return observations


if __name__ == '__main__':
    import json
    print(json.dumps(preflight(), indent=2))
