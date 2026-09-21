"""Supplementary author probe; never substitutes for original model evidence."""
import hashlib
from pathlib import Path
import shutil
import subprocess

PROBE = r'''
const assert = require('node:assert/strict');
const source = process.argv[1];
assert.equal(require.resolve(source), source);
const E = require(source), e = new E(), error = new Error('first duplicate');
let calls = 0;
function listener() { if (++calls === 1) throw error; }
e.once('x', listener); e.once('x', listener);
assert.throws(() => e.emit('x'), actual => actual === error);
const remaining = e.listenerCount('x');
const secondEmit = e.emit('x');
console.log(JSON.stringify({remaining, secondEmit, calls}));
assert.equal(remaining, 1, 'Throwing registration removed an unconsumed duplicate');
assert.equal(secondEmit, true);
assert.equal(calls, 2);
assert.equal(e.emit('x'), false);
'''


def observe(source):
    source = Path(source).resolve()
    result = subprocess.run([shutil.which('node'), '-e', PROBE, str(source)],
        text=True, capture_output=True, timeout=10)
    return dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        probe_sha256=hashlib.sha256(PROBE.encode()).hexdigest(), exit_code=result.returncode,
        output=result.stdout.replace(str(source), '<SOURCE>'),
        stderr=result.stderr.replace(str(source), '<SOURCE>'))
