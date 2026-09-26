import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run_namespace_surface_01 as runner

class NamespaceControls(unittest.TestCase):
    def test_frozen_flags_are_independent_and_drift_stops_before_model(self):
        with tempfile.TemporaryDirectory() as d, patch.object(runner.base,'preflight',return_value={}), patch.object(runner.base.subprocess,'check_output',return_value='synthetic version'), patch.object(runner.base.run,'run_cell') as cell:
            out=Path(d)/'run';manifest=runner.base.prepare(out)
            self.assertEqual(manifest['schedule'],['apps_only','apps_excluded'])
            self.assertEqual(manifest['flags'],runner.base.FLAGS)
            runner.base.FLAGS['apps_excluded'].append('--synthetic-drift')
            try:
                with self.assertRaisesRegex(ValueError,'Frozen'):
                    runner.base.execute(out,manifest)
                cell.assert_not_called()
                self.assertFalse((out/'execution-started.json').exists())
            finally:runner.base.FLAGS['apps_excluded'].pop()

if __name__=='__main__':unittest.main()
