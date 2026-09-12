import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'audit_mother_in_law_checkpoint', ROOT / 'benchmarks/audit_mother_in_law_checkpoint.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class MotherInLawCheckpointAuditTests(unittest.TestCase):
    def test_equal_task_summary(self):
        common = dict(cached_input_tokens=0, quality_target_met=True,
                      clean_false_positive=False)
        rows = [
            dict(common, case='a', arm='baseline', input_tokens=90, output_tokens=10, elapsed_seconds=10),
            dict(common, case='a', arm='skill', input_tokens=70, output_tokens=10, elapsed_seconds=8),
            dict(common, case='b', arm='baseline', input_tokens=190, output_tokens=10, elapsed_seconds=20),
            dict(common, case='b', arm='skill', input_tokens=210, output_tokens=10, elapsed_seconds=24),
        ]
        result = audit.summarize(rows)
        self.assertEqual(result['resource_ratios']['total_tokens']['skill'], 95.0)
        self.assertEqual(result['resource_ratios']['elapsed_seconds']['skill'], 100.0)

    def test_rejects_incomplete_pair(self):
        row = dict(case='a', arm='baseline', input_tokens=1, cached_input_tokens=0,
                   output_tokens=0, elapsed_seconds=1, quality_target_met=True,
                   clean_false_positive=False)
        with self.assertRaises(ValueError):
            audit.summarize([row])


if __name__ == '__main__':
    unittest.main()
