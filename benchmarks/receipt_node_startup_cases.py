"""Authored guide-transfer controls, including required Node preload semantics."""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from unittest.mock import patch

import run

ROOT = Path(__file__).resolve().parents[1]


def normalized(output, root):
    output = output.replace(str(root), '<COPY>')
    output = re.sub(r'"pid":\d+', '"pid":"<PID>"', output)
    return re.sub(r'(duration_ms:? )[\d.]+', r'\1<DURATION>', output)


BEFORE = '''const defaults = DEFAULTS;
export const origin = import.meta.url;
export function retries(options = {}) { return options.retries || defaults.retries; }
'''
AFTER = BEFORE.replace('options.retries ||', 'options.retries ??')
TESTS = '''import test from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import * as policy from '../policy.mjs';
console.log('ACTUAL_MODULE ' + JSON.stringify({path:fileURLToPath(policy.origin),pid:process.pid}));
test('explicit zero disables retries', () => assert.equal(policy.retries({retries:0}), 0));
test('explicit positive survives', () => assert.equal(policy.retries({retries:2}), 2));
test('omitted value uses default', () => assert.equal(policy.retries(), 3));
test('null uses default', () => assert.equal(policy.retries({retries:null}), 3));
'''
BOOTSTRAP = "globalThis.RUNTIME_DEFAULTS = Object.freeze({retries:3});\n"


def build_cases():
    rows = []
    for mode in ('plain', 'preloaded'):
        defaults = '{retries:3}' if mode == 'plain' else 'globalThis.RUNTIME_DEFAULTS'
        before, after = BEFORE.replace('DEFAULTS', defaults), AFTER.replace('DEFAULTS', defaults)
        # Reading a required default at import time makes missing setup a setup
        # error, never a valid before-failure witness.
        if mode == 'preloaded':
            before = before.replace('export const origin', 'void defaults.retries;\nexport const origin')
            after = after.replace('export const origin', 'void defaults.retries;\nexport const origin')
        command = "node --test --test-reporter=tap tests/policy.test.mjs"
        if mode == 'preloaded':
            command = "NODE_OPTIONS='--import ./bootstrap.mjs' " + command
        instructions = f'''Verification only. Native invocation from each copied project root:
{command}
Use the available Node executable, no installation/network/external services.
Keep this startup contract, actual implementation and the same current four tests
in both separate project-local disposable copies. Do not rewrite a simulation,
test or bootstrap, substitute inline globals, or remove required preload/options.
The origin export is diagnostic identity, not tamper-proof attestation.
Preserve all original bytes/modes, notes.txt, Git HEAD/index and installed skill
resources. Remove owned scratch and leave no new harness/report. No production
edits, commits, stashes, resets, other repositories or ancestor discovery.
'''
        files = {'policy.mjs': before, 'AGENTS.md': instructions, 'notes.txt': 'Preserve owner notes.\n'}
        if mode == 'preloaded':
            files['bootstrap.mjs'] = BOOTSTRAP
        rows.append(dict(id='node-retries-' + mode, skill='receipt',
            files={**files, 'policy.mjs': after},
            history=[dict(message='Original retry defaults', files=files),
                     dict(message='Honor explicit retry disable', files={'policy.mjs': after})],
            working_files={'tests/policy.test.mjs': TESTS},
            task='''Verify the existing policy.mjs fix by comparing HEAD^ and HEAD with
the identical current tests/policy.test.mjs in disposable project-local copies.
The supported input contract is omitted/null (default three retries), explicit
zero (disable retries), and positive integer values. No other input behavior is
specified. Follow the exact native startup command in AGENTS.md for both variants.
Run all four tests, report native identities/counts/exits and actual assertions,
and distinguish missing setup from a defect reproduction. Identify full revisions
and confirm the test-bound module origin/PID comes from the corresponding copy
inside each native test process. Explain the supported mechanism. Preserve original
files/modes, notes and Git state; remove scratch. Do not change code/tests/setup or
install anything. Unavailable evidence remains unknown.''',
            criteria=[
                'Both revisions execute identical current four tests under the required native startup, preserving preload/configuration when present.',
                'Before has the actual explicit-zero assertion failure (3 versus 0), with three neighboring controls passing and no setup error.',
                'After passes four with native counts/exits; explanation identifies falsy fallback versus nullish default and does not invent unspecified input contracts.',
                'Full revisions and actual native test-bound module copy-local origin/PID are evidenced, not a separate import-only check.',
                'Original bytes/modes, notes, Git HEAD/index and installed resources unchanged; scratch removed, no code/test/setup edits or external activity.'],
            provenance=dict(kind='Related authored synthetic guide-transfer tasks, not real issues or independent holdouts',
                            startup=mode)))
    return rows


