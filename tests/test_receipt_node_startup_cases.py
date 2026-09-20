import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import receipt_node_startup_cases as fixture


class ReceiptNodeStartupCasesTests(unittest.TestCase):
    def test_contract_is_explicit_and_tests_are_identical(self):
        plain, preloaded = fixture.build_cases()
        self.assertEqual(plain['working_files'], preloaded['working_files'])
        for case in (plain, preloaded):
            self.assertEqual(len(case['criteria']), 5)
            self.assertEqual(len(case['history']), 2)
            self.assertIn('remove scratch', case['task'])
            self.assertIn('No other input behavior', case['task'])
            before = case['history'][0]['files']['policy.mjs']
            after = case['history'][1]['files']['policy.mjs']
            self.assertEqual(before.replace('options.retries ||', 'options.retries ??'), after)
        self.assertNotIn('bootstrap.mjs', plain['files'])
        self.assertEqual(preloaded['files']['bootstrap.mjs'], fixture.BOOTSTRAP)
        self.assertIn("NODE_OPTIONS='--import ./bootstrap.mjs'", preloaded['files']['AGENTS.md'])
        self.assertIn('void defaults.retries;', preloaded['files']['policy.mjs'])

    def test_author_startup_settings_are_not_silently_removed(self):
        with patch.object(fixture.shutil, 'which', return_value='/node'), \
                patch.dict(os.environ, {'NODE_OPTIONS': '--import required.mjs'}):
            with self.assertRaisesRegex(RuntimeError, 'do not silently discard'):
                fixture.preflight(fixture.build_cases())

    def test_native_defect_setup_and_preservation_controls(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Node unavailable')
        if any(os.environ.get(k) for k in ('NODE_OPTIONS', 'NODE_PATH', 'NODE_COMPILE_CACHE')):
            self.skipTest('Author startup configuration present; do not strip it')
        probe = subprocess.run([node, '-p', "typeof require('node:module').registerHooks"],
                               capture_output=True, text=True, timeout=5)
        if probe.returncode or probe.stdout.strip() != 'function':
            self.skipTest('Synchronous Node hooks unavailable')
        controls = fixture.preflight(fixture.build_cases())
        self.assertTrue(controls['preservation'])
        native = [r for r in controls['controls'] if 'control' not in r]
        self.assertEqual([r['exit_code'] for r in native], [1, 0, 1, 0])
        self.assertEqual([r['passed'] for r in native], [3, 4, 3, 4])
        for row in native:
            self.assertIn('ACTUAL_MODULE', row['output'])
            self.assertIn('<COPY>/policy.mjs', row['output'])
            if row['failed']:
                self.assertIn('expected: 0', row['output'])
                self.assertIn('actual: 3', row['output'])
        missing = [r for r in controls['controls'] if 'control' in r]
        self.assertEqual(len(missing), 2)
        for row in missing:
            self.assertEqual(row['exit_code'], 1)
            self.assertIn('TypeError', row['output'])
            self.assertNotIn('ACTUAL_MODULE', row['output'])


if __name__ == '__main__':
    unittest.main()
