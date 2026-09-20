import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
from hostage_stale_patch_case import preflight, cases, BROKEN, CORRECT


class StalePatchTests(unittest.TestCase):
    def test_actual_rejection_and_native_assertion_controls(self):
        rows=preflight()
        self.assertEqual([r['exit_code'] for r in rows],[1,1,0,0])
        self.assertIn('patch does not apply',rows[0]['output'])
        self.assertIn('AssertionError: 100 != 0',rows[1]['output'])

    def test_audit_preserves_failed_and_correct_invocations(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch:
            project=Path(scratch)
            for name,content in cases()[0]['files'].items():
                (project/name).write_text(content)
            for code,expected in ((BROKEN,1),(CORRECT,0)):
                (project/'options.py').write_text(code)
                result=subprocess.run([sys.executable,'-B','-m','unittest','discover','-v'],
                    cwd=project,capture_output=True,text=True,timeout=10)
                self.assertEqual(result.returncode,expected,result.stdout+result.stderr)
            audit=[json.loads(line) for line in (project/'test-invocations.jsonl').read_text().splitlines()]
            self.assertEqual([r['zero_result'] for r in audit],[100,0])
            self.assertNotEqual(audit[0]['source_sha256'],audit[1]['source_sha256'])
