import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_artifact_audit_01 as probe


class ArtifactAuditRunnerTests(unittest.TestCase):
    def test_prepare_has_no_model_calls_then_executes_each_slot_once(self):
        with tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / 'probe'
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
                self.assertEqual(execute.call_count, 3)
                manifest = json.loads((output / 'run.json').read_text())
                self.assertEqual([c['condition'] for c in manifest['completed_cells']],
                                 list(probe.SCHEDULE))
                self.assertTrue(all(c.kwargs['persist_session'] for c in execute.call_args_list))

    def test_changed_snapshot_rejects_before_execution(self):
        with tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / 'probe'
            with patch.object(probe, 'OUTPUT', output), \
                    patch.object(probe, 'preflight', return_value={'exit_code': 0}), \
                    patch.object(probe.run, 'run_cell') as execute:
                with patch.object(sys, 'argv', ['probe']):
                    probe.main()
                (output / 'candidate/skills/con-artist/SKILL.md').write_text('changed')
                with patch.object(sys, 'argv', ['probe', '--execute']):
                    with self.assertRaisesRegex(ValueError, 'inputs/resources changed'):
                        probe.main()
                execute.assert_not_called()
                self.assertFalse((output / 'execution-started.json').exists())
