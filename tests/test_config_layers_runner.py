"""Apply the existing schedule contracts to the privately configured driver."""
from unittest.mock import patch
import test_packaging_specifier_runner as contracts
import run_config_layers_01 as configured


class ConfigScheduleTests(contracts.SpecifierScheduleTests):
    def setUp(self):
        change = patch.object(contracts, 'runner', configured.driver)
        change.start()
        self.addCleanup(change.stop)
        super().setUp()


class ConfigPinnedResourceTests(contracts.SpecifierPinnedResourceTests):
    def setUp(self):
        change = patch.object(contracts, 'runner', configured.driver)
        change.start()
        self.addCleanup(change.stop)
