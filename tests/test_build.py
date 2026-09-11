import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("builder", Path(__file__).resolve().parents[1] / "scripts/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
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
