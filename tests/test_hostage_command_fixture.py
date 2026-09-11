import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class HostageCommandFixtureTests(unittest.TestCase):
    def test_documented_loader_runs_real_checks_and_regression_detects_fault(self):
        source = Path(__file__).resolve().parents[1] / 'benchmarks/hostage-command-cases.json'
        case = json.loads(source.read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in case['files'].items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)

            def run(*args):
                return subprocess.run([sys.executable, '-B', '-m', 'unittest', *args],
                                      cwd=root, capture_output=True, text=True, timeout=5)

            default = run('discover', '-v')
            self.assertEqual(default.returncode, 0, default.stderr)
            self.assertIn('Ran 0 tests', default.stderr)
            command = ('discover', '-s', 'verification', '-p', 'check_*.py', '-v')
            existing = run(*command)
            self.assertEqual(existing.returncode, 0, existing.stderr)
            self.assertIn('Ran 3 tests', existing.stderr)
            check = root / 'verification/check_retry.py'
            check.write_text(check.read_text() + '''
    def test_exact_limit(self):
        for limit in (0, 1, 3, 100):
            with self.subTest(limit=limit):
                self.assertIs(should_retry(limit, limit), False)
''')
            before = run(*command)
            self.assertEqual(before.returncode, 1, before.stderr)
            self.assertIn('FAILED (failures=4)', before.stderr)
            implementation = root / 'retry.py'
            implementation.write_text(implementation.read_text().replace('failures <= limit', 'failures < limit'))
            after = run(*command)
            self.assertEqual(after.returncode, 0, after.stderr)
            self.assertIn('Ran 4 tests', after.stderr)
            for name in ('README.md', 'branding.txt'):
                self.assertEqual((root / name).read_text(), case['files'][name])


if __name__ == '__main__':
    unittest.main()
