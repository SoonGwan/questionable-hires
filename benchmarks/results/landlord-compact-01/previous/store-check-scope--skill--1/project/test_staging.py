import json
from pathlib import Path
import unittest

class StagingReceipt(unittest.TestCase):
    def test_provisioned_backend(self):
        receipt = json.loads(Path('staging-receipt.json').read_text())
        self.assertIs(receipt['contract_passed'], True)
