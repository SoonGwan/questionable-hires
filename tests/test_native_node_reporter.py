import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPORTER = Path(__file__).resolve().parents[1] / 'benchmarks/prototypes/native_node_reporter.mjs'
NODE = shutil.which('node')
NODE_24 = NODE and subprocess.check_output([NODE, '--version'], text=True).startswith('v24.')


class PublishedReporterObservationTests(unittest.TestCase):
    def test_published_files_match_manifest_without_private_paths(self):
        root = REPORTER.parent.parent / 'results/native-node-reporter-01'
        manifest = json.loads((root / 'manifest.json').read_text())
        for run, files in manifest['runs'].items():
            for name, identity in files.items():
                with self.subTest(run=run, name=name):
                    path = root / run / name
                    if identity.get('published_file_omitted'):
                        self.assertEqual(identity['original_bytes'], 0)
                        self.assertEqual(identity['published_bytes'], 0)
                        self.assertFalse(path.exists())
                        continue
                    data = path.read_bytes()
                    self.assertEqual(len(data), identity['published_bytes'])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), identity['published_sha256'])
                    self.assertNotIn(b'/Users/admin', data)


@unittest.skipUnless(NODE_24, 'Experimental reporter checks require Node 24')
class NativeNodeReporterTests(unittest.TestCase):
    def execute(self, source):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'case.test.mjs').write_text(source)
            result = subprocess.run([NODE, '--test', '--test-reporter=tap',
                '--test-reporter-destination=raw.tap', '--test-reporter=' + str(REPORTER),
                '--test-reporter-destination=stdout', 'case.test.mjs'],
                cwd=root, text=True, capture_output=True, timeout=10)
            raw = (root / 'raw.tap').read_text()
            records = [json.loads(line) for line in result.stdout.splitlines()]
            calls = (root / 'calls').read_text() if (root / 'calls').exists() else None
            return result, raw, records, calls

    def test_repeated_native_failures_retained_and_tests_execute_once(self):
        result, raw, records, calls = self.execute('''
import test from 'node:test';
import assert from 'node:assert/strict';
import {appendFileSync} from 'node:fs';
for (let i = 0; i < 24; i++) test(`failure ${i}`, () => {
  appendFileSync('calls', 'x'); assert.equal(2, 1, 'wrong result');
});
''')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(calls, 'x' * 24)
        failures = [r for r in records if r['type'] == 'test:fail']
        self.assertEqual([r['name']['text'] for r in failures], ['failure '+str(i) for i in range(24)])
        self.assertTrue(all('wrong result' in r['error']['message']['text'] for r in failures))
        end = records[-1]
        self.assertTrue(end['single_global_summary_seen'])
        self.assertFalse(end['native']['native_success'])
        self.assertEqual(end['native']['counts']['failed'], 24)
        self.assertEqual(end['omitted_result_events'], 0)
        self.assertIn('actual: 2', raw)
        self.assertIn('expected: 1', raw)
        self.assertIn('stack:', raw)
        self.assertLess(len(result.stdout), len(raw))

    def test_nested_skip_todo_and_diagnostics_are_not_flat_passes(self):
        result, raw, records, _ = self.execute('''
import test, {describe} from 'node:test';
describe('group', () => {
  test('normal', t => { t.diagnostic('important diagnostic'); });
  test.skip('skipped', () => {});
  test.todo('future', () => {});
});
''')
        self.assertEqual(result.returncode, 0, result.stderr)
        end = records[-1]
        self.assertEqual(end['native']['counts']['skipped'], 1)
        self.assertEqual(end['native']['counts']['todo'], 1)
        self.assertTrue(any(r.get('skip') for r in records))
        self.assertTrue(any(r.get('todo') for r in records))
        self.assertIn('important diagnostic', raw)
        self.assertGreater(end['other_event_counts'].get('test:diagnostic', 0), 0)

    def test_normal_passing_control_is_not_claimed_as_compression(self):
        result, raw, records, _ = self.execute('''
import test from 'node:test';
for (let i = 0; i < 24; i++) test(`normal ${i}`, () => {});
''')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(records[-1]['native']['native_success'])
        self.assertEqual(records[-1]['native']['counts']['passed'], 24)
        self.assertEqual(records[-1]['omitted_result_events'], 0)
        self.assertGreater(len(result.stdout), len(raw))

    def test_syntax_error_stays_native_failure_with_raw_diagnostic(self):
        result, raw, records, _ = self.execute('this is not valid JavaScript!')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SyntaxError', raw)
        self.assertFalse(records[-1]['native']['native_success'])
        self.assertTrue(any(r['type'] == 'test:fail' for r in records))

    def test_unresolved_test_cancellation_is_not_success(self):
        result, raw, records, _ = self.execute('''
import test from 'node:test';
test('never settled', {timeout: 50}, async () => { await new Promise(() => {}); });
''')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(records[-1]['native']['native_success'])
        self.assertEqual(records[-1]['native']['counts']['cancelled'], 1)
        self.assertIn('cancelled', raw)

    def test_limits_disclose_omitted_events_and_truncated_names(self):
        result, raw, records, _ = self.execute('''
import test from 'node:test';
for (let i = 0; i < 205; i++) test('long-' + i + '-' + 'x'.repeat(600), () => {});
''')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(records[-1]['observed_result_events'], 205)
        self.assertEqual(records[-1]['omitted_result_events'], 5)
        self.assertTrue(records[1]['name']['truncated'])
        self.assertIn('long-204-', raw)

    def test_missing_global_summary_cannot_become_complete_summary(self):
        source = "import report from " + json.dumps(REPORTER.as_uri()) + "; for await (const line of report((async function*(){})())) process.stdout.write(line);"
        result = subprocess.run([NODE, '--input-type=module', '-e', source],
            text=True, capture_output=True, timeout=10, check=True)
        end = json.loads(result.stdout.splitlines()[-1])
        self.assertFalse(end['single_global_summary_seen'])
        self.assertNotIn('native', end)
