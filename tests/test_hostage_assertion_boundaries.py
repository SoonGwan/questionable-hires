"""Native controls for observed test-authoring failures, not model compliance."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
from hostage_refresh_cases import SOURCE,BROKEN


class HostageAssertionBoundaryTests(unittest.TestCase):
    def execute(self,root):
        return subprocess.run([sys.executable,'-B','-m','unittest','discover','-v'],
            cwd=root,capture_output=True,text=True,timeout=10)

    def test_observable_assertion_accepts_valid_counter_and_rejects_broken_owner(self):
        evidence=ROOT/'benchmarks/results/hostage-modes-01/original/refresh-owner-a--skill--1/project'
        original=(evidence/'test_preview.py').read_text()
        old='        self.assert_state((False, before[1], before[2] + 1))'
        self.assertEqual(original.count(old),1)
        repaired=original.replace(old,'        self.assertFalse(self.preview.pending)\n        self.assertIs(self.preview.value, before[1])')
        alternative=SOURCE.replace('self.generation += 1','self.generation += 2')
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch:
            root=Path(scratch)
            (root/'controlled_call.py').write_bytes((evidence/'controlled_call.py').read_bytes())
            for label,tests,implementation,code in (
                ('original-correct',original,SOURCE,0),
                ('original-valid-alternative',original,alternative,1),
                ('repaired-correct',repaired,SOURCE,0),
                ('repaired-valid-alternative',repaired,alternative,0),
                ('repaired-defect',repaired,BROKEN,1)):
                with self.subTest(label=label):
                    (root/'test_preview.py').write_text(tests)
                    (root/'preview.py').write_text(implementation)
                    result=self.execute(root)
                    self.assertEqual(result.returncode,code,result.stderr)
                    self.assertIn('Ran 8 tests',result.stderr)
                    self.assertNotIn('ERROR:',result.stderr)
                    if label=='original-valid-alternative':
                        self.assertIn('6 != 5',result.stderr)
                    if label=='repaired-defect':
                        self.assertIn('False != True',result.stderr)
                    self.assertEqual((root/'test_preview.py').read_text(),tests)
                    self.assertEqual((root/'preview.py').read_text(),implementation)

    def test_distinct_helper_name_restores_native_assertion_evidence(self):
        source='''import unittest
class Checks(unittest.IsolatedAsyncioTestCase):
    async def fail(self, task, fetch, cancel):
        pass
    def test_contract(self):
        self.assertEqual("observed", "expected")
'''
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch:
            root=Path(scratch)
            for repaired in (False,True):
                with self.subTest(repaired=repaired):
                    (root/'test_contract.py').write_text(source.replace('async def fail(', 'async def fail_call(') if repaired else source)
                    result=self.execute(root)
                    self.assertEqual(result.returncode,1,result.stderr)
                    self.assertIn('Ran 1 test',result.stderr)
                    if repaired:
                        self.assertIn("'observed' != 'expected'",result.stderr)
                        self.assertIn('FAILED (failures=1)',result.stderr)
                        self.assertNotIn('TypeError',result.stderr)
                    else:
                        self.assertIn('TypeError',result.stderr)
                        self.assertIn('FAILED (errors=1)',result.stderr)
