"""Reuse all guarded scheduler controls with the actual reference-routing adapter."""
import test_receipt_guide_first_runner as controls
from run_receipt_optional_detail_01 import driver

class OptionalDetailScheduleTests(controls.GuideRunnerTests):
    def setUp(self):
        original=controls.driver
        controls.driver=driver
        self.addCleanup(setattr,controls,'driver',original)
        super().setUp()
