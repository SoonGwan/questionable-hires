import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'featured_benchmark_sync', ROOT / 'scripts/sync_featured_benchmark.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class FeaturedBenchmarkSyncTests(unittest.TestCase):
    def test_both_readmes_match_featured_dataset(self):
        value = sync.values()
        for name, language in (('README.md', 'en'), ('README.ko.md', 'ko')):
            current = (ROOT / name).read_text()
            self.assertEqual(current, sync.synchronized(current, sync.block(language, value)))

    def test_rejects_missing_or_duplicate_markers(self):
        with self.assertRaises(ValueError):
            sync.synchronized('no markers', 'replacement')
        with self.assertRaises(ValueError):
            sync.synchronized(sync.START * 2 + sync.END, 'replacement')


if __name__ == '__main__':
    unittest.main()
