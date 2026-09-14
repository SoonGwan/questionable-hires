import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORRECT = '''export class PreviewLoader {
  state = { status: 'idle', value: null, error: null };
  generation = 0;
  async load(key, fetchBytes, decode, signal) {
    const generation = ++this.generation;
    this.state = { status: 'loading', value: this.state.value, error: null };
    try {
      const bytes = await fetchBytes(key, signal);
      const value = await decode(bytes, signal);
      if (generation === this.generation) this.state = { status: 'ready', value, error: null };
      return value;
    } catch (error) {
      if (generation === this.generation) this.state = { status: 'error', value: this.state.value, error };
      throw error;
    }
  }
}
'''


@unittest.skipUnless(shutil.which('node'), 'Node is required for preview fixture validation')
class JavaScriptPreviewFixtureTests(unittest.TestCase):
    def execute(self, source, contract=True):
        case = json.loads((ROOT / 'benchmarks/hostage-javascript-preview-cases.json').read_text())[0]
        with tempfile.TemporaryDirectory(prefix='.preview-preflight-', dir=ROOT / 'tests') as folder:
            root = Path(folder)
            for path, content in case['files'].items():
                (root / path).write_text(content)
            (root / 'preview.mjs').write_text(source)
            if contract:
                shutil.copyfile(ROOT / 'tests/fixtures/preview_contract.test.mjs', root / 'contract.test.mjs')
            result = subprocess.run(['node', '--test', '--test-reporter=tap'], cwd=root,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual((root / 'preview.test.mjs').read_text(), case['files']['preview.test.mjs'])
            self.assertEqual((root / 'requirements.md').read_text(), case['files']['requirements.md'])
            return result.returncode, result.stdout + result.stderr

    def test_original_and_correct_preserve_existing_tests(self):
        original = json.loads((ROOT / 'benchmarks/hostage-javascript-preview-cases.json').read_text())[0]['files']['preview.mjs']
        for source in (original, CORRECT):
            code, output = self.execute(source, contract=False)
            self.assertEqual(code, 0, output)
            self.assertIn('# pass 2', output)

    def test_full_contract_passes(self):
        code, output = self.execute(CORRECT)
        self.assertEqual(code, 0, output)
        self.assertIn('# tests 18', output)
        self.assertIn('# pass 18', output)

    def test_faults_produce_native_assertions_not_hangs(self):
        variants = {
            'stale_success': CORRECT.replace("if (generation === this.generation) this.state = { status: 'ready'", "this.state = { status: 'ready'"),
            'stale_error': CORRECT.replace("if (generation === this.generation) this.state = { status: 'error'", "this.state = { status: 'error'"),
            'shared_generation': CORRECT.replace('++this.generation', '(this.generation = 1)'),
            'wrong_signal': CORRECT.replace('decode(bytes, signal)', 'decode(bytes, undefined)'),
            'lost_value': CORRECT.replace("status: 'loading', value: this.state.value", "status: 'loading', value: null"),
            'global_owner': 'let globalGeneration = 0;\n' + CORRECT.replace('this.generation', 'globalGeneration'),
            'skip_stale_decode': CORRECT.replace('      const value = await decode',
                '      if (generation !== this.generation) return undefined;\n      const value = await decode'),
        }
        for name, source in variants.items():
            with self.subTest(name=name):
                code, output = self.execute(source)
                self.assertEqual(code, 1, output)
                self.assertIn('ERR_ASSERTION', output)
                self.assertIn('actual', output)
                self.assertIn('expected', output)
                self.assertNotIn('preview contract deadline', output)
                self.assertIn('# tests 18', output)
                self.assertIn('# cancelled 0', output)
                self.assertIn('# skipped 0', output)
