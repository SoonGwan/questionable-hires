import importlib.util
from pathlib import Path
import signal
import subprocess
import unittest
from unittest.mock import Mock, patch

SOURCE = Path(__file__).resolve().parents[1] / 'benchmarks/browser/check_search.py'
spec = importlib.util.spec_from_file_location('browser_check', SOURCE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class BrowserRunnerTests(unittest.TestCase):
    def test_timeout_and_cancellation_terminate_owned_group(self):
        for error in (subprocess.TimeoutExpired('chrome', 30), KeyboardInterrupt()):
            with self.subTest(error=type(error)):
                process = Mock(pid=12345)
                process.communicate.side_effect = [error, ('', '')]
                with patch.object(runner.subprocess, 'Popen', return_value=process) as launch, \
                        patch.object(runner.os, 'killpg') as kill:
                    expected = RuntimeError if isinstance(error, subprocess.TimeoutExpired) else KeyboardInterrupt
                    with self.assertRaises(expected):
                        runner.check(Path('/unused-browser'))
                self.assertTrue(launch.call_args.kwargs['start_new_session'])
                kill.assert_called_once_with(12345, signal.SIGKILL)
                self.assertEqual([c.kwargs['timeout'] for c in process.communicate.call_args_list], [30, 5])
                profile = next(a.split('=', 1)[1] for a in launch.call_args.args[0]
                               if a.startswith('--user-data-dir='))
                self.assertFalse(Path(profile).exists())

    def test_cleanup_pipe_timeout_is_bounded_and_closed(self):
        process = Mock(pid=12345)
        process.communicate.side_effect = [subprocess.TimeoutExpired('chrome', 30),
                                          subprocess.TimeoutExpired('chrome', 5)]
        with patch.object(runner.subprocess, 'Popen', return_value=process), \
                patch.object(runner.os, 'killpg', side_effect=ProcessLookupError):
            with self.assertRaisesRegex(RuntimeError, 'incomplete'):
                runner.check(Path('/unused-browser'))
        process.stdout.close.assert_called_once()
        process.stderr.close.assert_called_once()
        process.wait.assert_called_once_with(timeout=5)
