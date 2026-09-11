import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class SignalFixtureTests(unittest.TestCase):
    def test_actual_callback_completion_distinguishes_signal_order(self):
        cases = json.loads((Path(__file__).resolve().parents[1] /
                            'benchmarks/exorcist-signal-cases.json').read_text())
        code = '''from worker import process
def notify(done):
    done()
    print('callback completed', flush=True)
print(process(notify), flush=True)
'''
        for case in cases:
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, content in case['files'].items():
                    (root / name).write_text(content)
                if case['id'] == 'signal-lost':
                    with self.assertRaises(subprocess.TimeoutExpired) as caught:
                        subprocess.run([sys.executable, '-B', '-c', code], cwd=root,
                                       capture_output=True, timeout=1)
                    self.assertEqual(caught.exception.stdout, b'callback completed\n')
                else:
                    result = subprocess.run([sys.executable, '-B', '-c', code], cwd=root,
                                            capture_output=True, text=True, timeout=1)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, 'callback completed\ndone\n')
                for name, content in case['files'].items():
                    self.assertEqual((root / name).read_text(), content)


if __name__ == '__main__':
    unittest.main()
