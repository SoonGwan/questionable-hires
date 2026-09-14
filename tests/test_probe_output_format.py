"""Verify serialized evidence, not a model performance estimate."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/exorcist/scripts/run_probe.py'
spec = importlib.util.spec_from_file_location('probe_output', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ProbeOutputFormatTests(unittest.TestCase):
    def render(self, result, encoding='utf-8', pretty=False):
        raw = io.BytesIO()
        stream = io.TextIOWrapper(raw, encoding=encoding)
        args = ['run_probe.py'] + (['--pretty'] if pretty else []) + ['--', 'probe']
        with mock.patch.object(sys, 'argv', args), mock.patch.object(helper, 'run', return_value=result), contextlib.redirect_stdout(stream):
            status = helper.main()
        stream.flush()
        return status, raw.getvalue()

    def test_utf8_compact_and_pretty_keep_all_evidence_and_statuses(self):
        for child, timed_out, clean, status in [(0, False, True, 0), (7, False, True, 1),
                                               (-9, True, True, 124), (None, True, False, 125)]:
            result = dict(exit_code=child, timed_out=timed_out, cleanup_complete=clean,
                          elapsed_seconds=0.123, output='한글 😀\n"actual"\\path\t', output_truncated=True)
            with self.subTest(status=status):
                compact_status, compact = self.render(result)
                pretty_status, pretty = self.render(result, pretty=True)
                self.assertEqual((compact_status, pretty_status), (status, status))
                self.assertEqual(json.loads(compact), result)
                self.assertEqual(json.loads(pretty), result)
                self.assertIn('한글 😀'.encode(), compact)
                self.assertLess(len(compact), len(pretty))
                self.assertEqual(compact.count(b'\n'), 1)

    def test_ascii_stdout_falls_back_without_losing_decoded_content(self):
        result = dict(exit_code=0, timed_out=False, cleanup_complete=True,
                      elapsed_seconds=0.0, output='한글 😀', output_truncated=False)
        for pretty in (False, True):
            status, rendered = self.render(result, encoding='ascii', pretty=pretty)
            self.assertEqual(status, 0)
            self.assertTrue(rendered.isascii())
            self.assertEqual(json.loads(rendered), result)

    @unittest.skipUnless(os.name == 'posix', 'POSIX runner')
    def test_real_unicode_child_and_truncated_tail_in_both_encodings(self):
        text = '진단 😀' * 4000 + '\n'
        # Generate in the child: a byte-literal expansion can exceed Linux's
        # per-argument limit before the wrapper or output path is exercised.
        child = "import os; os.write(1, ('진단 😀' * 4000 + '\\n').encode('utf-8'))"
        for encoding in ('utf-8', 'ascii'):
            completed = subprocess.run([sys.executable, '-B', str(SCRIPT), '--',
                                        sys.executable, '-B', '-c', child],
                                       env=dict(os.environ, PYTHONIOENCODING=encoding),
                                       capture_output=True, timeout=5)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result['output'], text[-12000:])
            self.assertTrue(result['output_truncated'])
            self.assertTrue(result['cleanup_complete'])
            self.assertFalse(result['timed_out'])
            if encoding == 'utf-8':
                self.assertTrue('진단 😀'.encode() in completed.stdout,
                                'UTF-8 result unnecessarily escapes the Unicode log')


if __name__ == '__main__':
    unittest.main()
