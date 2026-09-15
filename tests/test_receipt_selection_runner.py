import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run_receipt_selection_01 as probe


class ReceiptSelectionRunnerTests(unittest.TestCase):
    def test_prepare_and_execute_once_with_all_six_original_slots(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'probe'
            result = dict(completed=True, timed_out=False, limit_detected=False,
                          usage={}, elapsed_seconds=1)
            with patch.object(probe, 'OUTPUT', output), \
                    patch.object(probe, 'preflight', return_value={'exit_code': 0}), \
                    patch.object(probe.run, 'disabled_skills', return_value=[]), \
                    patch.object(probe.run, 'run_cell', return_value=result) as execute:
                with patch.object(sys, 'argv', ['probe']):
                    probe.main()
                execute.assert_not_called()
                with patch.object(sys, 'argv', ['probe', '--execute']):
                    probe.main()
                    with self.assertRaises(FileExistsError):
                        probe.main()
                self.assertEqual(execute.call_count, 6)
                manifest = json.loads((output/'run.json').read_text())
                self.assertEqual([(c['case'], c['condition']) for c in manifest['completed_cells']],
                                 [(c['case'], c['condition']) for c in manifest['schedule']])
                for call in execute.call_args_list:
                    self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
                    self.assertTrue(call.kwargs['persist_session'])

    def test_changed_resources_reject_before_model_or_marker(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'probe'
            with patch.object(probe, 'OUTPUT', output), \
                    patch.object(probe, 'preflight', return_value={'exit_code': 0}), \
                    patch.object(probe.run, 'run_cell') as execute:
                with patch.object(sys, 'argv', ['probe']):
                    probe.main()
                (output/'candidate/skills/receipt/SKILL.md').write_text('changed')
                with patch.object(sys, 'argv', ['probe', '--execute']):
                    with self.assertRaisesRegex(ValueError, 'inputs/resources changed'):
                        probe.main()
                execute.assert_not_called()
                self.assertFalse((output/'execution-started.json').exists())
