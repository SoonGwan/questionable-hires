"""Execute the shipped module-batch recipe, not an imitation of its schema."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_build import builder


class NativeBatchGuideTests(unittest.TestCase):
    def test_packaged_recipe_preserves_survivors_and_real_detection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bundle = builder.build(root / 'bundle with spaces')
            guide = (bundle / 'skills/con-artist/references/native-unittest-batch.md').read_text()
            recipe = json.loads(guide.split("<<'JSON'\n", 1)[1].split('\nJSON', 1)[0])
            project = root / 'project'
            project.mkdir()
            example = builder.ROOT / 'examples/con-artist-batch'
            for name in ('service.py', 'test_service.py'):
                (project / name).write_bytes((example / name).read_bytes())
                (project / name).chmod(0o600)
            original = (project / 'test_service.py').read_text()
            for sensitive in (False, True):
                with self.subTest(sensitive=sensitive):
                    test_source = original if not sensitive else (
                        'import unittest\nfrom service import save\n'
                        'class SaveTests(unittest.TestCase):\n'
                        '    def test_acknowledges_save(self):\n'
                        '        store = []\n        self.assertTrue(save(store, "new"))\n'
                        '        self.assertEqual(store, ["new"])\n')
                    (project / 'test_service.py').write_text(test_source)
                    before = {p.name: (p.read_bytes(), p.stat().st_mode & 0o777) for p in project.iterdir()}
                    result = subprocess.run([sys.executable, '-I', '-B',
                        str(bundle / 'skills/con-artist/scripts/audit.py'), '--source', str(project), '--spec', '-'],
                        input=json.dumps(recipe), text=True, capture_output=True, timeout=15)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report['status'], 'observed')
                    first, second = report['audits']
                    self.assertEqual(first['checks']['correct_tests']['exit_code'], 0)
                    self.assertEqual(second['checks']['correct_tests']['observation_ref'],
                                     '#/audits/0/checks/correct_tests')
                    for audit in report['audits']:
                        check = audit['checks']['mutant_tests']
                        self.assertEqual(check['exit_code'], int(sensitive))
                        self.assertEqual(check['command'][1:4], ['-B', '-m', 'unittest'])
                        self.assertEqual(check['suite_observation']['tests'], 1)
                        self.assertIn('Verified native test save binding', check['output'])
                        self.assertTrue(audit['integrity']['owned_scratch_removed'])
                        if sensitive:
                            self.assertIn('AssertionError: Lists differ:', check['output'])
                        else:
                            self.assertNotIn('correct_probe', audit['checks'])
                    self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                                              for p in project.iterdir()})
