"""Reuse all guarded scheduler controls with the assertion API adapter."""
import test_receipt_guide_first_runner as controls
from run_receipt_assertion_api_01 import driver

class AssertionApiScheduleTests(controls.GuideRunnerTests):
    def setUp(self):
        original=controls.driver
        controls.driver=driver
        self.addCleanup(setattr,controls,'driver',original)
        super().setUp()
