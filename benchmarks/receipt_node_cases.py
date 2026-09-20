"""Two authored Node comparison tasks; independent native controls, no model calls."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import run

ROOT = Path(__file__).resolve().parents[1]
BODY = '''class Decoder {
  constructor() { this.pending = Buffer.alloc(0); }
  push(chunk) {
    this.pending = Buffer.concat([this.pending, chunk]);
    const frames = [];
    while (this.pending.length >= 2) {
      const size = this.pending.readUInt16BE(0);
      this.pending = this.pending.subarray(2);
      if (this.pending.length < size) break;
      frames.push(Buffer.from(this.pending.subarray(0, size)));
      this.pending = this.pending.subarray(size);
    }
    return frames;
  }
}
'''
FIXED = BODY.replace('''      this.pending = this.pending.subarray(2);
      if (this.pending.length < size) break;''', '''      if (this.pending.length < 2 + size) break;
      this.pending = this.pending.subarray(2);''')
ASSERTIONS = '''import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
LOAD
console.log('ACTUAL_MODULE ' + JSON.stringify({path:fileURLToPath(component.origin), pid:process.pid}));
const encode = body => { const prefix = Buffer.alloc(2); prefix.writeUInt16BE(body.length); return Buffer.concat([prefix, body]); };
const hex = frames => frames.map(frame => frame.toString('hex'));
test('split header', () => {
  const d = new component.Decoder(), frame = encode(Buffer.from('hi'));
  assert.deepEqual(hex(d.push(frame.subarray(0, 1))), []);
  assert.deepEqual(hex(d.push(frame.subarray(1))), ['6869']);
});
test('split binary payload', () => {
  const d = new component.Decoder(), frame = encode(Buffer.from([0, 255, 13, 10]));
  assert.deepEqual(hex(d.push(frame.subarray(0, 3))), []);
  assert.deepEqual(hex(d.push(frame.subarray(3))), ['00ff0d0a']);
});
test('coalesced frames', () => {
  const d = new component.Decoder();
  assert.deepEqual(hex(d.push(Buffer.concat([encode(Buffer.from('a')), encode(Buffer.from('bc'))]))), ['61', '6263']);
});
test('empty frame and empty input', () => {
  const d = new component.Decoder();
  assert.deepEqual(hex(d.push(Buffer.alloc(0))), []);
  assert.deepEqual(hex(d.push(encode(Buffer.alloc(0)))), ['']);
  assert.deepEqual(hex(d.push(Buffer.alloc(0))), []);
});
'''


def build_cases():
    rows = []
    for mode in ('esm-committed', 'cjs-working'):
        esm = mode.startswith('esm')
        name = 'decoder.mjs' if esm else 'decoder.cjs'
        tail = ('export { Decoder };\nexport const origin = import.meta.url;\n' if esm else
                "exports.Decoder = Decoder;\nexports.origin = require('node:url').pathToFileURL(__filename).href;\n")
        before, after = BODY + tail, FIXED + tail
        loader = ("import * as component from '../decoder.mjs';" if esm else
                  "import { createRequire } from 'node:module';\nconst component = createRequire(import.meta.url)('../decoder.cjs');")
        tests = ASSERTIONS.replace('LOAD', loader)
        versions = 'HEAD^ and HEAD' if esm else 'HEAD and the current unstaged working-tree implementation'
        instructions = '''Verification only. Use the available Node executable and native node --test
with TAP output; no npm script, dependency installation, network or external service.
Keep exactly the four current tests in tests/decoder.test.mjs unchanged in both
separate project-local disposable copies. Include the actual implementation in
each copy, not a rewritten simulation. The exported origin field is diagnostic
source identity, not an assertion that arbitrary code is tamper-proof.
Keep every supplied file's bytes/modes, notes.txt, Git HEAD and index unchanged.
Remove owned scratch, leaving no harness/report. Do not commit, stash, reset,
edit production/tests, access other repositories or search ancestor directories.
'''
        files = {name: before, 'AGENTS.md': instructions,
                 'notes.txt': 'Owner notes: preserve this file too.\n'}
        history = [dict(message='Original decoder', files=files)]
        working = {'tests/decoder.test.mjs': tests}
        if esm:
            history.append(dict(message='Retain incomplete frame header', files={name: after}))
        else:
            working[name] = after
        rows.append(dict(id='node-decoder-' + mode, skill='receipt',
            files={**files, name: after}, history=history, working_files=working,
            task=f'''Verify the existing fix in {name}, comparing {versions} in isolated
copies using the identical current tests/decoder.test.mjs. The contract is a
two-byte unsigned big-endian byte length followed by arbitrary binary payload.
push must retain incomplete frames across chunks, emit every complete frame in
order and support zero-length payloads; empty input alone emits no new frame.
Run all four current native tests for both versions and report their own exits,
identities and actual assertions, distinguishing setup errors from a reproduced
defect. Identify source revisions (or working-tree byte identity), confirm the
test-bound module's reported origin lies in its corresponding copy within that
native process, and explain the mechanism supported by the observed results.
Follow AGENTS.md: preserve original files/modes and Git state, remove all scratch,
do not change code/tests or install anything. Missing evidence remains unknown.''',
            criteria=[
                'Both variants execute exactly the same four current native Node tests, preserving their bytes and inputs.',
                'Before: split binary payload assertion fails with actual empty frames versus expected 00ff0d0a; the other three controls pass, without setup failure.',
                'After: all four pass with native identities/counts/exits, and explanation ties the loss to consuming the header before the full payload is present.',
                'Source revision or working-tree identity and actual test-bound module copy-local origin/PID are evidenced, not a separate import-only process.',
                'Original files/modes, notes, Git HEAD/index and skill resources preserved; scratch removed; no code/test edits or external activity.'],
            provenance=dict(kind='Authored synthetic transfer pair; not independent real-world holdouts',
                            module=mode, difference='ESM committed fix versus CommonJS uncommitted fix')))
    return rows


def preflight(cases):
    node = shutil.which('node')
    if not node:
        raise RuntimeError('Native Node preflight requires Node')
    spec = importlib.util.spec_from_file_location('node_compare_control', ROOT / 'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(prefix='node-cases-', dir=ROOT / 'benchmarks') as scratch:
        for case in cases:
            project = Path(scratch) / case['id']
            run.prepare(case, project)
            original = helper.tree_inventory(project)
            esm = case['id'].endswith('esm-committed')
            name = 'decoder.mjs' if esm else 'decoder.cjs'
            before, after = ('HEAD^', 'HEAD') if esm else ('HEAD', {'working_tree': True})
            for label, revision, expected in (('before', before, 1), ('after', after, 0)):
                with tempfile.TemporaryDirectory(prefix='.native-copy-', dir=project) as scratch_copy:
                    copy = Path(scratch_copy).resolve()
                    (copy / 'tests').mkdir()
                    (copy / 'tests/decoder.test.mjs').write_bytes((project / 'tests/decoder.test.mjs').read_bytes())
                    content = ((project / name).read_bytes() if isinstance(revision, dict) else
                               subprocess.check_output(['git', 'show', revision + ':' + name], cwd=project))
                    (copy / name).write_bytes(content)
                    result = subprocess.run([node, '--test', '--test-reporter=tap', 'tests/decoder.test.mjs'],
                                            cwd=copy, capture_output=True, text=True, timeout=10)
                    output = result.stdout + result.stderr
                    assert result.returncode == expected and '# tests 4' in output, output
                    assert '# fail ' + str(expected) in output, output
                    assert str(copy / name) in output and 'ACTUAL_MODULE ' in output, output
                    if expected:
                        assert '00ff0d0a' in output and 'ERR_ASSERTION' in output, output
                        assert '# pass 3' in output, output
                    else:
                        assert '# pass 4' in output, output
                    normalized = output.replace(str(copy), '<COPY>')
                    normalized = re.sub(r'"pid":\d+', '"pid":"<PID>"', normalized)
                    normalized = re.sub(r'(duration_ms: )[\d.]+', r'\1<DURATION>', normalized)
                    normalized = re.sub(r'(# duration_ms )[\d.]+', r'\1<DURATION>', normalized)
                    rows.append(dict(case=case['id'], variant=label, native_exit=result.returncode, output=normalized))
            recipe = dict(fixed=['tests'], vary=[name], before=before, after=after,
                          imports=[name], tests=['tests/decoder.test.mjs'], runner='node', guard_tree=True)
            comparison = helper.compare(project, recipe, node=node)
            assert comparison['status'] == 'observed', comparison
            assert [c['native_exit_code'] for c in comparison['checks'].values()] == [1, 0], comparison
            assert all(c['provenance_ready'] for c in comparison['checks'].values()), comparison
            assert comparison['comparison_copies_removed'] and comparison['tree_guard']['unchanged']
            assert helper.tree_inventory(project) == original
            assert not list(project.glob('.native-copy-*')) and not list(project.glob('.receipt-*'))
    return dict(node=subprocess.check_output([node, '--version'], text=True).strip(),
                native_controls=rows, helper_controls='Both cases preserve originals, sources and cleanup; before 1 / after 0')


if __name__ == '__main__':
    cases = build_cases()
    print(json.dumps(dict(cases=cases, preflight=preflight(cases)), indent=2))
