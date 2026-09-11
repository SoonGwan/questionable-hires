import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackagingReviewFixtureTests(unittest.TestCase):
    def test_archived_review_matches_pinned_source_when_available(self):
        spec = importlib.util.spec_from_file_location(
            'packaging_review_provenance', ROOT / 'benchmarks/packaging_review_cases.py')
        fixture = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture)
        if subprocess.run(['git', 'cat-file', '-e', fixture.SNAPSHOT + '^{commit}'],
                          cwd=ROOT, capture_output=True).returncode:
            self.skipTest('Pinned packaging review provenance unavailable')
        self.assertEqual(fixture.cases(), fixture.cases(historical=True))

    def test_actual_cleanup_removal_breaks_existing_regression(self):
        spec = importlib.util.spec_from_file_location(
            'packaging_review', ROOT / 'benchmarks/packaging_review_cases.py')
        fixture = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture)
        case = fixture.cases()[0]
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for name, content in case['files'].items():
                target = project / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            baseline = subprocess.run(
                [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
                 '-p', 'test_build.py', '-v'], cwd=project,
                capture_output=True, text=True, timeout=60)
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            self.assertIn('Ran 5 tests', baseline.stderr)
            probe = '''import ast, pathlib, sys, unittest
sys.path.insert(0, 'tests')
import test_build
source = pathlib.Path('scripts/build.py')
tree = ast.parse(source.read_text())
build = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build')
handlers = [n for n in build.body if isinstance(n, ast.Try)]
assert len(handlers) == 1
handler = handlers[0]
assert len(handler.handlers) == 1 and not handler.orelse and not handler.finalbody
build.body = [child for node in build.body for child in (handler.body if node is handler else [node])]
namespace = {'__file__': str(source.resolve()), '__name__': 'cleanup_removal'}
exec(compile(ast.fix_missing_locations(tree), str(source), 'exec'), namespace)
test_build.builder.build = namespace['build']
suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_build.BuildTests)
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
'''
            removed = subprocess.run([sys.executable, '-B', '-c', probe], cwd=project,
                                     capture_output=True, text=True, timeout=60)
            self.assertEqual(removed.returncode, 1, removed.stderr)
            self.assertIn('Ran 5 tests', removed.stderr)
            self.assertIn('FAILED (failures=3)', removed.stderr)
            self.assertIn('self.assertFalse(destination.exists())', removed.stderr)
            for name, content in case['files'].items():
                self.assertEqual((project / name).read_text(), content)
