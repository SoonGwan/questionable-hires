import tempfile
from pathlib import Path
import unittest
from bridge import refresh as publish

ROOT = Path(__file__).resolve().parents[1]


class SuccessTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(scratch.cleanup)
        self.target = Path(scratch.name) / 'active.json'
        self.target.write_bytes(b'previous manifest\n')

    def test_success(self):
        self.assertEqual(publish(self.target, {'version': 2, 'routes': ['/']}), {'published': 2})

    def test_unicode_success(self):
        self.assertEqual(publish(self.target, {'version': 3, 'routes': ['/서울', '/café']}), {'published': 3})
