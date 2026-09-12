import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
try:
    spec = importlib.util.spec_from_file_location(
        'run_mother_in_law_fast', ROOT / 'benchmarks/run_mother_in_law_fast.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
finally:
    sys.path.pop(0)


class MotherInLawFastRunnerTests(unittest.TestCase):
    def test_dry_run_materializes_five_cases_without_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            with mock.patch.object(sys, 'argv', [
                    'run_mother_in_law_fast.py', '--output', str(output),
                    '--dry-run']), mock.patch('builtins.print'):
                self.assertEqual(runner.main(), 0)
            plan = json.loads((output / 'plan.json').read_text())
            self.assertEqual(len(plan['cases']), 5)
            self.assertEqual(plan['session_count'], 10)
            self.assertEqual(len(json.loads((output / 'generic-cases.json').read_text())), 4)
            self.assertEqual(len(plan['commands']), 2)

    def test_case_and_arm_filters_bound_iteration(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            with mock.patch.object(sys, 'argv', [
                    'run_mother_in_law_fast.py', '--output', str(output),
                    '--dry-run', '--case', 'search-protected', '--arms', 'skill']), \
                    mock.patch('builtins.print'):
                self.assertEqual(runner.main(), 0)
            plan = json.loads((output / 'plan.json').read_text())
            self.assertEqual([case['id'] for case in plan['cases']], ['search-protected'])
            self.assertEqual(plan['session_count'], 1)
            self.assertEqual(len(plan['commands']), 1)


if __name__ == '__main__':
    unittest.main()
