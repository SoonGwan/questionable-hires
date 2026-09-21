import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORTER = ROOT / 'benchmarks/prototypes/native_node_reporter_v2.mjs'
NODE = shutil.which('node')
NODE_24 = NODE and subprocess.check_output([NODE, '--version'], text=True).startswith('v24.')


@unittest.skipUnless(NODE_24, 'Experimental reporter checks require Node 24')
class FirstLookReporterTests(unittest.TestCase):
    def run_source(self, source):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'case.test.mjs').write_text(source)
            result = subprocess.run([NODE, '--test', '--test-reporter=tap',
                '--test-reporter-destination=raw.tap', '--test-reporter=' + str(REPORTER),
                '--test-reporter-destination=stdout', 'case.test.mjs'],
                cwd=root, capture_output=True, text=True, timeout=10)
            return result, (root / 'raw.tap').read_text(), [json.loads(s) for s in result.stdout.splitlines()]

    def test_passing_overhead_reduced_with_explicit_identity_omission(self):
        result, raw, records = self.run_source("import test from 'node:test'; for(let i=0;i<24;i++)test('pass'+i,()=>{});")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(records[-1]['native']['counts']['passed'], 24)
        self.assertEqual(records[-1]['ordinary_pass_identities_omitted'], 24)
        self.assertEqual(records[-1]['exceptional_results_omitted'], 0)
        self.assertLess(len(result.stdout), len(raw))
        self.assertIn('pass23', raw)

    def test_failure_after_many_passes_is_still_displayed(self):
        result, raw, records = self.run_source("""
import test from 'node:test'; import assert from 'node:assert/strict';
for(let i=0;i<205;i++)test('pass'+i,()=>{});
test('late failure',()=>assert.equal(2,1,'decisive failure'));
""")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(records[-1]['ordinary_pass_identities_omitted'], 205)
        self.assertEqual(records[-1]['exceptional_results_shown'], 1)
        self.assertEqual(records[1][1], 'late failure')
        self.assertIn('decisive failure', records[1][7])
        self.assertIn('actual: 2', raw)
        self.assertFalse(records[-1]['native']['success'])

    def test_skip_todo_and_diagnostic_not_silently_classed_as_ordinary(self):
        result, raw, records = self.run_source("""
import test from 'node:test';
test.skip('skip',()=>{}); test.todo('todo',()=>{});
test('pass',t=>t.diagnostic('important'));
""")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(records[1][5])
        self.assertTrue(records[2][6])
        self.assertEqual(records[-1]['ordinary_pass_identities_omitted'], 1)
        self.assertGreater(records[-1]['other_events']['test:diagnostic'], 0)
        self.assertIn('important', raw)

    def test_skips_cannot_exhaust_failure_allowance(self):
        result, raw, records = self.run_source("""
import test from 'node:test';
for(let i=0;i<205;i++)test.skip('skip'+i,()=>{});
test('late failure',()=>{throw new Error('still visible');});
""")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(records[-1]['exceptional_results_omitted'], 5)
        self.assertEqual(records[-1]['displayed_by_type']['test:fail'], 1)
        self.assertEqual(records[-2][1], 'late failure')
        self.assertIn('still visible', raw)

    def test_exceptional_cap_and_text_truncation_are_explicit(self):
        result, raw, records = self.run_source("import test from 'node:test'; for(let i=0;i<205;i++)test.skip('x'.repeat(600)+i,()=>{});")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(records[-1]['exceptional_results_shown'], 200)
        self.assertEqual(records[-1]['exceptional_results_omitted'], 5)
        self.assertTrue(records[1][1]['truncated'])
        self.assertIn('x'*600+'204', raw)

    def test_syntax_failure_is_not_pass(self):
        result, raw, records = self.run_source('this is invalid JavaScript!')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(records[-1]['native']['success'])
        self.assertIn('SyntaxError', raw)

    def test_native_cancellation_remains_failure(self):
        result, raw, records = self.run_source("import test from 'node:test';test('timeout',{timeout:50},async()=>await new Promise(()=>{}));")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(records[-1]['native']['success'])
        self.assertEqual(records[-1]['native']['counts']['cancelled'], 1)
        self.assertEqual(records[1][0], 'test:fail')
        self.assertIn('cancelled', raw)

    def test_repeated_failures_keep_names_and_execute_once(self):
        result, raw, records = self.run_source("""
import test, {after} from 'node:test'; import assert from 'node:assert/strict';
let calls=0;
for(let i=0;i<24;i++)test('failure'+i,()=>{calls++;assert.equal(2,1,'wrong result');});
after(()=>assert.equal(calls,24,'exactly once'));
""")
        self.assertEqual(result.returncode, 1)
        self.assertEqual([r[1] for r in records if isinstance(r,list)], ['failure'+str(i) for i in range(24)])
        self.assertEqual(records[-1]['native']['counts']['failed'], 24)
        self.assertEqual(records[-1]['exceptional_results_omitted'], 0)
        self.assertLess(len(result.stdout), len(raw))
        self.assertNotIn('hookFailed', raw)

    def test_zero_tests_does_not_invent_test_evidence(self):
        result, raw, records = self.run_source('export const noAssertions = true;')
        self.assertEqual(result.returncode, 0)
        # Node can report file-level success even without authored assertions.
        self.assertIn('not verification', records[0]['warning'])
        self.assertEqual(records[-1]['exceptional_results_shown'], 0)
        self.assertIn('case.test.mjs', raw)

    def test_empty_stream_does_not_get_native_success(self):
        source = 'import report from ' + json.dumps(REPORTER.as_uri()) + ';for await(const s of report((async function*(){})()))process.stdout.write(s);'
        result = subprocess.run([NODE, '--input-type=module', '-e', source],
            capture_output=True, text=True, timeout=10, check=True)
        end = json.loads(result.stdout.splitlines()[-1])
        self.assertEqual(end['summaries'], 0)
        self.assertIsNone(end['native'])
