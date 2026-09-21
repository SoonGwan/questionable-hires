import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from hostage_conditional_cases import SHARED_FIXED
from probe_completed_fetch_gap import observe


class CompletedFetchGapTests(unittest.TestCase):
    def test_native_completed_window_rejects_reference_and_accepts_fresh_fetch(self):
        self.assertEqual(SHARED_FIXED.count('if task is None:'), 1)
        corrected = SHARED_FIXED.replace('if task is None:', 'if task is None or task.done():')
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'shared.py'
            for body, exit_code, calls in ((SHARED_FIXED, 1, 1), (corrected, 0, 2)):
                source.write_text(body)
                result = observe(source)
                self.assertEqual(result['exit_code'], exit_code, result)
                observation = json.loads(result['output'])
                self.assertEqual(observation['original_fetch_already_done'], [True])
                self.assertEqual(observation['calls'], calls)
                self.assertEqual(observation['same_object'], bool(exit_code))
                if exit_code:
                    self.assertIn('Completed fetch result reused by a new caller', result['stderr'])
                else:
                    self.assertEqual(result['stderr'], '')
                self.assertEqual(source.read_text(), body)
