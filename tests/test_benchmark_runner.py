import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("runner", Path(__file__).resolve().parents[1] / "benchmarks/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class BenchmarkRunnerTests(unittest.TestCase):
    def test_fixture_paths_cannot_escape_workspace(self):
        for name in ("../escape.py", "/tmp/escape.py", ".git/config"):
            with tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / "project"
                with self.assertRaises(ValueError):
                    runner.prepare({"files": {name: "bad"}}, workspace)
                self.assertFalse(workspace.exists())

    def test_every_hire_has_a_neutral_task(self):
        cases = json.loads((runner.ROOT / "benchmarks/cases.json").read_text())
        actual = {c["skill"] for c in cases}
        expected = {p.parent.name for p in (runner.ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, expected)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))

    def test_history_preparation_is_identical_between_arms(self):
        case = json.loads((runner.ROOT / "benchmarks/cases.json").read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(runner.prepare(case, first), runner.prepare(case, second))
            for name, expected in case["files"].items():
                self.assertEqual((first / name).read_text(), expected)
            self.assertFalse((first / "criteria.json").exists())
            self.assertEqual(runner.command(["git", "rev-list", "--count", "HEAD"], first), "2")


if __name__ == "__main__":
    unittest.main()
