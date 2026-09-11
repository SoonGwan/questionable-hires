import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

spec = importlib.util.spec_from_file_location("builder", Path(__file__).resolve().parents[1] / "scripts/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
    def test_bundled_receipt_executes_real_before_after_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            plugin = builder.build(scratch / 'bundle')
            project = scratch / 'project'
            project.mkdir()
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=project, text=True).strip()
            git('init', '-q', '--template=')
            git('config', 'user.name', 'Package Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            git('config', 'core.hooksPath', str(scratch / 'no-hooks'))
            revisions = []
            for expression in ('n > 18', 'n >= 18'):
                (project / 'rule.py').write_text('def eligible(n): return ' + expression + '\n')
                git('add', '.')
                git('commit', '-qm', 'boundary version')
                revisions.append(git('rev-parse', 'HEAD'))
            test = ('import unittest\nfrom rule import eligible\n'
                    'class Boundary(unittest.TestCase):\n'
                    '    def test_boundary(self): self.assertTrue(eligible(18))\n')
            (project / 'test_rule.py').write_text(test)
            status = git('status', '--porcelain')
            recipe = dict(fixed=['test_rule.py'], vary=['rule.py'],
                          imports=['rule'], runner='unittest', tests=['-v', 'test_rule'],
                          before=revisions[0], after=revisions[1])
            process = subprocess.run(
                [sys.executable, '-B', str(plugin / 'skills/receipt/scripts/compare.py'),
                 '--source', str(project), '--spec', '-'], input=json.dumps(recipe),
                text=True, capture_output=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['checks']['before']['exit_code'], 1)
            self.assertIn('AssertionError', result['checks']['before']['output'])
            self.assertEqual(result['checks']['after']['exit_code'], 0)
            self.assertIn('Verified copied import: rule', result['checks']['after']['output'])
            self.assertIn('Ran 1 test', result['checks']['after']['output'])
            self.assertEqual((project/'test_rule.py').read_text(), test)
            self.assertEqual((project/'rule.py').read_text(), 'def eligible(n): return n >= 18\n')
            self.assertEqual(git('status', '--porcelain'), status)

    def test_bundle_resolves_catalog_to_all_original_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "bundle"
            plugin = builder.build(root)
            catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
            self.assertEqual((root / catalog["plugins"][0]["source"]["path"]).resolve(), plugin)
            self.assertEqual(json.loads((plugin / ".codex-plugin/plugin.json").read_text())["name"], plugin.name)
            files = list((plugin / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(files), 8)
            for file in files:
                self.assertEqual(file.read_bytes(), (builder.ROOT / file.relative_to(plugin)).read_bytes())
            source_files = {file.relative_to(builder.ROOT / 'skills')
                            for entrypoint in (builder.ROOT / 'skills').glob('*/SKILL.md')
                            for file in entrypoint.parent.rglob('*')
                            if file.is_file() and '__pycache__' not in file.parts and file.suffix != '.pyc'}
            bundled_files = {file.relative_to(plugin / 'skills') for file in
                             (plugin / 'skills').rglob('*') if file.is_file()}
            self.assertEqual(bundled_files, source_files)
            for relative in source_files:
                original, bundled = builder.ROOT / 'skills' / relative, plugin / 'skills' / relative
                self.assertEqual(original.read_bytes(), bundled.read_bytes())
                self.assertEqual(original.stat().st_mode & 0o777, bundled.stat().st_mode & 0o777)
            self.assertTrue((plugin / "LICENSE").is_file())
            for name in ('scripts/audit.py', 'references/python-audit.md'):
                relative = Path('skills/con-artist') / name
                self.assertEqual((plugin / relative).read_bytes(), (builder.ROOT / relative).read_bytes())
            for name in ('scripts/trace.py', 'references/focused-history.md'):
                relative = Path('skills/necromancer') / name
                self.assertEqual((plugin / relative).read_bytes(), (builder.ROOT / relative).read_bytes())
            with self.assertRaises(FileExistsError):
                builder.build(root)


if __name__ == "__main__":
    unittest.main()
