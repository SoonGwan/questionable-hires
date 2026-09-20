from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import hostage_input_cases as fixture
import check_hostage_input_output as replay


class InputOutputReplayTests(unittest.TestCase):
    def test_actual_native_controls_preserve_sources_and_accept_equivalent_normalization(self):
        for mode in ('opaque', 'normalized'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as temp:
                project = Path(temp)
                (project / 'sender.py').write_text(fixture.implementation(mode, fixed=True))
                (project / 'test_sender.py').write_text(fixture.SMOKE)
                (project / 'test_contract.py').write_text(fixture.author_test(mode))
                result = replay.inspect(project, mode)
                self.assertEqual([row['exit_code'] for row in result['rows']],
                                 [0, 1] if mode == 'opaque' else [0, 1, 0])
                for row in result['rows']:
                    self.assertFalse(row['timed_out'])
                    self.assertIn('Ran 6 tests', row['output'])
                    self.assertNotIn('ERROR:', row['output'])
                self.assertIn('AssertionError:', result['rows'][1]['output'])

    def test_unknown_contract_and_symlink_reject_before_execution(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as temp:
            project = Path(temp)
            with self.assertRaises(ValueError): replay.inspect(project, 'unknown')
            (project / 'linked').symlink_to(project / 'absent')
            with self.assertRaises(ValueError): replay.inspect(project, 'opaque')
