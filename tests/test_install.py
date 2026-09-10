import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dest = Path(self.temp.name) / "skills"

    def test_selected_skill_is_complete(self):
        installer.install(self.dest, ["necromancer"])
        source = installer.ROOT / "skills/necromancer"
        for file in source.rglob("*"):
            if file.is_file():
                self.assertEqual(file.read_bytes(), (self.dest / "necromancer" / file.relative_to(source)).read_bytes())
        self.assertEqual([p.name for p in self.dest.iterdir()], ["necromancer"])

    def test_conflict_prevents_partial_install(self):
        existing = self.dest / "receipt"
        existing.mkdir(parents=True)
        marker = existing / "mine"
        marker.write_text("user content")
        with self.assertRaises(ValueError):
            installer.install(self.dest, ["necromancer", "receipt"])
        self.assertFalse((self.dest / "necromancer").exists())
        self.assertEqual(marker.read_text(), "user content")

    def test_dry_run_does_not_create_destination(self):
        self.assertEqual(len(installer.install(self.dest, installer.available(), True)), 8)
        self.assertFalse(self.dest.exists())

    def test_unknown_name_cannot_escape_destination(self):
        with self.assertRaises(ValueError):
            installer.install(self.dest, ["../outside"])
        self.assertFalse(self.dest.exists())

    def test_copy_failure_rolls_back_only_new_targets(self):
        self.dest.mkdir()
        existing = self.dest / "unrelated"
        existing.mkdir()
        with patch.object(installer.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                installer.install(self.dest, ["receipt"])
        self.assertEqual(list(self.dest.iterdir()), [existing])

    def test_broken_symlink_is_not_overwritten(self):
        self.dest.mkdir()
        link = self.dest / "receipt"
        link.symlink_to(self.dest / "missing")
        with self.assertRaises(ValueError):
            installer.install(self.dest, ["receipt"])
        self.assertTrue(link.is_symlink())


if __name__ == "__main__":
    unittest.main()
