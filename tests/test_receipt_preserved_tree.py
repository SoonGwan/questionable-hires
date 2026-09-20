import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/receipt/scripts/preserve.py'
spec = importlib.util.spec_from_file_location('receipt_preserve', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ReceiptPreservedTreeTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / 'notes').write_text('owner draft')

    def test_exactly_two_inventories_and_owned_cleanup_before_exit(self):
        with patch.object(helper, 'tree_inventory', wraps=helper.tree_inventory) as inventory:
            with helper.preserved_tree(self.root) as report:
                self.assertIsNone(report['unchanged'])
                with tempfile.TemporaryDirectory(dir=self.root) as copy:
                    (Path(copy) / 'generated').write_text('temporary')
            self.assertEqual(inventory.call_count, 2)
        self.assertTrue(report['unchanged'])
        self.assertEqual(report['entries'], 2)
        self.assertEqual((self.root / 'notes').read_text(), 'owner draft')

    def test_exception_propagates_even_when_originals_are_unchanged(self):
        with self.assertRaisesRegex(ValueError, 'native setup failed'):
            with helper.preserved_tree(self.root) as report:
                raise ValueError('native setup failed')
        self.assertTrue(report['unchanged'])  # Preservation, not workflow success.

    def test_change_rejected_without_restoration_and_original_error_retained(self):
        with self.assertRaisesRegex(RuntimeError, 'Project tree changed; not restored') as caught:
            with helper.preserved_tree(self.root) as report:
                (self.root / 'notes').write_text('changed')
                raise ValueError('native failure')
        self.assertIsInstance(caught.exception.__context__, ValueError)
        self.assertIsNone(report['unchanged'])
        self.assertEqual((self.root / 'notes').read_text(), 'changed')

    def test_modes_links_git_and_retained_scratch_are_not_ignored(self):
        for mutation in ('mode', 'link', 'git', 'scratch'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(dir=self.root) as sample:
                root = Path(sample)
                (root / 'note').write_text('same')
                (root / 'note').chmod(0o600)
                (root / 'link').symlink_to('old-target')
                (root / '.git').mkdir()
                (root / '.git/index').write_bytes(b'original')
                with self.assertRaisesRegex(RuntimeError, 'Project tree changed'):
                    with helper.preserved_tree(root):
                        if mutation == 'mode':
                            (root / 'note').chmod(0o700)
                        elif mutation == 'link':
                            (root / 'link').unlink()
                            (root / 'link').symlink_to('new-target')
                        elif mutation == 'git':
                            (root / '.git/index').write_bytes(b'changed')
                        else:
                            (root / 'owned-but-not-cleaned').mkdir()

    def test_bounds_fail_before_work_and_after_without_success_report(self):
        with self.assertRaisesRegex(ValueError, 'directory root'):
            with helper.preserved_tree(self.root / 'notes'):
                self.fail('Must not treat a file as a project root')
        with patch.object(helper._comparison, 'MAX_GUARD_BYTES', 1):
            with self.assertRaisesRegex(ValueError, 'Tree guard exceeds'):
                with helper.preserved_tree(self.root):
                    self.fail('Must not enter oversized tree')
        with self.assertRaisesRegex(ValueError, 'supports only files'):
            with helper.preserved_tree(self.root) as report:
                os.mkfifo(self.root / 'fifo')
        self.assertIsNone(report['unchanged'])

    def test_native_startup_positive_negative_controls_keep_originals(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'benchmarks'))
        from receipt_startup_case import BEFORE, AFTER, HOOK, TESTS
        originals = {'manifest.py': BEFORE, 'sitecustomize.py': HOOK,
                     'test_manifest.py': TESTS, 'format.json': '{"delimiter":";"}\n'}
        for name, contents in originals.items():
            (self.root / name).write_text(contents)
        with helper.preserved_tree(self.root) as report:
            for source, expected in ((BEFORE, 1), (AFTER, 0)):
                with tempfile.TemporaryDirectory(dir=self.root) as isolated:
                    copy = Path(isolated)
                    for name, contents in originals.items():
                        (copy / name).write_text(source if name == 'manifest.py' else contents)
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_manifest'],
                        cwd=copy, env=dict(os.environ, PYTHONPATH='.'), text=True,
                        capture_output=True, timeout=10)
                    output = result.stdout + result.stderr
                    self.assertEqual(result.returncode, expected, output)
                    self.assertIn('Ran 5 tests', output)
                    self.assertIn('NATIVE_IMPORTS ', output)
                    self.assertNotIn('ERROR:', output)
                    if expected:
                        self.assertIn('FAILED (failures=2)', output)
                        self.assertIn('Lists differ:', output)
        self.assertTrue(report['unchanged'])
