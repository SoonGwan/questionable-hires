import importlib.util
from pathlib import Path
import tempfile
import unittest
import hashlib

spec = importlib.util.spec_from_file_location('audit_httpx', Path(__file__).resolve().parents[1] / 'benchmarks/audit_httpx.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class HTTPXAuditTests(unittest.TestCase):
    def test_resource_hashes_detect_helper_changes_and_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'scripts').mkdir()
            (root / 'scripts/audit.py').write_text('original')
            expected = {'scripts/audit.py': hashlib.sha256(b'original').hexdigest()}
            self.assertTrue(audit.check_resources(root, expected)['matches'])
            (root / 'scripts/audit.py').write_text('changed')
            self.assertFalse(audit.check_resources(root, expected)['matches'])
            self.assertFalse(audit.check_resources(root / 'missing', expected)['matches'])
            self.assertIsNone(audit.check_resources(root, None)['matches'])

    def test_resource_checks_reject_escape_and_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'real').mkdir()
            (root / 'real/code.py').write_text('original')
            (root / 'linked').symlink_to(root / 'real', target_is_directory=True)
            digest = hashlib.sha256(b'original').hexdigest()
            self.assertFalse(audit.check_resources(root, {'linked/code.py': digest})['matches'])
            with self.assertRaises(ValueError):
                audit.check_resources(root, {'../escape': digest})

    def test_detects_deleted_and_changed_originals_but_allows_new_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'source', Path(directory) / 'target'
            source.mkdir()
            target.mkdir()
            for name in ('same.py', 'changed.py', 'missing.py'):
                (source / name).write_text('original')
            (target / 'same.py').write_text('original')
            (target / 'changed.py').write_text('edited')
            (target / 'diagnostic.py').write_text('new')
            result = audit.compare_files(source, target, ['same.py', 'changed.py', 'missing.py'])
            self.assertFalse(result['originals_preserved'])
            self.assertEqual(result['changed_original_files'], ['changed.py'])
            self.assertEqual(result['missing_original_files'], ['missing.py'])
            self.assertTrue(audit.compare_files(source, target, ['same.py'])['originals_preserved'])

    def test_symlink_to_original_is_not_independent_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'source', Path(directory) / 'target'
            source.mkdir()
            target.mkdir()
            (source / 'code.py').write_text('original')
            (target / 'code.py').symlink_to(source / 'code.py')
            self.assertFalse(audit.compare_files(source, target, ['code.py'])['originals_preserved'])
