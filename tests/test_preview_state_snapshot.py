"""Author repair of a frozen model-test blind spot, never rewriting old evidence."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'benchmarks/results/hostage-javascript-preview-01/javascript-preview-latest--skill--1/project'


@unittest.skipUnless(shutil.which('node'), 'Node is required for state-content regression validation')
class PreviewStateSnapshotTests(unittest.TestCase):
    def execute(self, *, repair, success='guarded', error='guarded'):
        original_test = (PROJECT / 'preview.regression.test.mjs').read_text()
        original_owner = (PROJECT / 'preview.mjs').read_text()
        test = original_test
        if repair:
            capture = 'const protectedState = loader.state;'
            assertion = 'assert.equal(loader.state, protectedState);'
            self.assertEqual(test.count(capture), 2)
            self.assertEqual(test.count(assertion), 2)
            test = test.replace(capture, 'const protectedState = { ...loader.state };')
            test = test.replace(assertion,
                'state(loader, protectedState.status, protectedState.value, protectedState.error);')
        owner = original_owner
        guard = 'if (this.#latestRequest === request)'
        for status, mode, fields in [
            ('ready', success, 'status: \'ready\', value, error: null'),
            ('error', error, 'status: \'error\', value: this.state.value, error'),
        ]:
            if mode == 'guarded':
                continue
            assignment = f'this.state = {{ {fields} }};'
            block = guard + ' {\n        ' + assignment + '\n      }'
            self.assertEqual(owner.count(block), 1)
            mutation = f'Object.assign(this.state, {{ {fields} }});'
            if mode == 'guarded_in_place':
                replacement = guard + ' {\n        ' + mutation + '\n      }'
            else:
                self.assertEqual(mode, 'unguarded_in_place')
                replacement = mutation
            owner = owner.replace(block, replacement)
        with tempfile.TemporaryDirectory(prefix='.snapshot-preflight-', dir=ROOT / 'tests') as folder:
            scratch = Path(folder) / 'project'
            shutil.copytree(PROJECT, scratch)
            (scratch / 'preview.mjs').write_text(owner)
            (scratch / 'preview.regression.test.mjs').write_text(test)
            result = subprocess.run(['node', '--test', '--test-reporter=tap'], cwd=scratch,
                                    capture_output=True, text=True, timeout=15)
            for path in ('preview.test.mjs', 'requirements.md', 'test-support/controlled_call.mjs'):
                self.assertEqual((scratch / path).read_bytes(), (PROJECT / path).read_bytes())
        self.assertEqual((PROJECT / 'preview.mjs').read_text(), original_owner)
        self.assertEqual((PROJECT / 'preview.regression.test.mjs').read_text(), original_test)
        output = result.stdout + result.stderr
        self.assertIn('# tests 54', output)
        self.assertIn('# cancelled 0', output)
        self.assertIn('# skipped 0', output)
        return result.returncode, output

    def test_preserve_historical_escape_in_untouched_tests(self):
        code, output = self.execute(repair=False, success='unguarded_in_place')
        self.assertEqual(code, 0, output)
        self.assertIn('# pass 54', output)

    def test_field_snapshot_accepts_correct_replacement_and_in_place_updates(self):
        for mode in ('guarded', 'guarded_in_place'):
            with self.subTest(mode=mode):
                code, output = self.execute(repair=True, success=mode, error=mode)
                self.assertEqual(code, 0, output)
                self.assertIn('# pass 54', output)

    def test_field_snapshot_detects_stale_success_and_error_contents(self):
        for phase in ('success', 'error'):
            with self.subTest(phase=phase):
                code, output = self.execute(repair=True, **{phase: 'unguarded_in_place'})
                self.assertEqual(code, 1, output)
                self.assertIn('ERR_ASSERTION', output)
                self.assertIn('actual', output)
                self.assertIn('expected', output)
                self.assertNotIn('deadline exceeded', output)
