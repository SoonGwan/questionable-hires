import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_input_budget', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class AuditInputBudgetTests(unittest.TestCase):
    def test_final_comparison_detects_growth_without_reading_the_entire_new_file(self):
        with tempfile.TemporaryDirectory(prefix='audit-input-', dir=ROOT / 'benchmarks') as temporary:
            source = Path(temporary) / 'data.bin'
            source.write_bytes(b'x')
            mode = source.stat().st_mode & 0o777
            real_open, reads = Path.open, []
            class Reader:
                def __enter__(self):
                    self.stream = real_open(source, 'rb')
                    return self
                def read(self, size=-1):
                    reads.append(size)
                    return self.stream.read(size)
                def __exit__(self, *args):
                    self.stream.close()
            def growing_open(path, *args, **kwargs):
                if path == source and args == ('rb',):
                    with real_open(source, 'wb') as stream:
                        stream.write(b'x' * 20_000_001)
                    return Reader()
                return real_open(path, *args, **kwargs)
            with patch.object(Path, 'open', growing_open):
                self.assertFalse(helper.original_matches(source, b'x', mode))
            self.assertEqual(reads, [2])
            self.assertEqual(source.stat().st_size, 20_000_001)
            with patch.object(Path, 'open') as opened:
                self.assertFalse(helper.original_matches(source, b'x', mode))
                opened.assert_not_called()

    def test_growth_after_stat_is_rejected_with_bounded_read(self):
        with tempfile.TemporaryDirectory(prefix='audit-input-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            source = root / 'data.bin'
            source.write_bytes(b'x')
            real_open = Path.open
            reads = []
            class Reader:
                def __enter__(self):
                    self.stream = real_open(source, 'rb')
                    return self
                def read(self, size=-1):
                    reads.append(size)
                    return self.stream.read(size)
                def __exit__(self, *args):
                    self.stream.close()
            def growing_open(path, *args, **kwargs):
                if path == source and args == ('rb',):
                    with real_open(source, 'wb') as stream:
                        stream.write(b'x' * 20_000_001)
                    return Reader()
                return real_open(path, *args, **kwargs)
            with patch.object(Path, 'open', growing_open):
                with self.assertRaisesRegex(ValueError, '20 MB'):
                    helper.snapshot(root, ['data.bin'])
            self.assertEqual(reads, [20_000_001])
            self.assertEqual(source.stat().st_size, 20_000_001)

    def test_shared_budget_charges_bytes_actually_read_after_growth(self):
        with tempfile.TemporaryDirectory(prefix='audit-input-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            first, second = root / 'first.bin', root / 'second.bin'
            first.write_bytes(b'x')
            second.write_bytes(b'y' * 10_000_000)
            real_open = Path.open
            def growing_open(path, *args, **kwargs):
                if path == first and args == ('rb',):
                    with real_open(first, 'wb') as stream:
                        stream.write(b'x' * 10_000_001)
                return real_open(path, *args, **kwargs)
            with patch.object(Path, 'open', growing_open):
                with self.assertRaisesRegex(ValueError, '20 MB'):
                    helper.snapshot(root, ['first.bin', 'second.bin'])

    def test_exact_limit_and_overlapping_selections_preserve_content(self):
        with tempfile.TemporaryDirectory(prefix='audit-input-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            (root / 'pkg').mkdir()
            content = b'x' * 20_000_000
            (root / 'pkg/data.bin').write_bytes(content)
            self.assertEqual(helper.snapshot(root, ['pkg', 'pkg/data.bin']), {'pkg/data.bin': content})
