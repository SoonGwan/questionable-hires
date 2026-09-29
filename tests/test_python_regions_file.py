"""Real CLI file-input parity, error outcomes and source preservation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
SCRIPT=Path(__file__).resolve().parents[1]/'skills/necromancer/scripts/python_regions.py'
class FileInput(unittest.TestCase):
    def invoke(self,*args,stdin=b''):
        return subprocess.run([sys.executable,'-B',str(SCRIPT),*args],input=stdin,capture_output=True,timeout=10)
    def test_same_regions_hash_and_compiler_context_without_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'source.py';marker=Path(folder)/'executed'
            raw=('from __future__ import annotations\nfrom pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\nclass C:\n    @property\n    def selected(self):\n        return "한글"\n').encode();source.write_bytes(raw);mode=source.stat().st_mode
            direct=self.invoke('--path',str(source),'--name','C.selected',stdin=b'invalid stdin must be ignored')
            piped=self.invoke('--name','C.selected',stdin=raw)
            self.assertEqual((direct.returncode,piped.returncode),(0,0))
            a,b=json.loads(direct.stdout),json.loads(piped.stdout)
            self.assertEqual(a['input_path'],str(source))
            self.assertEqual(a['source_sha256'],hashlib.sha256(raw).hexdigest())
            for k in b:
                if k!='limitation':self.assertEqual(a[k],b[k])
            self.assertIn('not a Git revision or atomic snapshot',a['limitation'])
            self.assertEqual(source.read_bytes(),raw);self.assertEqual(source.stat().st_mode,mode);self.assertFalse(marker.exists())
    def test_missing_directory_invalid_encoding_and_oversized_sources_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for name,body in [('encoding.py',b'\xff'),('large.py',b' '*2_000_001)]: (root/name).write_bytes(body)
            for source in [root/'absent.py',root,root/'encoding.py',root/'large.py']:
                with self.subTest(source=source):
                    r=self.invoke('--path',str(source),'--name','f');self.assertEqual(r.returncode,2);self.assertEqual(r.stdout,b'');self.assertIn(b'Source regions unavailable',r.stderr)
    def test_missing_name_remains_incomplete_exit_one(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'source.py';source.write_text('def found():\n    return 1\n')
            r=self.invoke('--path',str(source),'--name','absent');self.assertEqual(r.returncode,1);self.assertFalse(json.loads(r.stdout)['complete']);self.assertEqual(json.loads(r.stdout)['missing_names'],['absent'])
