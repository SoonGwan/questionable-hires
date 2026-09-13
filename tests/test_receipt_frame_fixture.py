import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'benchmarks/receipt-frame-cases.json'

# Author-only witness; never copied into the model input.
AFTER = '''class Decoder:
    def __init__(self):
        self.pending = bytearray()

    def feed(self, chunk):
        self.pending.extend(chunk)
        messages = []
        while len(self.pending) >= 2:
            size = int.from_bytes(self.pending[:2], 'big')
            if len(self.pending) < size + 2:
                break
            messages.append(bytes(self.pending[2:size + 2]))
            del self.pending[:size + 2]
        return messages
'''


class FrameFixtureTests(unittest.TestCase):
    def test_actual_before_failures_and_unchanged_after_suite(self):
        case, = json.loads(CASES.read_text())
        for variant in ('before', 'after'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, content in case['files'].items():
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                if variant == 'after':
                    (root / 'packet.py').write_text(AFTER)
                process = subprocess.run([sys.executable, '-B', '-m', 'unittest',
                                          'discover', '-s', 'tests', '-v'], cwd=root,
                                         capture_output=True, text=True, timeout=10)
                output = process.stdout + process.stderr
                self.assertEqual(process.returncode, 1 if variant == 'before' else 0, output)
                self.assertIn('Ran 5 tests', output)
                if variant == 'before':
                    self.assertIn('FAILED (failures=2)', output)
                    self.assertIn("[] != [b'hello']", output)
                    self.assertIn("[] != [b'world', b'last']", output)
                else:
                    self.assertIn('OK', output)
                for name, content in case['files'].items():
                    if name != 'packet.py':
                        self.assertEqual((root / name).read_text(), content)
                self.assertEqual({str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()},
                                 set(case['files']))
