from pathlib import Path
import sys
import tempfile
import unittest

BENCHMARKS = Path(__file__).resolve().parents[1] / 'benchmarks'
sys.path.insert(0, str(BENCHMARKS))
import prepare_httpx_receipt as fixture


class HttpxReceiptFixtureTests(unittest.TestCase):
    def test_rejects_output_inside_source_before_copying_or_git(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'nested'
            with self.assertRaisesRegex(ValueError, 'inside the original'):
                fixture.prepare(root, Path(sys.executable), output)
            self.assertFalse(output.exists())

    def test_seed_is_unique_and_does_not_change_adjacent_operations(self):
        correct = 'return self.copy_with(params=self.params.set(key, value))'
        neighbor = 'return self.copy_with(params=self.params.remove(key))'
        source = correct + '\n' + neighbor
        self.assertEqual(fixture.seeded_source(source),
                         'return self.copy_with(params=self.params.add(key, value))\n' + neighbor)
        for invalid in ('', neighbor, correct + '\n' + correct):
            with self.subTest(source=invalid), self.assertRaisesRegex(ValueError, 'exactly one'):
                fixture.seeded_source(invalid)
