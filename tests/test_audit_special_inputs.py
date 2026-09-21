"""Selected copy inputs must not silently omit unsupported filesystem objects."""
import importlib.util
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_special_inputs', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


@unittest.skipUnless(os.name == 'posix', 'POSIX filesystem inputs')
class AuditSpecialInputsTests(unittest.TestCase):
    def test_special_inputs_are_rejected_directly_and_inside_selected_directory(self):
        for kind in ('fifo', 'socket'):
            for directory_selection in (False, True):
                with self.subTest(kind=kind, directory=directory_selection), tempfile.TemporaryDirectory() as folder:
                    root = Path(folder)
                    (root / 'pkg').mkdir()
                    (root / 'pkg/service.py').write_text('value = 1\n')
                    special = root / 'pkg/event'
                    endpoint = None
                    try:
                        if kind == 'fifo':
                            os.mkfifo(special)
                        else:
                            endpoint = socket.socket(socket.AF_UNIX)
                            endpoint.bind(str(special))
                        selection = ['pkg'] if directory_selection else ['pkg/service.py', 'pkg/event']
                        with self.assertRaisesRegex(ValueError, 'regular file or directory'):
                            helper.snapshot(root, selection)
                        self.assertTrue(special.exists())
                        self.assertEqual((root / 'pkg/service.py').read_text(), 'value = 1\n')
                    finally:
                        if endpoint is not None:
                            endpoint.close()

    def test_audit_rejects_special_input_before_running_native_checks(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'pkg').mkdir()
            (root / 'pkg/service.py').write_text('value = 1\n')
            os.mkfifo(root / 'pkg/event')
            recipe = dict(files=['pkg'], imports=['pkg.service'], tests=['-v'],
                          target='pkg/service.py', old='value = 1', new='value = 2')
            with patch.object(helper, 'execute') as execute:
                with self.assertRaisesRegex(ValueError, 'regular file or directory'):
                    helper.audit(root, recipe)
                execute.assert_not_called()
            self.assertFalse(list(root.glob('.con-artist-*')))

    def test_regular_directory_selection_preserves_bytes_and_empty_directories(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'pkg/empty').mkdir(parents=True)
            (root / 'pkg/data').write_bytes(b'\x00\xff')
            self.assertEqual(helper.snapshot(root, ['pkg', 'pkg/data']), {'pkg/data': b'\x00\xff'})
            self.assertTrue((root / 'pkg/empty').is_dir())
