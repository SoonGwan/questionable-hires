import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class RuntimeFixtureTests(unittest.TestCase):
    def test_fixture_reproduces_import_timing_not_random_retries(self):
        path = Path(__file__).resolve().parents[1] / 'benchmarks/exorcist-runtime-cases.json'
        case = json.loads(path.read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in case['files'].items():
                (root / name).write_text(content)
            env = dict(os.environ)
            env.pop('REQUEST_RETRIES', None)
            env.pop('PYTHONPATH', None)
            env.pop('PYTHONOPTIMIZE', None)
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_worker'],
                                    cwd=root, env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertIn('AssertionError: 3 != 1', result.stderr)
            probe = """import worker
calls = []
def send():
    calls.append('attempt')
    raise RuntimeError('offline failure')
try:
    worker.deliver(send)
except RuntimeError:
    pass
assert worker.RETRIES == 0
assert len(calls) == 1
print('one callback')
"""
            env['REQUEST_RETRIES'] = '0'
            result = subprocess.run([sys.executable, '-B', '-c', probe], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), 'one callback')
            for name, content in case['files'].items():
                self.assertEqual((root / name).read_text(), content)


if __name__ == '__main__':
    unittest.main()
