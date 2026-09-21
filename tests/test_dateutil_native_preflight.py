"""Offline source-identity checks for the optional real-project preflight."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('dateutil_preflight',
    Path(__file__).resolve().parents[1] / 'benchmarks/preflight_dateutil_native_01.py')
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


class DateutilSourceIdentityTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.body = b'original\n'
        self.file = self.root / 'source.py'
        self.file.write_bytes(self.body)
        blob = hashlib.sha1(b'blob 9\0' + self.body).hexdigest()
        self.blobs = patch.object(preflight, 'BLOBS', {'source.py': blob})
        self.blobs.start()
        self.addCleanup(self.blobs.stop)
        self.revision = patch.object(preflight.subprocess, 'check_output',
                                     return_value=preflight.REVISION + '\n')
        self.git = self.revision.start()
        self.addCleanup(self.revision.stop)

    def test_original_bytes_accepted_without_execution(self):
        self.assertEqual(preflight.load_source(self.root), {'source.py': self.body})

    def test_changed_bytes_or_revision_rejected(self):
        self.file.write_bytes(b'changed\n')
        with self.assertRaisesRegex(ValueError, 'Changed upstream file'):
            preflight.load_source(self.root)
        self.file.write_bytes(self.body)
        self.git.return_value = 'different-revision\n'
        with self.assertRaisesRegex(ValueError, 'Wrong upstream revision'):
            preflight.load_source(self.root)

    def test_symlink_rejected_even_with_identical_contents(self):
        target = self.root / 'target.py'
        self.file.rename(target)
        self.file.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'Not a regular upstream file'):
            preflight.load_source(self.root)
