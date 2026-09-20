import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_korean_auto_01 as screen
from runner_snapshot_support import controlled_bundle_git, require_history, assert_pinned_bundle


class KoreanAutoRunnerTests(unittest.TestCase):
    def test_real_pinned_bundle(self):
        require_history(self, ROOT, [screen.RESOURCE])
        with tempfile.TemporaryDirectory() as scratch, patch.object(screen,'OUTPUT',Path(scratch)/'screen'), patch.object(screen,'preflight',return_value={}):
            with patch.object(sys,'argv',['screen']): screen.main()
            assert_pinned_bundle(self, ROOT, screen.OUTPUT/'auto', screen.RESOURCE)

    def test_ten_auto_sessions_install_all_eight_and_cannot_restart(self):
        with controlled_bundle_git(screen, screen.RESOURCE), tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / 'screen'
            result = dict(completed=True, timed_out=False, limit_detected=False,
                          usage={}, elapsed_seconds=1)
            with patch.object(screen, 'OUTPUT', output), \
                    patch.object(screen, 'preflight', return_value={'exit_code': 0}), \
                    patch.object(screen.run, 'disabled_skills', return_value=[]), \
                    patch.object(screen.run, 'run_cell', return_value=result) as execute:
                with patch.object(sys, 'argv', ['screen']): screen.main()
                execute.assert_not_called()
                self.assertEqual(len(list((output / 'auto/skills').glob('*/SKILL.md'))), 8)
                with patch.object(sys, 'argv', ['screen', '--execute']):
                    screen.main()
                    with self.assertRaises(FileExistsError): screen.main()
                self.assertEqual(execute.call_count, 10)
                for call in execute.call_args_list:
                    self.assertEqual(call.args[1], 'auto')
                    self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 240))
                    self.assertTrue(call.kwargs['persist_session'])
                manifest = json.loads((output / 'run.json').read_text())
                self.assertEqual(manifest['resource_revision'], 'unit-fixture-'+screen.RESOURCE)
                self.assertEqual([c['case'] for c in manifest['completed_cells']], manifest['schedule'])

    def test_changed_skill_is_rejected_before_any_model_call(self):
        with controlled_bundle_git(screen, screen.RESOURCE), tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / 'screen'
            with patch.object(screen, 'OUTPUT', output), \
                    patch.object(screen, 'preflight', return_value={'exit_code': 0}), \
                    patch.object(screen.run, 'run_cell') as execute:
                with patch.object(sys, 'argv', ['screen']): screen.main()
                (output / 'auto/skills/friday/SKILL.md').write_text('changed')
                with patch.object(sys, 'argv', ['screen', '--execute']):
                    with self.assertRaisesRegex(ValueError, 'inputs/resources changed'): screen.main()
                execute.assert_not_called()
                self.assertFalse((output / 'execution-started.json').exists())
