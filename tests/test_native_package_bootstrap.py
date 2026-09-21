"""A green unittest selector need not prove a clean package import works."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROBE = '''import sys
print('ATTEMPT', 'demo' in sys.modules, 'demo.util' in sys.modules, flush=True)
from demo.util import value
import unittest

class Probe(unittest.TestCase):
    def test_value(self):
        self.assertEqual(value, 17)
'''


class NativePackageBootstrapTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        package = self.root / 'demo'
        package.mkdir()
        (package / '__init__.py').write_text('from . import util\nfrom .generated import version\n')
        (package / 'util.py').write_text('value = 17\n')
        (self.root / 'test_probe.py').write_text(PROBE)

    def invoke(self, *args):
        return subprocess.run([sys.executable, '-B', *args], cwd=self.root,
            env=dict(os.environ, PYTHONPATH=str(self.root), PYTHONDONTWRITEBYTECODE='1'),
            capture_output=True, text=True, timeout=10)

    def test_partial_module_cache_masks_missing_generated_metadata(self):
        direct = self.invoke('-c', 'import demo')
        self.assertNotEqual(direct.returncode, 0)
        self.assertIn("No module named 'demo.generated'", direct.stderr)
        naive = self.invoke('-m', 'unittest', 'test_probe.Probe.test_value', '-v')
        self.assertEqual(naive.returncode, 0, naive.stderr)
        self.assertIn('Ran 1 test', naive.stderr)
        self.assertEqual(naive.stdout.splitlines(), ['ATTEMPT False False', 'ATTEMPT False True'])
        (self.root / 'test_probe.py').write_text(PROBE + '\nimport demo\n')
        strict = self.invoke('-m', 'unittest', 'test_probe.Probe.test_value', '-v')
        self.assertNotEqual(strict.returncode, 0)
        self.assertIn('FAILED (errors=1)', strict.stderr)
        self.assertIn("No module named 'demo.generated'", strict.stderr)

    def test_valid_metadata_passes_clean_import_and_native_test(self):
        (self.root / 'demo/generated.py').write_text("version = '1.0'\n")
        direct = self.invoke('-c', 'import demo; assert demo.version == "1.0"')
        self.assertEqual(direct.returncode, 0, direct.stderr)
        native = self.invoke('-m', 'unittest', 'test_probe.Probe.test_value', '-v')
        self.assertEqual(native.returncode, 0, native.stderr)
        self.assertIn('Ran 1 test', native.stderr)
        self.assertEqual(native.stdout.splitlines(), ['ATTEMPT False False'])
