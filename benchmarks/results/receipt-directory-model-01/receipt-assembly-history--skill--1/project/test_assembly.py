import tempfile
import unittest
from assembly.service import assemble

class AssemblyTests(unittest.TestCase):
    def test_numeric_order(self):
        self.assertEqual(assemble('samples'), 'one|two|ten\n')
    def test_empty(self):
        with tempfile.TemporaryDirectory(dir='.') as empty:
            self.assertEqual(assemble(empty), '')
