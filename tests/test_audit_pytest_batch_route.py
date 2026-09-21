"""Execute the supported pytest batch composition through a built skill."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_build import builder


@unittest.skipUnless(importlib.util.find_spec('pytest'), 'Native pytest dependency is required')
class PytestBatchRouteTests(unittest.TestCase):
    def test_common_contract_composes_with_batch_without_module_startup(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bundle = builder.build(root / 'bundle with spaces')
            guide = (bundle / 'skills/con-artist/references/python-audit.md').read_text()
            recipe = json.loads(guide.split("<<'JSON'\n",1)[1].split('\nJSON',1)[0])
            first = {k:recipe.pop(k) for k in ('target','old','new')}
            recipe.pop('probe')
            recipe.pop('probe_when')
            recipe.update(runner='pytest', tests=['test_service.py','-q','-p','no:cacheprovider'],
                          mutations=[first, dict(first, new='    store.extend([record, record])\n')])
            project = root / 'project'
            project.mkdir()
            example = builder.ROOT / 'examples/con-artist-batch'
            for name in ('service.py','test_service.py'):
                (project / name).write_bytes((example / name).read_bytes())
                (project / name).chmod(0o600)
            weak = (project / 'test_service.py').read_text()
            for strong in (False, True):
                with self.subTest(strong=strong):
                    text = weak if not strong else (
                        'import unittest\nfrom service import save\n'
                        'class SaveTests(unittest.TestCase):\n'
                        '    def test_acknowledges_save(self):\n'
                        '        records = []\n        self.assertTrue(save(records, "new"))\n'
                        '        self.assertEqual(records, ["new"])\n')
                    (project / 'test_service.py').write_text(text)
                    before = {p.name:(p.read_bytes(),p.stat().st_mode & 0o777) for p in project.iterdir()}
                    result = subprocess.run([sys.executable,'-I','-B',
                        str(bundle / 'skills/con-artist/scripts/audit.py'),'--source',str(project),'--spec','-'],
                        input=json.dumps(recipe),text=True,capture_output=True,timeout=20)
                    self.assertEqual(result.returncode,0,result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report['status'],'observed')
                    first_result, second = report['audits']
                    self.assertEqual(first_result['checks']['correct_tests']['exit_code'],0)
                    self.assertIn('1 passed',first_result['checks']['correct_tests']['output'])
                    self.assertEqual(second['checks']['correct_tests']['observation_ref'],
                                     '#/audits/0/checks/correct_tests')
                    for audit in report['audits']:
                        mutant = audit['checks']['mutant_tests']
                        self.assertEqual(mutant['exit_code'],int(strong))
                        self.assertIn('Verified actual test global save is service.save',mutant['output'])
                        self.assertIn('1 failed' if strong else '1 passed',mutant['output'])
                        if strong: self.assertIn('AssertionError',mutant['output'])
                        self.assertFalse(mutant['timed_out'])
                        self.assertFalse(mutant['output_truncated'])
                        self.assertTrue(audit['integrity']['owned_scratch_removed'])
                    self.assertEqual(before,{p.name:(p.read_bytes(),p.stat().st_mode & 0o777) for p in project.iterdir()})
