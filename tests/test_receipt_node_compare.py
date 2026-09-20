"""Native Node regression comparisons, preservation and incomplete evidence."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_receipt_helper import helper

ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which('node')


@unittest.skipUnless(NODE and os.name == 'posix', 'Requires Node/POSIX')
class NodeComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        probe = subprocess.run([NODE, '-p', "typeof require('node:module').registerHooks"],
                               capture_output=True, text=True, timeout=5)
        if probe.returncode or probe.stdout.strip() != 'function':
            raise unittest.SkipTest('Node synchronous loader hooks unavailable')

    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        env = dict(os.environ)
        for key in ('NODE_OPTIONS', 'NODE_PATH', 'NODE_COMPILE_CACHE'):
            env.pop(key, None)
        self.environment = patch.dict(os.environ, env, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.git('init', '-q', '--template=')
        for key, value in (('user.name', 'Fixture'), ('user.email', 'fixture@example.invalid'),
                           ('commit.gpgsign', 'false'), ('core.hooksPath', str(self.root / 'no-hooks'))):
            self.git('config', key, value)
        for extension, prefix in (('mjs', 'export const accepted ='), ('cjs', 'exports.accepted =')):
            (self.root / ('app.' + extension)).write_text(prefix + ' n => n > 18;\n')
        self.commit()
        for path in self.root.glob('app.*'):
            path.write_text(path.read_text().replace('> 18', '>= 18'))
        self.commit()
        self.test = self.root / 'regression.test.mjs'
        self.test.write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import {accepted} from './app.mjs';
test('age boundary', () => { assert.equal(accepted(18), true); });
''')
        self.recipe = dict(fixed=[self.test.name], vary=['app.mjs'], before='HEAD^', after='HEAD',
                           imports=['app.mjs'], tests=[self.test.name], runner='node', guard_tree=True)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixture')

    def compare(self, recipe=None, **kwargs):
        before = helper.tree_inventory(self.root)
        result = helper.compare(self.root, recipe or self.recipe, node=NODE, **kwargs)
        self.assertEqual(helper.tree_inventory(self.root), before)
        self.assertTrue(result['comparison_copies_removed'])
        self.assertTrue(result['tree_guard']['unchanged'])
        self.assertEqual(list(self.root.glob('.receipt-*')), [])
        return result

    def test_committed_esm_preserves_native_assertions_and_sources(self):
        result = self.compare()
        self.assertEqual(result['status'], 'observed')
        self.assertEqual([c['native_exit_code'] for c in result['checks'].values()], [1, 0])
        self.assertIn('expected: true', result['checks']['before']['output'])
        self.assertIn('actual: false', result['checks']['before']['output'])
        for check in result['checks'].values():
            self.assertTrue(check['provenance_ready'])
            self.assertEqual(len(check['copied_loads']), 1)
            self.assertIn('# tests 1', check['output'])

    def test_commonjs_and_working_tree_after(self):
        self.test.write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
test('age boundary', () => { assert.equal(require('./app.cjs').accepted(18), true); });
''')
        result = self.compare(dict(self.recipe, vary=['app.cjs'], imports=['app.cjs'],
                                   after={'working_tree': True}))
        self.assertEqual([c['exit_code'] for c in result['checks'].values()], [1, 0])
        self.assertIsNone(result['revisions']['after'])
        self.assertEqual(set(result['working_tree_after']['sha256']), {'app.cjs'})

    def test_missing_load_stops_before_after_even_if_native_test_passes(self):
        self.test.write_text("import test from 'node:test'; test('unrelated', () => {});\n")
        result = self.compare()
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        check = result['checks']['before']
        self.assertEqual((check['exit_code'], check['native_exit_code']), (7, 0))
        self.assertFalse(check['provenance_ready'])

    def test_truncated_output_does_not_certify_provenance(self):
        self.test.write_text(self.test.read_text() + "console.log('x'.repeat(13000));\n")
        result = self.compare()
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertTrue(result['checks']['before']['output_truncated'])

    def test_deadline_stops_comparison_and_cleans_copies(self):
        self.test.write_text(self.test.read_text() + 'setInterval(() => {}, 1000);\n')
        result = self.compare(timeout=0.5)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertTrue(result['checks']['before']['timed_out'])

    def test_custom_environment_and_python_options_reject_before_execution(self):
        with patch.object(helper, 'run_node_check', side_effect=AssertionError('must not execute')):
            for key in ('NODE_OPTIONS', 'NODE_PATH', 'NODE_COMPILE_CACHE'):
                with self.subTest(key=key), patch.dict(os.environ, {key: 'custom'}):
                    with self.assertRaisesRegex(ValueError, 'custom startup'):
                        helper.compare(self.root, self.recipe, node=NODE)
            for key, value in (('invocation', 'module'), ('import_roots', []), ('module_bindings', {})):
                with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Python invocation'):
                    helper.compare(self.root, dict(self.recipe, **{key: value}), node=NODE)
            for key, value in (('tests', ['--help']), ('imports', ['app']),
                               ('tests', ['../outside.mjs']), ('tests', ['app.mjs'])):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    helper.compare(self.root, dict(self.recipe, **{key: value}), node=NODE)

    def test_bad_record_cannot_become_verified_load(self):
        for record in ({'url': []}, {'url': 'file:///unselected', 'pid': 1, 'sha256': 'wrong'}, None):
            with self.subTest(record=record), patch.object(helper, 'capture_check', return_value=dict(
                    exit_code=0, timed_out=False, output_truncated=False,
                    output='Receipt copied load: ' + json.dumps(record) + '\n')):
                result = self.compare()
                self.assertEqual(result['status'], 'incomplete')
                self.assertFalse(result['checks']['before']['provenance_ready'])
                self.assertEqual(list(result['checks']), ['before'])

    def test_cli_json_stdin_observations_are_not_a_success_claim(self):
        before = helper.tree_inventory(self.root)
        run = subprocess.run([sys.executable, '-B', str(Path(helper.__file__)), '--source', str(self.root),
                              '--spec', '-', '--node', NODE], input=json.dumps(self.recipe),
                             text=True, capture_output=True, timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertEqual(helper.tree_inventory(self.root), before)
