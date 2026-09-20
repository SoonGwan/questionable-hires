import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/necromancer/scripts/trace.py'
spec=importlib.util.spec_from_file_location('history_special_files',SCRIPT)
helper=importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class HistorySpecialFileTests(unittest.TestCase):
    @unittest.skipUnless(hasattr(os,'mkfifo'),'Requires POSIX named pipes')
    def test_native_fifo_rejected_without_waiting_for_a_writer(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch:
            fifo=Path(scratch)/'source.py'
            os.mkfifo(fifo)
            before=fifo.stat()
            try:
                result=subprocess.run([sys.executable,'-B',str(SCRIPT),'--repo',scratch,
                    '--path','source.py','--lines','1:1'],capture_output=True,text=True,timeout=2)
            except subprocess.TimeoutExpired:
                self.fail('Collector blocked opening FIFO before Git timeout could apply')
            self.assertEqual(result.returncode,2,result.stderr)
            self.assertEqual(result.stdout,'')
            self.assertIn('regular file',result.stderr)
            self.assertEqual(fifo.stat().st_ino,before.st_ino)
            self.assertEqual(fifo.stat().st_mode,before.st_mode)

    def test_directory_rejected_before_open_or_git(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch:
            (Path(scratch)/'directory').mkdir()
            with patch.object(Path,'open',side_effect=AssertionError('Special file must not be opened')),patch.object(helper,'git') as git:
                with self.assertRaisesRegex(ValueError,'regular file'):
                    helper.trace(scratch,'directory',1,1)
            git.assert_not_called()