def preflight(cases):
    node = shutil.which('node')
    if not node:
        raise RuntimeError('Node is required')
    if any(os.environ.get(k) for k in ('NODE_OPTIONS', 'NODE_PATH', 'NODE_COMPILE_CACHE')):
        raise RuntimeError('Author controls require a clean startup environment; do not silently discard it')
    spec = importlib.util.spec_from_file_location('startup_comparison', ROOT / 'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(prefix='node-startup-', dir=ROOT / 'benchmarks') as scratch:
        for case in cases:
            root = Path(scratch) / case['id']
            run.prepare(case, root)
            original = helper.tree_inventory(root)
            preloaded = case['provenance']['startup'] == 'preloaded'
            for label, revision, expected in (('before', 'HEAD^', 1), ('after', 'HEAD', 0)):
                with tempfile.TemporaryDirectory(prefix='.native-copy-', dir=root) as directory:
                    copied = Path(directory).resolve()
                    (copied / 'tests').mkdir()
                    (copied / 'policy.mjs').write_bytes(subprocess.check_output(['git', 'show', revision + ':policy.mjs'], cwd=root))
                    (copied / 'tests/policy.test.mjs').write_bytes((root / 'tests/policy.test.mjs').read_bytes())
                    env = dict(os.environ)
                    if preloaded:
                        (copied / 'bootstrap.mjs').write_bytes((root / 'bootstrap.mjs').read_bytes())
                        env['NODE_OPTIONS'] = '--import ./bootstrap.mjs'
                    command = [node, '--test', '--test-reporter=tap', 'tests/policy.test.mjs']
                    result = subprocess.run(command, cwd=copied, env=env, capture_output=True, text=True, timeout=10)
                    output = result.stdout + result.stderr
                    assert result.returncode == expected and '# tests 4' in output, output
                    assert f'# fail {expected}' in output and f'# pass {4-expected}' in output, output
                    assert str(copied / 'policy.mjs') in output, output
                    if expected:
                        assert 'expected: 0' in output and 'actual: 3' in output, output
                    rows.append(dict(case=case['id'], variant=label, exit_code=result.returncode,
                                     tests=4, passed=4-expected, failed=expected,
                                     output=normalized(output, copied)))
                    if preloaded:
                        missing = subprocess.run(command, cwd=copied, env=dict(os.environ), capture_output=True, text=True, timeout=10)
                        missing_output = missing.stdout + missing.stderr
                        assert missing.returncode == 1 and 'TypeError' in missing_output, missing_output
                        assert 'ACTUAL_MODULE ' not in missing_output, missing_output
                        rows.append(dict(case=case['id'], variant=label, control='missing preload is setup failure',
                                         exit_code=missing.returncode, observed='TypeError before application identity',
                                         output=normalized(missing_output, copied)))
            recipe = dict(fixed=['tests'] + (['bootstrap.mjs'] if preloaded else []), vary=['policy.mjs'],
                          before='HEAD^', after='HEAD', imports=['policy.mjs'], tests=['tests/policy.test.mjs'],
                          runner='node', guard_tree=True)
            if preloaded:
                with patch.dict(os.environ, {'NODE_OPTIONS': '--import ./bootstrap.mjs'}):
                    try:
                        helper.compare(root, recipe, node=node)
                    except ValueError as error:
                        assert 'custom startup' in str(error), error
                    else:
                        raise AssertionError('Required custom startup must not be silently stripped')
            else:
                result = helper.compare(root, recipe, node=node)
                assert result['status'] == 'observed' and result['tree_guard']['unchanged'], result
                assert [v['native_exit_code'] for v in result['checks'].values()] == [1, 0], result
            assert helper.tree_inventory(root) == original
            assert not list(root.glob('.native-copy-*')) and not list(root.glob('.receipt-*'))
    return dict(node=subprocess.check_output([node, '--version'], text=True).strip(), controls=rows,
                preservation=True, helper='Plain succeeds; required custom startup rejects unchanged before execution')


if __name__ == '__main__':
    print(json.dumps(preflight(build_cases()), indent=2))
