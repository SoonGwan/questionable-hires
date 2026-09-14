import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORRECT = '''export class SubmitPanel {
  pending = false;
  async submit(save, signal) {
    if (this.pending) return;
    this.pending = true;
    try { return await save(signal); }
    finally { this.pending = false; }
  }
}
'''


@unittest.skipUnless(shutil.which('node'), 'Node is required for fixture preflight')
class JavaScriptPanelFixtureTests(unittest.TestCase):
    def execute(self, implementation, probe=False):
        case = json.loads((ROOT / 'benchmarks/hostage-javascript-panel-cases.json').read_text())[0]
        with tempfile.TemporaryDirectory(prefix='.panel-preflight-', dir=ROOT / 'tests') as folder:
            root = Path(folder)
            for path, source in case['files'].items():
                (root / path).write_text(source)
            (root / 'panel.mjs').write_text(implementation)
            if probe:
                shutil.copyfile(ROOT / 'tests/fixtures/panel_contract.mjs', root / 'contract.mjs')
            command = ['node', 'contract.mjs'] if probe else ['node', '--test', '--test-reporter=tap']
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=10)
            self.assertEqual((root / 'panel.test.mjs').read_text(), case['files']['panel.test.mjs'])
            return result.returncode, result.stdout + result.stderr

    def test_original_and_correct_preserve_existing_native_tests(self):
        original = json.loads((ROOT / 'benchmarks/hostage-javascript-panel-cases.json').read_text())[0]['files']['panel.mjs']
        for source in (original, CORRECT):
            code, output = self.execute(source)
            self.assertEqual(code, 0, output)
            self.assertIn('# pass 2', output)

    def test_full_contract_accepts_correct_implementation(self):
        code, output = self.execute(CORRECT, probe=True)
        self.assertEqual(code, 0, output)
        self.assertIn('all panel transitions passed', output)

    def test_missing_guard_cleanup_and_signal_have_native_assertion_failures(self):
        variants = [CORRECT.replace('    if (this.pending) return;\n', ''),
                    CORRECT.replace('finally { this.pending = false; }', 'finally {}'),
                    CORRECT.replace('save(signal)', 'save(undefined)')]
        for source in variants:
            with self.subTest(source=source):
                code, output = self.execute(source, probe=True)
                self.assertEqual(code, 1, output)
                self.assertIn('AssertionError', output)
                self.assertNotIn('contract wait timed out', output)
