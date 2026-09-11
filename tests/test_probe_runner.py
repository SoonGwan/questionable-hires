import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/exorcist/scripts/run_probe.py'
spec = importlib.util.spec_from_file_location('probe_runner', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


@unittest.skipUnless(os.name == 'posix', 'POSIX process groups')
class ProbeRunnerTests(unittest.TestCase):
    def run_code(self, code, timeout=2):
        return helper.run([sys.executable, '-B', '-c', code], timeout)

    def test_preserves_success_failure_and_combined_output(self):
        result = self.run_code('import sys; print("output", flush=True); print("error", file=sys.stderr); sys.exit(7)')
        self.assertEqual(result['exit_code'], 7)
        self.assertFalse(result['timed_out'])
        self.assertEqual(result['output'], 'output\nerror\n')
        self.assertEqual(self.run_code('print("ok")')['exit_code'], 0)

    def test_deadline_ignores_cooperative_cancellation(self):
        result = self.run_code('import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); print("ready", flush=True); time.sleep(20)', 0.2)
        self.assertTrue(result['timed_out'])
        self.assertEqual(result['exit_code'], -9)
        self.assertIn('ready', result['output'])
        self.assertLess(result['elapsed_seconds'], 2)

    def test_deadline_after_output_is_closed(self):
        result = self.run_code('import os, time; os.close(1); os.close(2); time.sleep(20)', 0.2)
        self.assertTrue(result['timed_out'])
        self.assertLess(result['elapsed_seconds'], 2)

    def test_inherited_pipe_from_descendant_does_not_hang(self):
        result = self.run_code('import subprocess, sys; subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])', 0.2)
        self.assertTrue(result['timed_out'])
        self.assertLess(result['elapsed_seconds'], 2)

    def test_large_unicode_output_is_bounded(self):
        result = self.run_code('print("안녕" * 100000)')
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(result['output_truncated'])
        self.assertEqual(len(result['output']), 12000)
        self.assertNotIn('\ufffd', result['output'])

    def test_uses_requested_directory_without_shell_interpolation(self):
        with tempfile.TemporaryDirectory() as scratch:
            result = helper.run([sys.executable, '-B', '-c', 'import os, sys; print(os.getcwd()); print(sys.argv[1])', '$(false); literal'], cwd=scratch)
            self.assertEqual(result['output'].splitlines(), [str(Path(scratch).resolve()), '$(false); literal'])
            self.assertEqual(list(Path(scratch).iterdir()), [])

    def test_cli_distinguishes_child_124_from_wrapper_timeout(self):
        for code, expected in [('raise SystemExit(124)', 1), ('import time; time.sleep(20)', 124)]:
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--timeout', '0.2', '--', sys.executable, '-B', '-c', code], capture_output=True, text=True, timeout=3)
            self.assertEqual(result.returncode, expected, result.stderr)
            self.assertEqual(json.loads(result.stdout)['timed_out'], expected == 124)

    def test_rejects_invalid_deadlines_before_start(self):
        for timeout in (0, -1, float('nan'), float('inf'), 301):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                helper.run([sys.executable, '-c', 'raise RuntimeError'], timeout)


if __name__ == '__main__':
    unittest.main()
