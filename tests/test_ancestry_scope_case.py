import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import ancestry_scope_case as fixture
import run as benchmark_run


class AncestryScopeCaseTests(unittest.TestCase):
    def test_native_bootstrap_assertions_and_merge_scope(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as directory:
            root = Path(directory) / 'project'
            ids = fixture.build(root)
            before = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
            env = dict(os.environ, PYTHONPATH=str(root))

            def run(*args):
                return subprocess.run([sys.executable, '-B', *args], cwd=root, env=env,
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)

            cold = run('-c', 'import catalog; from pathlib import Path; '
                       'assert Path(catalog.__file__).resolve() == Path("catalog.py").resolve()')
            self.assertEqual(cold.returncode, 0, cold.stdout)
            normal = run('-m', 'unittest', '-v', 'test_catalog')
            self.assertEqual(normal.returncode, 0, normal.stdout)
            self.assertIn('Ran 2 tests', normal.stdout)
            (root / 'catalog.py').write_text(fixture.SOURCE.replace('return (tenant, item)', 'return item'))
            mutant = run('-m', 'unittest', '-v', 'test_catalog')
            self.assertEqual(mutant.returncode, 1, mutant.stdout)
            self.assertIn("AssertionError: 'east:17' != 'west:17'", mutant.stdout)
            self.assertRegex(mutant.stdout, r'test_single_tenant \(test_catalog\.CatalogTests(?:\.test_single_tenant)?\) \.\.\. ok')
            (root / 'catalog.py').write_bytes(before['catalog.py'])
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}, before)
            self.assertEqual(fixture.git(root, 'status', '--porcelain'), '')
            ancestors = fixture.git(root, 'rev-list', 'HEAD').splitlines()
            self.assertIn(ids['introduction'], ancestors)
            self.assertNotIn(ids['future'], ancestors)
            first = fixture.git(root, 'rev-list', '--first-parent', 'HEAD').splitlines()
            self.assertNotIn(ids['introduction'], first)
            selected = fixture.git(root, 'log', '--format=%H', '-S', 'return (tenant, item)', 'HEAD', '--', 'catalog.py').splitlines()
            self.assertEqual(selected, [ids['introduction']])

    def test_reproducible_commits_and_task_boundaries(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as directory:
            root = Path(directory)
            self.assertEqual(fixture.build(root / 'one'), fixture.build(root / 'two'))
            with self.assertRaises(FileExistsError):
                fixture.build(root / 'one')
        cases = fixture.cases()
        self.assertEqual(len(cases), 2)
        self.assertIn('Do not inspect Git history', cases[1]['task'])
        self.assertIn('Use only pinned HEAD', cases[0]['task'])

    def test_existing_runner_copy_preserves_scope_control_refs(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as directory:
            root = Path(directory)
            source, copied = root / 'source', root / 'copy'
            ids = fixture.build(source)
            self.assertEqual(benchmark_run.prepare_repository(source, copied), ids['base'])
            self.assertEqual(fixture.git(copied, 'show-ref'), fixture.git(source, 'show-ref'))
            self.assertEqual(fixture.git(copied, 'rev-list', 'HEAD'), fixture.git(source, 'rev-list', 'HEAD'))
            self.assertIn(ids['future'], fixture.git(copied, 'rev-list', '--all').splitlines())
            self.assertNotIn(ids['future'], fixture.git(copied, 'rev-list', 'HEAD').splitlines())
            self.assertEqual(fixture.git(copied, 'status', '--porcelain'), '')


if __name__ == '__main__':
    unittest.main()
