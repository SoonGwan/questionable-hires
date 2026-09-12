from pathlib import Path
import subprocess
import tempfile
import unittest


class ReceiptCheckCollectionTests(unittest.TestCase):
    def test_fail_fast_chain_preserves_failure_and_does_not_claim_later_execution(self):
        # Real shell statuses, not a wording test of the skill instruction.
        for failing in (None, 0, 1, 2):
            commands = ["printf 'check-%d\\n'; exit %d" % (i, 7 if i == failing else 0)
                        for i in range(3)]
            with self.subTest(failing=failing):
                chain = ' && '.join("( " + command + " )" for command in commands)
                result = subprocess.run(['sh', '-c', chain], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0 if failing is None else 7)
                count = 3 if failing is None else failing + 1
                self.assertEqual(result.stdout.splitlines(), ['check-' + str(i) for i in range(count)])

    def test_all_check_collection_keeps_early_failure_instead_of_last_success(self):
        hidden = subprocess.run(['sh', '-c', '(exit 7); (exit 0)'], timeout=5)
        self.assertEqual(hidden.returncode, 0)
        collected = subprocess.run(['sh', '-c',
            '(exit 7); receipt_first=$?\n'
            '(exit 0); receipt_second=$?\n'
            'printf "%s %s\\n" "$receipt_first" "$receipt_second"\n'
            'test "$receipt_first" -eq 0 && test "$receipt_second" -eq 0'],
            capture_output=True, text=True, timeout=5)
        self.assertEqual(collected.stdout, '7 0\n')
        self.assertNotEqual(collected.returncode, 0)

    def test_real_diff_failure_stops_following_checks_and_success_runs_them(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            subprocess.run(['git', 'init', '-q', '--template='], cwd=root, check=True, timeout=5)
            target = root / 'source.py'
            target.write_text('VALUE = 1\n')
            subprocess.run(['git', 'add', 'source.py'], cwd=root, check=True, timeout=5)
            command = "git -c core.whitespace=trailing-space diff --check && printf 'next-check-ran\\n'"
            target.write_text('VALUE = 2 \n')
            before = subprocess.run(['sh', '-c', command], cwd=root, capture_output=True, text=True, timeout=5)
            self.assertNotEqual(before.returncode, 0)
            self.assertIn('trailing whitespace', before.stdout)
            self.assertNotIn('next-check-ran', before.stdout)
            target.write_text('VALUE = 2\n')
            after = subprocess.run(['sh', '-c', command], cwd=root, capture_output=True, text=True, timeout=5)
            self.assertEqual(after.returncode, 0)
            self.assertEqual(after.stdout, 'next-check-ran\n')
