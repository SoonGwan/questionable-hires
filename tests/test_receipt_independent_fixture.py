import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('independent_cases', ROOT / 'benchmarks/receipt_independent_cases.py')
FIXTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXTURE)


class ReceiptIndependentFixtureTests(unittest.TestCase):
    def test_fix_does_not_remove_independent_packaging_failure(self):
        case = FIXTURE.cases()[0]
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for name, content in case['files'].items():
                (root / name).write_text(content)
            def checks():
                return [subprocess.run([sys.executable, '-B', *args], cwd=root,
                    capture_output=True, text=True, timeout=5) for args in
                    (['-m', 'unittest', '-v'], ['check_manifest.py'], ['check_example.py'])]
            before = checks()
            self.assertEqual([r.returncode for r in before], [1, 1, 1])
            self.assertIn('AssertionError', before[0].stderr)
            target = root / 'render.py'
            target.write_text('def render(lines):\n    return "\\n".join(lines) + "\\n" if lines else ""\n')
            after = checks()
            self.assertEqual([r.returncode for r in after], [0, 1, 0])
            self.assertIn('missing NOTICE', after[1].stdout)
            self.assertIn('Example rendering: OK', after[2].stdout)
            namespace = {}
            exec(compile(target.read_text(), 'render.py', 'exec'), namespace)
            self.assertEqual(namespace['render'](['']), '\n')
            for name, content in case['files'].items():
                if name != 'render.py':
                    self.assertEqual((root / name).read_text(), content)
            self.assertFalse((root / 'NOTICE').exists())
