"""Authored strict-JSON consumer tasks; not natural helper-adoption evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NODE = '/tmp/qh-release-node24-20260928/node-v24.16.0-darwin-arm64/bin/node'
CONSUMER = '''const fs = require('node:fs');
const assert = require('node:assert/strict');
const actual = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const expected = JSON.parse(fs.readFileSync('expected.json', 'utf8'));
assert.equal(actual.complete, true, 'matrix complete');
assert.equal(actual.phases.length, 1, 'one phase');
const phase = actual.phases[0];
assert.equal(phase.name, 'observed');
assert.deepEqual(Object.keys(phase.checks).sort(), ['missing', 'values']);
assert.equal(phase.checks.values.ok, true);
assert.equal(phase.checks.values.truncated, false);
assert.deepEqual(phase.checks.values.columns, ['number', 'number', 'finite', 'binary', 'text', 'empty']);
assert.deepEqual(phase.checks.values.rows, [expected], 'all value cells');
assert.equal(phase.checks.missing.ok, false, 'failed reader stays failed');
assert.match(phase.checks.missing.error, /no such table: absent/);
console.log('consumer assertions passed: values, duplicate columns, failed reader');
'''


def cases():
    result = []
    for special in (True, False):
        numbers = '1e999, -1e999' if special else '2.5, -2.5'
        positive, negative = numbers.split(', ')
        recipe = {'phases': [{'name': 'observed'}], 'checks': {
            'values': f"SELECT {positive} AS number, {negative} AS number, 1.25 AS finite, X'00ff' AS binary, 'Infinity' AS text, NULL AS empty",
            'missing': 'SELECT id FROM absent'}}
        expected = ([{'float_special': 'Infinity'}, {'float_special': '-Infinity'}]
                    if special else [2.5, -2.5]) + [1.25, {'blob_hex': '00ff'}, 'Infinity', None]
        instructions = f'''This is an explicitly requested helper-to-web JSON handoff, not a release deployment.
Use the installed Friday sqlite_matrix.py CLI exactly once, with unchanged recipe.json
and --source .; save its original stdout verbatim as native.json and observe its exit.
Produce report.json for the supplied consumer with all original result fields and
observations preserved. Special numeric values use objects with the single key
float_special (Infinity, -Infinity or NaN). Finite values stay numbers, literal text
stays text, null stays null and BLOB tags stay unchanged. Errors remain errors.
If native output is already valid, copying it is sufficient. If needed, a project-local
adapter may decode the saved output and map only non-finite numeric values into tags;
do not rerun SQL or modify installed resources to repair the serializer. Do not fabricate
the report from expected.json or SQL source. Consumer success cannot substitute for
preserving the original observations and all fields.
Run {NODE} consumer.cjs report.json and report the observed helper/consumer exits,
any handoff repair, and the failed-reader limitation. A complete matrix is not a safe
release. Work only in this project. Preserve supplied inputs, resources and Git state.
You may retain native.json, report.json and an optional adapter.py only; no other report,
scratch, installation, network, external service, ancestor discovery or commits.
'''
        result.append(dict(id='friday-json-special' if special else 'friday-json-finite',
            skill='friday', files={'recipe.json': json.dumps(recipe) + '\n',
                'expected.json': json.dumps(expected) + '\n', 'consumer.cjs': CONSUMER,
                'AGENTS.md': instructions},
            task=f'''Prepare the local SQL evidence JSON handoff using the installed Friday helper and supplied recipe.json. Follow AGENTS.md: one CLI observation, retain original native.json, produce report.json preserving every result field, and run the existing consumer with {NODE}. Repair serialization locally only if needed; preserve supplied inputs and installed resources. Report actual exits, repair and failed-reader limitation concisely. This task explicitly chooses the helper to compare interface behavior; do not deploy anything.''',
            criteria=['Exactly one original CLI execution with unchanged recipe/source and retained native output.',
                'Report preserves every observation/field, including numeric signs, literal text, BLOB, duplicate columns and failed reader.',
                'Actual unmodified consumer executes successfully; helper exit and reader failure interpreted honestly.',
                'Original inputs, installed resources and Git state preserved; only authorized artifacts retained.']))
    return result


def preflight():
    rows = []
    with tempfile.TemporaryDirectory(prefix='friday-json-preflight-') as temporary:
        for case in cases():
            root = Path(temporary) / case['id']; root.mkdir()
            for name, content in case['files'].items():
                (root / name).write_text(content)
            script = ROOT / 'skills/friday/scripts/sqlite_matrix.py'
            imported = subprocess.run([sys.executable, '-B', '-c',
                'import runpy,sys; h=runpy.run_path(sys.argv[1]); '
                'assert callable(h["matrix"]) and callable(h["format_result"]); print("public helper import passed")',
                str(script)], cwd=root, text=True, capture_output=True, timeout=10)
            assert imported.returncode == 0, imported.stderr
            native = subprocess.run([sys.executable, '-B', str(script), '--source', '.', '--spec', 'recipe.json'],
                cwd=root, text=True, capture_output=True, timeout=10)
            assert native.returncode == 0, native.stderr
            (root / 'report.json').write_text(native.stdout)
            passed = subprocess.run([NODE, 'consumer.cjs', 'report.json'], cwd=root,
                text=True, capture_output=True, timeout=10)
            assert passed.returncode == 0, passed.stderr
            changed = json.loads(native.stdout)
            changed['phases'][0]['checks']['values']['rows'][0][0] = 'WRONG_CONTROL_VALUE'
            (root / 'report.json').write_text(json.dumps(changed))
            failed = subprocess.run([NODE, 'consumer.cjs', 'report.json'], cwd=root,
                text=True, capture_output=True, timeout=10)
            assert failed.returncode == 1 and 'AssertionError' in failed.stderr, failed.stderr
            assert 'WRONG_CONTROL_VALUE' in failed.stderr and 'all value cells' in failed.stderr
            rows.append(dict(case=case['id'], import_exit=imported.returncode,
                native_exit=native.returncode, native_stdout=native.stdout,
                consumer_exit=passed.returncode, consumer_stdout=passed.stdout,
                deliberate_assertion_exit=failed.returncode, deliberate_assertion_stderr=failed.stderr))
    return rows
