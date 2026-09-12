import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/exorcist/scripts/run_probe.py'
spec = importlib.util.spec_from_file_location('probe_runner', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


@unittest.skipUnless(os.name == 'posix', 'POSIX process groups')
class ProbeRunnerTests(unittest.TestCase):
    def test_cleanup_wait_is_bounded_and_incomplete_is_explicit(self):
        process = mock.Mock(returncode=None)
        process.wait.side_effect = subprocess.TimeoutExpired(['probe'], 5)
        with mock.patch.object(helper.subprocess, 'Popen', return_value=process), \
                mock.patch.object(helper.selectors, 'DefaultSelector', side_effect=subprocess.TimeoutExpired(['probe'], 1)), \
                mock.patch.object(helper.os, 'killpg'):
            result = helper.run(['probe'], 1)
        process.wait.assert_called_once_with(timeout=5)
        process.stdout.close.assert_called_once()
        self.assertTrue(result['timed_out'])
        self.assertFalse(result['cleanup_complete'])
        self.assertIsNone(result['exit_code'])

    def test_cleanup_timeout_preserves_interruption(self):
        process = mock.Mock(returncode=None)
        process.wait.side_effect = subprocess.TimeoutExpired(['probe'], 5)
        with mock.patch.object(helper.subprocess, 'Popen', return_value=process), \
                mock.patch.object(helper.selectors, 'DefaultSelector', side_effect=KeyboardInterrupt), \
                mock.patch.object(helper.os, 'killpg'), self.assertRaises(KeyboardInterrupt):
            helper.run(['probe'], 1)
        process.wait.assert_called_once_with(timeout=5)

    def test_cli_reports_incomplete_cleanup_as_distinct_failure(self):
        result = dict(exit_code=None, timed_out=True, cleanup_complete=False)
        with mock.patch.object(sys, 'argv', ['run_probe.py', '--', 'probe']), \
                mock.patch.object(helper, 'run', return_value=result), \
                mock.patch('builtins.print'):
            self.assertEqual(helper.main(), 125)

    def run_code(self, code, timeout=2):
        return helper.run([sys.executable, '-B', '-c', code], timeout)

    def test_preserves_success_failure_and_combined_output(self):
        result = self.run_code('import sys; print("output", flush=True); print("error", file=sys.stderr); sys.exit(7)')
        self.assertEqual(result['exit_code'], 7)
        self.assertFalse(result['timed_out'])
        self.assertEqual(result['output'], 'output\nerror\n')
        self.assertEqual(self.run_code('print("ok")')['exit_code'], 0)

    def test_nested_worker_output_and_forwarded_status_are_captured(self):
        for status in (0, 1):
            with self.subTest(status=status):
                worker = ('import sys\nprint("normal sequence passed", flush=True)\n'
                          'print("worker diagnostic", file=sys.stderr, flush=True)\n'
                          f'raise SystemExit({status})\n')
                parent = ('import subprocess,sys\n'
                          f'p = subprocess.run([sys.executable, "-B", "-c", {worker!r}], timeout=2)\n'
                          'raise SystemExit(p.returncode)\n')
                result = self.run_code(parent, timeout=4)
                self.assertEqual(result['exit_code'], status)
                self.assertFalse(result['timed_out'])
                self.assertTrue(result['cleanup_complete'])
                self.assertFalse(result['output_truncated'])
                self.assertEqual(result['output'], 'normal sequence passed\nworker diagnostic\n')

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

    def test_async_wait_for_is_not_a_process_deadline(self):
        code = '''import asyncio
async def stubborn():
    print("task started", flush=True)
    while True:
        try:
            await asyncio.sleep(20)
        except asyncio.CancelledError:
            print("cancellation suppressed", flush=True)
async def main():
    await asyncio.wait_for(stubborn(), timeout=0.02)
asyncio.run(main())
'''
        result = self.run_code(code, timeout=0.3)
        self.assertIn('cancellation suppressed', result['output'])
        self.assertTrue(result['timed_out'])
        self.assertEqual(result['exit_code'], -9)
        self.assertLess(result['elapsed_seconds'], 2)

    def test_inherited_pipe_from_descendant_does_not_hang(self):
        result = self.run_code('import subprocess, sys; subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])', 0.2)
        self.assertTrue(result['timed_out'])
        self.assertLess(result['elapsed_seconds'], 2)

    def test_existing_deadline_covers_async_cleanup_without_self_spawn(self):
        code = '''import asyncio
async def operation():
    try:
        await asyncio.Event().wait()
    finally:
        print("cleanup entered", flush=True)
        while STUBBORN:
            try:
                await asyncio.sleep(20)
            except asyncio.CancelledError:
                pass
        print("cleanup finished", flush=True)
async def main():
    task = asyncio.create_task(operation())
    await asyncio.sleep(0)
    print("sequence checked", flush=True)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)
asyncio.run(main())
'''
        for stubborn in (False, True):
            with self.subTest(stubborn=stubborn):
                result = self.run_code('STUBBORN = ' + repr(stubborn) + '\n' + code,
                                       timeout=0.5)
                self.assertIn('sequence checked\ncleanup entered\n', result['output'])
                self.assertEqual(result['timed_out'], stubborn)
                self.assertEqual(result['exit_code'], -9 if stubborn else 0)
                self.assertEqual('cleanup finished' in result['output'], not stubborn)
                self.assertTrue(result['cleanup_complete'])
                self.assertFalse(result['output_truncated'])
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
