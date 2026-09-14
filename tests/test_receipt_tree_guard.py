import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_receipt_helper as fixture

helper = fixture.helper


class ReceiptTreeGuardTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def test_native_comparison_preserves_whole_tree_without_listing_hashes(self):
        (self.root / 'unrelated.bin').write_bytes(b'\x00\xfforiginal')
        (self.root / 'empty').mkdir()
        (self.root / 'link').symlink_to('unavailable-target')
        initial, byte_count = helper.tree_inventory(self.root)
        result = helper.compare(self.root, dict(self.recipe, guard_tree=True))
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertIn('Ran 1 test', result['checks']['after']['output'])
        self.assertTrue(result['tree_guard']['unchanged'])
        self.assertEqual(result['tree_guard']['entries'], len(initial))
        self.assertEqual(result['tree_guard']['file_bytes'], byte_count)
        encoded = json.dumps(initial, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(result['tree_guard']['inventory_sha256'], hashlib.sha256(encoded).hexdigest())
        self.assertEqual(helper.tree_inventory(self.root), (initial, byte_count))
        self.assertTrue(result['comparison_copies_removed'])
        self.assertNotIn('unrelated.bin', json.dumps(result))

    def test_actual_native_mutations_are_rejected_without_restoration(self):
        note = self.root / 'unrelated.bin'
        directory = self.root / 'empty'
        directory.mkdir()
        link = self.root / 'link'
        link.symlink_to('old-target')
        mutations = {
            'bytes': "(root/'unrelated.bin').write_bytes(b'changed')",
            'mode': "(root/'unrelated.bin').chmod(0o700)",
            'delete': "(root/'unrelated.bin').unlink(missing_ok=True)",
            'added-file': "(root/'new.bin').write_bytes(b'new')",
            'added-directory': "(root/'new-directory').mkdir(exist_ok=True)",
            'directory-mode': "(root/'empty').chmod(0o750)",
            'root-mode': "root.chmod(0o750)",
            'git-metadata': "(root/'.git/COMMIT_EDITMSG').write_text('changed')",
            'symlink-target': "(root/'link').unlink(); (root/'link').symlink_to('new-target')",
        }
        for label, source in mutations.items():
            with self.subTest(mutation=label):
                note.write_bytes(b'original')
                self.root.chmod(0o700)
                note.chmod(0o600)
                directory.chmod(0o700)
                git_note = self.root / '.git/COMMIT_EDITMSG'
                git_note.write_text('original')
                link.unlink()
                link.symlink_to('old-target')
                (self.root / 'test_rule.py').write_text(self.tests +
                    '\nfrom pathlib import Path\nroot = Path(' + repr(str(self.root)) + ')\n' + source + '\n')
                previous, _ = helper.tree_inventory(self.root)
                observed, native = [], helper.run_check
                def observe_native(*args):
                    result = native(*args)
                    observed.append(result)
                    return result
                with patch.object(helper, 'run_check', side_effect=observe_native):
                    with self.assertRaisesRegex(RuntimeError, 'Project tree changed; not restored'):
                        helper.compare(self.root, dict(self.recipe, guard_tree=True))
                self.assertEqual([check['exit_code'] for check in observed], [1, 0])
                self.assertIn('AssertionError: False is not true', observed[0]['output'])
                self.assertIn('Ran 1 test', observed[1]['output'])
                current, _ = helper.tree_inventory(self.root)
                self.assertNotEqual(previous, current)
                self.assertFalse(list(self.root.glob('.receipt-*')))
                if label == 'added-file':
                    self.assertEqual((self.root / 'new.bin').read_bytes(), b'new')
                    (self.root / 'new.bin').unlink()
                if label == 'added-directory':
                    (self.root / 'new-directory').rmdir()

    def test_disabled_guard_does_not_inventory_unselected_tree(self):
        for option in ({}, {'guard_tree': False}):
            with self.subTest(option=option), patch.object(helper, 'tree_inventory') as inventory:
                result = helper.compare(self.root, dict(self.recipe, **option))
                inventory.assert_not_called()
                self.assertNotIn('tree_guard', result)

    def test_invalid_flags_and_oversized_tree_fail_before_native_execution(self):
        for value in (None, 0, 1, 'true', []):
            with self.subTest(value=value), patch.object(helper, 'run_check') as native:
                with self.assertRaisesRegex(ValueError, 'guard_tree must be a boolean'):
                    helper.compare(self.root, dict(self.recipe, guard_tree=value))
                native.assert_not_called()
        with patch.object(helper, 'MAX_GUARD_BYTES', 1), patch.object(helper, 'run_check') as native:
            with self.assertRaisesRegex(ValueError, 'Tree guard exceeds 20 MB'):
                helper.compare(self.root, dict(self.recipe, guard_tree=True))
            native.assert_not_called()

    def test_inventory_bounds_links_and_special_files(self):
        directory = self.root / 'inventory-test'
        directory.mkdir()
        payload = directory / 'payload'
        payload.write_bytes(b'1234')
        (directory / 'outside-link').symlink_to(self.root / 'rule.py')
        opened, real_open = [], os.open
        def recording_open(path, *args, **kwargs):
            opened.append(Path(path))
            return real_open(path, *args, **kwargs)
        with patch.object(helper.os, 'open', side_effect=recording_open):
            values, size = helper.tree_inventory(directory)
        self.assertEqual(size, 4)
        self.assertEqual(opened, [payload])
        self.assertEqual(values['outside-link'][0], 'symlink')
        with patch.object(helper, 'MAX_FIXED_ENTRIES', 2):
            with self.assertRaisesRegex(ValueError, 'Tree guard exceeds 10000 entries'):
                helper.tree_inventory(directory)
        os.mkfifo(directory / 'fifo')
        with self.assertRaisesRegex(ValueError, 'supports only files, directories and symlinks'):
            helper.tree_inventory(directory)

    def test_file_growth_cannot_exceed_streaming_budget(self):
        directory = self.root / 'growth-test'
        directory.mkdir()
        payload = directory / 'payload'
        payload.write_bytes(b'12')
        real_open = os.open
        def grow_before_open(path, *args, **kwargs):
            payload.write_bytes(b'12345')
            return real_open(path, *args, **kwargs)
        with patch.object(helper, 'MAX_GUARD_BYTES', 4), patch.object(helper.os, 'open', side_effect=grow_before_open):
            with self.assertRaisesRegex(ValueError, 'Tree guard exceeds 20 MB'):
                helper.tree_inventory(directory)

    def test_cli_reports_guard_and_native_results(self):
        installed = self.root / '.agents/skills/receipt/scripts/compare.py'
        installed.parent.mkdir(parents=True)
        shutil.copy2(fixture.SCRIPT, installed)
        result = subprocess.run([sys.executable, '-B', str(installed), '--source',
                                 str(self.root), '--spec', '-'],
                                input=json.dumps(dict(self.recipe, guard_tree=True)),
                                cwd=self.root, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data['tree_guard']['unchanged'])
        self.assertEqual(data['checks']['before']['exit_code'], 1)
        self.assertEqual(data['checks']['after']['exit_code'], 0)

    def test_cli_rejects_native_unrelated_mutation_without_success_json(self):
        (self.root / 'test_rule.py').write_text(self.tests +
            '\nfrom pathlib import Path\nPath(' + repr(str(self.root / 'extra')) + ').write_text("changed")\n')
        result = subprocess.run([sys.executable, '-B', str(fixture.SCRIPT), '--source',
                                 str(self.root), '--spec', '-'],
                                input=json.dumps(dict(self.recipe, guard_tree=True)),
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('Project tree changed; not restored', result.stderr)
        self.assertEqual((self.root / 'extra').read_text(), 'changed')
        self.assertFalse(list(self.root.glob('.receipt-*')))


if __name__ == '__main__':
    unittest.main()
