import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('keyed_fixture', ROOT / 'benchmarks/hostage_keyed_import_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class KeyedImportPreflight(unittest.TestCase):
    def test_native_support_passes_real_result_and_exposes_deliberate_identity_failure(self):
        # No reusable test helper or custom runner method; real application import.
        case = fixture.cases()[0]
        for faulty in (False, True):
            with self.subTest(faulty=faulty), tempfile.TemporaryDirectory(prefix='keyed-preflight-', dir=ROOT) as temporary:
                project = Path(temporary)
                for name, content in case['files'].items():
                    if faulty and name == 'importer.py':
                        content = content.replace('return await persist(key, payload)',
                                                  'await persist(key, payload)\n        return None')
                    (project / name).write_text(content)
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                    cwd=project, capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
                self.assertEqual(result.returncode, int(faulty), output)
                self.assertIn('Ran 2 tests', output)
                self.assertNotIn('RuntimeWarning', output)
                if faulty:
                    self.assertIn('FAILED (failures=1)', output)
                    self.assertIn('AssertionError: None is not <object object at ', output)
                else:
                    self.assertIn('\nOK\n', output)

    def test_frozen_json_matches_authored_case(self):
        import json
        self.assertEqual(json.loads((ROOT / 'benchmarks/hostage-keyed-import-cases.json').read_text()), fixture.cases())
