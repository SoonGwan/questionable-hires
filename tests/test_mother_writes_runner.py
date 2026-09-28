"""Reuse scheduling/stop controls and verify the isolated added asset boundary."""
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_mother_writes_01 as runner
import test_mother_support_fit_01 as controls


class MotherWritesRunnerTests(controls.MotherSupportFitTests):
    def setUp(self):
        replacement = patch.object(controls, 'runner', runner.base)
        replacement.start()
        self.addCleanup(replacement.stop)
        super().setUp()

    def test_only_entry_body_changes_and_metadata_links_survive(self):
        runner.base.driver.base.prepare(self.output)
        roots = [self.output / arm / 'skills/mother-in-law' for arm in ('previous', 'candidate')]
        manifests = [runner.base.driver.base.run.resource_manifest(root) for root in roots]
        self.assertEqual(set(manifests[1]) - set(manifests[0]), {'assets/controlled_writes.py'})
        self.assertEqual(set(manifests[0]) - set(manifests[1]), set())
        self.assertEqual([n for n in manifests[0] if manifests[0][n] != manifests[1][n]], ['SKILL.md'])
        before, after = [(root / 'SKILL.md').read_text() for root in roots]
        self.assertEqual(before.split('\n---\n')[0], after.split('\n---\n')[0])
        self.assertEqual((roots[1] / 'assets/controlled_writes.py').read_bytes(),
                         (ROOT / 'benchmarks/candidates/mother-writes01/controlled_writes.py').read_bytes())
