import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('friday_config_fixture', ROOT / 'benchmarks/friday_config_cases.py')
fixture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixture)


class ConfigReleaseFixtureTests(unittest.TestCase):
    def test_frozen_files_and_nested_contract_remain_model_visible(self):
        cases = fixture.cases()
        self.assertEqual(cases, json.loads((ROOT / 'benchmarks/friday-config-cases.json').read_text()))
        for case in cases:
            files = case['files']
            self.assertNotIn('test_release.py', files)
            plan = json.loads(files['ops/releases/current.json'])
            for phase in plan['phases']:
                self.assertIn(phase['config'], files)
                for name in phase['active']:
                    self.assertIn(plan['consumers'][name], files)
            self.assertIn('services/worker/AGENTS.md', files)
            self.assertIn('ops/AGENTS.md', files)

    def test_native_values_fail_without_exceptions_and_final_recovery_survives(self):
        observed = fixture.preflight()
        self.assertEqual([r['exit_code'] for r in observed], [0, 1])
        self.assertIn("rollback overlap old {'timeout_ms': 1000, 'attempts': 4}", observed[1]['output'])
        self.assertIn('FAILED (failures=1)', observed[1]['output'])
