"""Native display controls, independent of Git history and model artifacts."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'benchmarks/prototypes/fold_tracebacks.py'
spec = importlib.util.spec_from_file_location('fold_tracebacks', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

FIXTURE = '''import unittest
from pathlib import Path
class Native(unittest.IsolatedAsyncioTestCase):
    async def check(self, expected):
        with Path('calls.txt').open('a') as f:
            f.write(str(expected) + '\\n')
        self.assertEqual('observed', expected)
    async def test_one(self):
        await self.check(EXPECTED_ONE)
    async def test_two(self):
        await self.check(EXPECTED_TWO)
    async def test_three(self):
        await self.check(EXPECTED_THREE)
'''


class DisplayTests(unittest.TestCase):
    def test_native_failures_and_passes_execute_once_and_keep_values(self):
        for passing in (False, True):
            with self.subTest(passing=passing), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = FIXTURE
                for name in ('ONE', 'TWO', 'THREE'):
                    source = source.replace('EXPECTED_' + name, repr('observed' if passing else name))
                (root / 'test_native.py').write_text(source)
                native = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_native'],
                                        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        timeout=10)
                self.assertEqual(native.returncode, 0 if passing else 1)
                self.assertEqual(len((root / 'calls.txt').read_text().splitlines()), 3)
                raw = native.stdout
                full = root / 'output.txt'
                full.write_bytes(raw)
                records = helper.fold(raw.decode())
                self.assertEqual(helper.expand(records).encode(), raw)
                rendered = helper.display(raw, full)
                cli = subprocess.run([sys.executable, '-B', str(SCRIPT), str(full)],
                                     capture_output=True, timeout=10)
                self.assertEqual(cli.returncode, 0)
                self.assertEqual(cli.stdout, rendered)
                self.assertEqual(full.read_bytes(), raw)
                self.assertEqual(len((root / 'calls.txt').read_text().splitlines()), 3)
                self.assertIn(b'Ran 3 tests', rendered)
                for name in ('one', 'two', 'three'):
                    self.assertIn(('test_' + name).encode(), rendered)
                if passing:
                    self.assertEqual(raw, rendered)
                    self.assertIn(b'\nOK\n', rendered)
                else:
                    self.assertLess(len(rendered), len(raw))
                    self.assertIn(b'FAILED (failures=3)', rendered)
                    for name in ('ONE', 'TWO', 'THREE'):
                        self.assertIn(("'observed' != '" + name + "'").encode(), rendered)

    def test_unrecognized_unicode_binary_and_line_endings(self):
        for raw in (b'', b'ordinary output without newline', b'\xff\x00',
                    '실패: 서로 다른 값\r\n'.encode(), b'ExceptionGroup: nested\n  | traceback\n'):
            with self.subTest(raw=raw):
                self.assertEqual(helper.display(raw, 'raw'), raw)
        frame = '  File "' + 'p' * 180 + '", line 1, in check\r\n    run()\r\n'
        block = 'Traceback (most recent call last):\r\n' + frame
        text = block + 'ValueError: first\r\n' + block + 'ValueError: second'
        self.assertEqual(helper.expand(helper.fold(text)), text)
        # Header/path overhead must not expand even a foldable input.
        self.assertEqual(helper.display(text.encode(), 'long-source-' * 1000), text.encode())

    def test_different_frames_are_not_equated(self):
        prefix = 'Traceback (most recent call last):\n  File "'
        text = prefix + 'a' * 200 + '", line 1, in f\nValueError: a\n'
        text += prefix + 'b' * 200 + '", line 1, in f\nValueError: b\n'
        self.assertEqual(helper.display(text.encode(), 'raw'), text.encode())

    def test_invalid_references_and_size_limit_are_explicit(self):
        for ref in ([0, 1], [-1, 0], [True, 1]):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                helper.expand([{'repeat': ref}])
        with self.assertRaisesRegex(ValueError, '1 MiB'):
            helper.display(b'x' * (helper.LIMIT + 1), 'raw')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'raw'
            path.write_bytes(b'x' * (helper.LIMIT + 1))
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(path)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')
            self.assertIn(b'1 MiB', result.stderr)


if __name__ == '__main__':
    unittest.main()
