from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ControlledCallJavaScriptTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'Node is required for native JavaScript verification')
    def test_scope_lifecycle_and_failure_controls(self):
        result = subprocess.run(['node', '--test', '--test-reporter=tap',
                                 'tests/controlled_scope_js.test.mjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=15)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn('# tests 10', output)
        self.assertIn('# pass 10', output)
        self.assertIn('# fail 0', output)

    @unittest.skipUnless(shutil.which('node'), 'Node is required for native JavaScript verification')
    def test_native_asset_and_real_owner_controls(self):
        result = subprocess.run(['node', '--test', '--test-reporter=tap',
                                 'tests/controlled_call_js.test.mjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=15)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn('# tests 7', output)
        self.assertIn('# pass 7', output)
        self.assertIn('# fail 0', output)

    @unittest.skipUnless(shutil.which('node'), 'Node is required for native JavaScript verification')
    def test_copied_asset_has_no_repository_or_installed_skill_dependency(self):
        with tempfile.TemporaryDirectory() as folder:
            asset = ROOT / 'skills/hostage-negotiator/assets/controlled_call.mjs'
            target = Path(folder) / 'controlled_call.mjs'
            shutil.copyfile(asset, target)
            result = subprocess.run(['node', '--input-type=module', '-e', '''
import assert from 'node:assert/strict';
import { controlledCall, withControlledCalls } from './controlled_call.mjs';
const callback = controlledCall(), value = {};
const task = callback(value);
const call = await callback.started();
assert.equal(call.args[0], value);
call.complete(value);
assert.equal(await task, value);
await withControlledCalls(async ({ call, run, wait }) => {
    const save = call(), task = run(() => save(value));
    (await save.started()).complete(value);
    assert.equal(await wait(task), value);
});
console.log('standalone copy passed');
'''], cwd=folder, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('standalone copy passed', result.stdout)
            self.assertEqual(target.read_bytes(), asset.read_bytes())
