import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('receipt_profile_cases', ROOT / 'benchmarks/receipt_profile_cases.py')
FIXTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXTURE)


class ReceiptProfileFixtureTests(unittest.TestCase):
    def test_suite_success_requires_executed_regression(self):
        for case in FIXTURE.cases():
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as scratch:
                project = Path(scratch)
                for name, content in case['files'].items():
                    (project / name).write_text(content)
                frozen = (project / 'test_assembly.py').read_bytes()

                def run(enabled):
                    env = {k: v for k, v in os.environ.items() if k != 'ARCHIVE_CHECKS'}
                    if enabled:
                        env['ARCHIVE_CHECKS'] = '1'
                    return subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v'],
                        cwd=project, env=env, capture_output=True, text=True, timeout=5)

                gated = case['id'].endswith('gated')
                default = run(False)
                self.assertEqual(default.returncode, 0 if gated else 1, default.stderr)
                if gated:
                    self.assertIn('OK (skipped=1)', default.stderr)
                before = run(True)
                self.assertEqual(before.returncode, 1, before.stderr)
                self.assertIn("'onetentwo' != 'onetwoten'", before.stderr)
                target = project / 'assembly.py'
                target.write_text(target.read_text().replace(
                    "sorted(directory.glob('part-*.txt'))",
                    "sorted(directory.glob('part-*.txt'), key=lambda path: int(path.stem[5:]))"))
                after = run(True)
                self.assertEqual(after.returncode, 0, after.stderr)
                self.assertIn('test_long_document', after.stderr)
                self.assertNotIn('skipped', after.stderr)
                self.assertEqual((project / 'test_assembly.py').read_bytes(), frozen)
