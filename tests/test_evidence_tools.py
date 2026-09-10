import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


exporter = load("exporter", "benchmarks/export.py")
auditor = load("auditor", "benchmarks/audit.py")


class EvidenceTests(unittest.TestCase):
    def test_export_preserves_evidence_and_resolves_source_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "app.py").write_text("answer = 42\n")
            (workspace / ".git").mkdir()
            (workspace / ".git/config").write_text("private git config")
            source = root / "run"
            cell = source / "case--skill--1"
            cell.mkdir(parents=True)
            (source / "run.json").write_text('{}')
            (cell / "metadata.json").write_text(json.dumps({"workspace": str(workspace), "completed": True}))
            (cell / "events.jsonl").write_text(json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": "pwd", "aggregated_output": str(workspace), "exit_code": 0}}) + '\n')
            (cell / "answer.md").write_text(f"See [code]({workspace}/app.py:1) and [angled](<{workspace}/app.py:1>).")
            (cell / "changes.diff").write_text("diff evidence\n")
            target = root / "export"
            self.assertEqual(exporter.export(source, target), 1)
            output = target / cell.name
            self.assertIn("[code](project/app.py#L1) and [angled](project/app.py#L1)", (output / "answer.md").read_text())
            self.assertNotIn(str(workspace), (output / "commands.json").read_text())
            self.assertNotIn("workspace", json.loads((output / "metadata.json").read_text()))
            self.assertFalse((output / "project/.git").exists())
            self.assertEqual((output / "changes.diff").read_text(), "diff evidence\n")
            with self.assertRaises(FileExistsError):
                exporter.export(source, target)

    def test_export_uses_retained_snapshot_and_preserves_failure_logs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "run"
            cell = source / "case--skill--1"
            (cell / "project").mkdir(parents=True)
            (cell / "project/app.py").write_text("snapshot = True\n")
            (source / "run.json").write_text('{}')
            (cell / "metadata.json").write_text(json.dumps({"workspace": str(root / "gone"), "completed": False}))
            (cell / "events.jsonl").write_text('{"type":"error","message":"rate limit"}\n')
            (cell / "stderr.txt").write_text(str(Path.home()) + '/private-path: timeout')
            (cell / "stdout.original.jsonl").write_text('private original')
            target = root / "export"
            exporter.export(source, target)
            dest = target / cell.name
            self.assertEqual((dest / "project/app.py").read_text(), "snapshot = True\n")
            self.assertIn("rate limit", (dest / "events.jsonl").read_text())
            self.assertNotIn(str(Path.home()), (dest / "stderr.txt").read_text())
            self.assertFalse((dest / "stdout.original.jsonl").exists())
            self.assertIn('stdout.original.jsonl', json.loads((dest / 'source-sha256.json').read_text()))
            self.assertEqual((cell / "stdout.original.jsonl").read_text(), 'private original')

    def test_audit_flags_added_files_on_read_only_review(self):
        case = next(c for c in json.loads((ROOT / "benchmarks/cases.json").read_text()) if c["id"] == "formatter-review")
        with tempfile.TemporaryDirectory() as directory:
            cell = Path(directory) / "formatter-review--baseline--1"
            project = cell / "project"
            project.mkdir(parents=True)
            for name, contents in case["files"].items():
                (project / name).write_text(contents)
            (project / "unrequested.md").write_text("extra")
            (cell / "metadata.json").write_text(json.dumps({"case": "formatter-review", "completed": True}))
            (cell / "commands.json").write_text('[]')
            self.assertEqual(auditor.audit(Path(directory))[0]["changes_requiring_scope_review"], ["unrequested.md"])

    def test_audit_flags_unrequested_source_edit(self):
        case = next(c for c in json.loads((ROOT / "benchmarks/cases.json").read_text()) if c["id"] == "label-change")
        with tempfile.TemporaryDirectory() as directory:
            cell = Path(directory) / "label-change--skill--1"
            project = cell / "project"
            project.mkdir(parents=True)
            for name, contents in case["files"].items():
                (project / name).write_text(contents)
            (project / "checkout.html").write_text(case["files"]["checkout.html"].replace(">Buy<", ">Place order<"))
            (project / "state.js").write_text("unrequested rewrite")
            (cell / "metadata.json").write_text(json.dumps({"case": "label-change", "completed": True}))
            (cell / "commands.json").write_text('[]')
            row = auditor.audit(Path(directory))[0]
            self.assertEqual(row["changes_requiring_scope_review"], ["state.js"])
            self.assertTrue(row["behavior_checks"][0]["passed"])


if __name__ == "__main__":
    unittest.main()
