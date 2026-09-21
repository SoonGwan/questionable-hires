"""Offline source-identity gates; no upstream fetches or model sessions."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('urllib3_preflight', ROOT / 'benchmarks/preflight_urllib3_history_01.py')
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


class Urllib3HistorySourceTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.files = {n: b'original\n' for n in (preflight.TARGET, 'test/test_retry.py', 'LICENSE.txt')}
        for name, body in self.files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            path.chmod(0o644)
        self.revision = preflight.REVISION.encode() + b'\n'
        self.status = b''
        self.shallow = b'false\n'

    def git(self, root, *args):
        self.assertEqual(root, self.root)
        if args == ('rev-parse', 'HEAD'):
            return self.revision
        if args == ('status', '--porcelain=v1'):
            return self.status
        if args == ('rev-parse', '--is-shallow-repository'):
            return self.shallow
        self.assertEqual(args[:3], ('ls-tree', '-r', 'HEAD'))
        return ''.join('100644 blob ' + hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
                       + '\t' + name + '\n' for name, body in self.files.items()).encode()

    def load(self):
        with patch.object(preflight, 'git', side_effect=self.git):
            return preflight.load_source(self.root)

    def test_original_and_content_mode_drift(self):
        self.assertEqual(self.load(), self.files)
        path = self.root / preflight.TARGET
        path.write_bytes(b'changed\n')
        with self.assertRaisesRegex(ValueError, 'Changed upstream file'):
            self.load()
        path.write_bytes(self.files[preflight.TARGET])
        path.chmod(0o755)
        with self.assertRaisesRegex(ValueError, 'Changed upstream file'):
            self.load()

    def test_revision_dirty_and_shallow_rejected(self):
        for attr, bad in [('revision', b'wrong\n'), ('status', b' M changed.py\n'), ('shallow', b'true\n')]:
            good = getattr(self, attr)
            setattr(self, attr, bad)
            with self.subTest(attr=attr), self.assertRaises(ValueError):
                self.load()
            setattr(self, attr, good)

    def test_same_content_symlink_rejected(self):
        path = self.root / preflight.TARGET
        moved = path.with_suffix('.saved')
        path.rename(moved)
        path.symlink_to(moved)
        with self.assertRaisesRegex(ValueError, 'Unexpected upstream entry'):
            self.load()

    def test_required_source_missing_rejected(self):
        del self.files[preflight.TARGET]
        with self.assertRaisesRegex(ValueError, 'Missing required source'):
            self.load()
