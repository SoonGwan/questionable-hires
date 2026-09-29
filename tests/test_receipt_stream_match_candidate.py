"""Native exact-byte and race controls for an unadopted memory prototype."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from receipt_stream_match_candidate import transform


class StreamingMatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        path = self.root / 'compare.py'
        path.write_text(transform((ROOT / 'skills/receipt/scripts/compare.py').read_text()))
        spec = importlib.util.spec_from_file_location('stream_receipt', path)
        self.helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.helper)

    def test_exact_comparison_retains_growth_truncation_and_boundary_differences(self):
        path = self.root / 'input'
        for size in (0, 1, 65535, 65536, 65537, 131073):
            original = b'x' * size
            cases = [('same', original, True), ('growth', original + b'y', False)]
            if size:
                cases += [('truncated', original[:-1], False), ('last byte', original[:-1] + b'y', False)]
            if size > 65536:
                cases += [('boundary', original[:65536] + b'y' + original[65537:], False)]
            for label, value, matches in cases:
                with self.subTest(size=size, mutation=label):
                    path.write_bytes(value)
                    self.assertIs(self.helper.content_matches(path, original), matches)
                    self.assertEqual(path.read_bytes(), value)

    def test_final_reads_are_bounded_even_when_file_grows(self):
        path = self.root / 'input'
        original = b'x' * 131073
        path.write_bytes(original + b'y' * 100000)
        calls = []
        fdopen = os.fdopen
        class Stream:
            def __init__(self, stream): self.stream = stream
            def __enter__(self): return self
            def __exit__(self, *args): return self.stream.__exit__(*args)
            def fileno(self): return self.stream.fileno()
            def read(self, count):
                value = self.stream.read(count)
                calls.append((count, len(value)))
                return value
        with patch.object(self.helper.os, 'fdopen', side_effect=lambda *args: Stream(fdopen(*args))):
            self.assertFalse(self.helper.content_matches(path, original))
        self.assertTrue(all(0 < requested <= 65536 for requested, _ in calls))
        self.assertEqual(sum(count for _, count in calls), len(original) + 1)

    def test_replaced_inode_and_symlink_are_rejected(self):
        selected = self.root / 'input'
        external = self.root / 'other'
        external.write_bytes(b'original')
        original_open = os.open
        for kind in ('regular', 'symlink', 'fifo'):
            with self.subTest(kind=kind):
                selected.unlink(missing_ok=True)
                selected.write_bytes(b'original')
                def replace(path, *args, **kwargs):
                    if path == selected:
                        selected.rename(self.root / ('old-' + kind))
                        if kind == 'symlink': selected.symlink_to(external)
                        elif kind == 'fifo': os.mkfifo(selected)
                        else: selected.write_bytes(b'original')
                    return original_open(path, *args, **kwargs)
                with patch.object(self.helper.os, 'open', side_effect=replace):
                    with self.assertRaises((ValueError, OSError)):
                        self.helper.content_matches(selected, b'original')


if __name__ == '__main__':
    unittest.main()
