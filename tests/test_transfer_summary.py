import importlib.util
from pathlib import Path
import sys
import unittest

directory = Path(__file__).resolve().parents[1] / 'benchmarks'
sys.path.insert(0, str(directory))
spec = importlib.util.spec_from_file_location('export_transfer', directory / 'export_transfer.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.path.pop(0)


class TransferSummaryTests(unittest.TestCase):
    def test_failure_stays_in_denominator_and_unknown_is_not_pass(self):
        rows = [dict(condition='candidate', completed=True, scope='pass', criteria=['pass'] * 3, total_tokens=100, elapsed_seconds=10),
                dict(condition='candidate', completed=True, scope='unknown', criteria=['pass'] * 3, total_tokens=200, elapsed_seconds=20),
                dict(condition='candidate', completed=False, scope='pass', criteria=['pass'] * 3, total_tokens=None, elapsed_seconds=240)]
        result = module.summarize(rows)['candidate']
        self.assertEqual(result['scheduled'], 3)
        self.assertEqual(result['completed'], 2)
        self.assertEqual(result['strict_success'], 1)
        self.assertEqual(result['metrics']['total_tokens']['mean'], 150)
        self.assertEqual(result['metrics']['elapsed_seconds']['n'], 2)

    def test_empty_condition_is_not_zero_cost(self):
        result = module.summarize([])['baseline']
        self.assertIsNone(result['metrics']['total_tokens']['mean'])
        self.assertEqual(result['metrics']['total_tokens']['n'], 0)
