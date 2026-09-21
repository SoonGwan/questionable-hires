"""Offline checks: altered upstream inputs cannot silently enter preflight."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('slugify_preflight',
    Path(__file__).resolve().parents[1] / 'benchmarks/preflight_slugify_native_01.py')
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


class SlugifySourceIdentityTests(unittest.TestCase):
    def test_original_accepted_but_content_revision_and_link_drift_rejected(self):
        body = b'original\n'
        blob = hashlib.sha1(b'blob 9\0' + body).hexdigest()
        with tempfile.TemporaryDirectory() as folder, patch.object(preflight, 'BLOBS', {'source.py': blob}), \
                patch.object(preflight.subprocess, 'check_output', return_value=preflight.REVISION + '\n') as git:
            root = Path(folder)
            path = root / 'source.py'
            path.write_bytes(body)
            self.assertEqual(preflight.load_source(root), {'source.py': body})
            path.write_bytes(b'changed\n')
            with self.assertRaisesRegex(ValueError, 'Changed upstream file'):
                preflight.load_source(root)
            path.write_bytes(body)
            git.return_value = 'different-revision\n'
            with self.assertRaisesRegex(ValueError, 'Wrong upstream revision'):
                preflight.load_source(root)
            git.return_value = preflight.REVISION + '\n'
            target = root / 'target.py'
            path.rename(target)
            path.symlink_to(target)
            with self.assertRaisesRegex(ValueError, 'Not a regular upstream file'):
                preflight.load_source(root)
