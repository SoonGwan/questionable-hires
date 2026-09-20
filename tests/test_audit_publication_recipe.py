"""Author-side support validation; not a replay/replacement of model evidence."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'benchmarks/results/con-artist-discovery-01/baseline/manifest-discovery-known--baseline--1/project'
spec = importlib.util.spec_from_file_location('publication_audit', ROOT/'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

STRONG = r'''
    def test_published_bytes(self):
        payload = {'version': 3, 'routes': ['/서울', '/café']}
        expected = '{"routes": ["/서울", "/café"], "version": 3}\n'.encode('utf-8')
        self.assertNotEqual(self.target.read_bytes(), expected)
        self.assertEqual(publish(self.target, payload), {'published': 3})
        self.assertFalse(self.target.with_name('active.json.pending').exists())
        self.assertEqual(self.target.read_bytes(), expected)
'''


class PublicationRecipeTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(dir=ROOT/'benchmarks')
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.files = ['engine.py','bridge.py','checks/test_engine.py','requirements.md','notes.txt','AGENTS.md']
        for name in self.files:
            path = self.root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((SOURCE/name).read_bytes())
        self.recipe = dict(files=self.files, imports=['engine','bridge','test_engine'],
            import_roots=['checks'], target='engine.py', old='        staged.replace(destination)\n',
            new='        pass  # omit publication\n', runner='unittest',
            tests=['discover','-s','checks','-v'], probe_tests=['discover','-s','checks','-v'],
            probe_replacements={'checks/test_engine.py':(self.root/'checks/test_engine.py').read_text()+STRONG},
            precheck="import engine, bridge, test_engine\nassert test_engine.publish is bridge.refresh\nassert bridge.refresh.__globals__['_install'] is engine.install\nprint('ACTUAL_IMPORTED_BINDINGS_VERIFIED', flush=True)\n")

    def run_recipe(self):
        before = {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mode & 0o777)
                  for p in self.root.rglob('*') if p.is_file()}
        with patch.object(helper, 'execute', wraps=helper.execute) as calls:
            result = helper.audit(self.root, self.recipe)
        self.assertEqual(before, {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mode & 0o777)
                                 for p in self.root.rglob('*') if p.is_file()})
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        self.assertEqual(sorted(p.name for p in self.root.iterdir()),
                         ['AGENTS.md','bridge.py','checks','engine.py','notes.txt','requirements.md'])
        return result, calls.call_count

    def test_native_four_checks_with_real_imports_without_startup_hook(self):
        result, count = self.run_recipe()
        self.assertEqual(count, 4)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual({k:v['exit_code'] for k,v in result['checks'].items()},
                         dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        for key, check in result['checks'].items():
            self.assertIn('ACTUAL_IMPORTED_BINDINGS_VERIFIED', check['output'])
            self.assertIn('Verified copied import: test_engine', check['output'])
            self.assertIn(f'Ran {3 if key.endswith("probe") else 2} tests', check['output'])
            self.assertNotIn('ERROR:', check['output'])
        faulty = result['checks']['mutant_probe']['output']
        self.assertIn('FAIL: test_published_bytes', faulty)
        self.assertIn('previous manifest', faulty)
        self.assertIn('version', faulty)

    def test_wrong_writer_binding_is_incomplete_before_tests(self):
        bridge = self.root/'bridge.py'
        bridge.write_text(bridge.read_text().replace('from engine import install as _install',
            "def _install(destination, payload):\n    return {'published': payload['version']}"))
        result, count = self.run_recipe()
        self.assertEqual(count, 1)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests'])
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 6)
        self.assertIn('Precheck failed; not mutation evidence', result['checks']['correct_tests']['output'])
        self.assertNotIn('Ran 2 tests', result['checks']['correct_tests']['output'])

    def test_invalid_stronger_source_stops_before_mutant_checks(self):
        self.recipe['probe_replacements']['checks/test_engine.py'] += "\ninvalid = 'unterminated\n"
        result, count = self.run_recipe()
        self.assertEqual(count, 2)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests','correct_probe'])
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 7)
        self.assertIn('SyntaxError', result['checks']['correct_probe']['output'])
        self.assertIn('Import setup failed; not mutation evidence', result['checks']['correct_probe']['output'])
