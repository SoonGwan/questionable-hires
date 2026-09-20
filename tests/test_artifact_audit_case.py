import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from artifact_audit_case import APP, OLD, NEW, STRONG, case
import run


@unittest.skipUnless(importlib.util.find_spec('pytest'), 'requires installed pytest')
class ArtifactAuditCaseTests(unittest.TestCase):
    def test_native_four_way_controls_and_helper_preservation(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            project = Path(scratch) / 'project'
            task = case(sys.executable)
            run.prepare(task, project)
            original = run.resource_manifest(project)
            for strong in (False, True):
                for faulty in (False, True):
                    copy = project / ('audit-' + str(strong) + '-' + str(faulty))
                    copy.mkdir()
                    for name, value in task['files'].items():
                        (copy / name).write_text(value)
                    (copy / 'manifest.py').write_text(APP.replace(OLD, NEW) if faulty else APP)
                    if strong:
                        (copy / 'checks_manifest.py').write_text(STRONG)
                    result = subprocess.run([sys.executable, '-B', '-m', 'pytest', '-vv', '-s',
                        '-p', 'no:cacheprovider', 'checks_manifest.py'], cwd=copy,
                        capture_output=True, text=True, timeout=20)
                    output = result.stdout + result.stderr
                    self.assertEqual(result.returncode, int(strong and faulty), output)
                    self.assertIn('2 failed, 1 passed' if strong and faulty else '3 passed', output)
                    if strong and faulty:
                        self.assertIn("'sha256': ''", output)
                        self.assertIn('a' * 64, output)
                        self.assertIn('c' * 64, output)
                    self.assertFalse(list(copy.glob('.manifest-test-*')))
                    # Owned disposable files only; not the original project.
                    import shutil
                    shutil.rmtree(copy)
            spec = importlib.util.spec_from_file_location('artifact_audit', ROOT / 'skills/con-artist/scripts/audit.py')
            helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(helper)
            report = helper.audit(project, dict(files=['manifest.py', 'conftest.py', 'pytest.ini', 'checks_manifest.py'],
                imports=['manifest', 'checks_manifest'], runner='pytest',
                tests=['-vv', '-s', '-p', 'no:cacheprovider', 'checks_manifest.py'],
                target='manifest.py', old=OLD, new=NEW,
                probe_replacements={'checks_manifest.py': STRONG},
                probe_tests=['-vv', '-s', '-p', 'no:cacheprovider', 'checks_manifest.py']), python=sys.executable)
            self.assertEqual(report['status'], 'observed')
            for name, check in report['checks'].items():
                self.assertEqual(check['exit_code'], int(name == 'mutant_probe'), check['output'])
                self.assertIn('2 failed, 1 passed' if name == 'mutant_probe' else '3 passed', check['output'])
                self.assertIn('Verified copied import: manifest', check['output'])
                self.assertFalse(check['output_truncated'])
            self.assertTrue(report['integrity']['owned_scratch_removed'])
            self.assertEqual(original, run.resource_manifest(project))
