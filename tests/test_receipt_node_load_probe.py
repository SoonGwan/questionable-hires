"""Actual native-runner controls for an unshipped Node comparison direction."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / 'benchmarks/node_load_probe/hook.mjs'
NODE = shutil.which('node')


def records(output, prefix):
    return [json.loads(line.split(prefix, 1)[1]) for line in output.splitlines() if prefix in line]


@unittest.skipUnless(NODE, 'Node runtime is not installed')
class NodeLoadProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run([NODE, '-p', "typeof require('node:module').registerHooks"],
                                capture_output=True, text=True, timeout=5)
        if result.returncode or result.stdout.strip() != 'function':
            raise unittest.SkipTest('Synchronous Node loader hooks are unavailable')

    def run_case(self, kind, value=2, observed=True, throws=False, wrong_binding=False):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            root = Path(scratch).resolve()
            extension = 'mjs' if kind == 'esm' else 'cjs'
            source = ('throw new Error("evaluation failed");\n' if throws else '')
            source += ('export const observed = ' if kind == 'esm' else 'exports.observed = ')
            source += f'{{ value: {value}, phase: globalThis.qhPhase, pid: process.pid }};\n'
            app = root / ('app.' + extension)
            app.write_text(source)
            if wrong_binding:
                (root / ('other.' + extension)).write_text(source)
            target = 'other' if wrong_binding else 'app'
            load = (f'(await import("./{target}.mjs")).observed' if kind == 'esm'
                    else f'require("./{target}.cjs").observed')
            test_source = ('import test from "node:test"; import assert from "node:assert/strict";\n'
                           if kind == 'esm' else
                           'const test = require("node:test"); const assert = require("node:assert/strict");\n')
            test_source += '''test('native regression', async () => {
  globalThis.qhPhase = 'ready';
  const observed = LOAD;
  console.log('QH_BEHAVIOR ' + JSON.stringify(observed));
  assert.equal(observed.phase, 'ready');
  assert.equal(observed.pid, process.pid);
  assert.equal(observed.value, 2);
});
'''.replace('LOAD', load)
            path = root / ('regression.test.' + extension)
            path.write_text(test_source)
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            env = dict(os.environ, QH_PROBE_MODULE_URLS=json.dumps([app.as_uri()]))
            # Keep this preflight independent of inherited user preloads/options.
            # A production integration would need an explicit compatibility policy.
            env.pop('NODE_OPTIONS', None)
            command = [NODE, '--test', '--test-reporter=tap']
            if observed:
                command += ['--import', str(HOOK)]
            command.append(str(path))
            result = subprocess.run(command, cwd=root, env=env, capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)
            output = result.stdout + result.stderr
            return result.returncode, output, records(output, 'QH_LOAD '), records(output, 'QH_BEHAVIOR '), hashlib.sha256(source.encode()).hexdigest()

    def test_esm_and_cjs_keep_native_pass_fail_and_loading_order(self):
        for kind in ('esm', 'cjs'):
            for value in (1, 2):
                with self.subTest(kind=kind, value=value):
                    plain = self.run_case(kind, value, observed=False)
                    hooked = self.run_case(kind, value)
                    self.assertEqual(plain[0], 0 if value == 2 else 1, plain[1])
                    self.assertEqual(hooked[0], plain[0], hooked[1])
                    self.assertEqual(len(hooked[2]), 1, hooked[1])
                    self.assertEqual(len(hooked[3]), 1, hooked[1])
                    self.assertEqual(hooked[2][0]['pid'], hooked[3][0]['pid'])
                    self.assertEqual(hooked[2][0]['source_sha256'], hooked[4])
                    self.assertEqual(hooked[3][0]['phase'], 'ready')
                    self.assertEqual(hooked[3][0]['value'], value)
                    self.assertIn('# tests 1', hooked[1])
                    if value == 1:
                        self.assertIn('expected: 2', hooked[1])
                        self.assertIn('actual: 1', hooked[1])

    def test_success_without_selected_import_is_not_provenance(self):
        for kind in ('esm', 'cjs'):
            with self.subTest(kind=kind):
                status, output, loads, behavior, _ = self.run_case(kind, wrong_binding=True)
                self.assertEqual(status, 0, output)
                self.assertEqual(loads, [])
                self.assertEqual(len(behavior), 1)

    def test_load_record_does_not_prove_successful_evaluation(self):
        for kind in ('esm', 'cjs'):
            with self.subTest(kind=kind):
                status, output, loads, behavior, _ = self.run_case(kind, throws=True)
                self.assertEqual(status, 1, output)
                self.assertEqual(len(loads), 1, output)
                self.assertEqual(behavior, [])
                self.assertIn('evaluation failed', output)
