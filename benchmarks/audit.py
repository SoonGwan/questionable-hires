#!/usr/bin/env python3
"""Audit execution and source preservation; semantic findings still need review."""

import argparse
import json
from pathlib import Path
import subprocess
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"boundary-fix": {"eligibility.py", "test_eligibility.py"}, "label-change": {"checkout.html"}, "necessary-state": {"form.py"}}


def audit(directory):
    cases = {}
    for name in ("cases.json", "clean-cases.json"):
        cases.update({c["id"]: c for c in json.loads((ROOT / "benchmarks" / name).read_text())})
    rows = []
    for cell in sorted(directory.glob("*--*")):
        meta = json.loads((cell / "metadata.json").read_text())
        case = cases[meta["case"]]
        changed = [name for name, original in case["files"].items()
                   if not (cell / "project" / name).exists() or (cell / "project" / name).read_text() != original]
        unexpected = sorted(set(changed) - ALLOWED.get(meta["case"], set()))
        present = {str(p.relative_to(cell / "project")) for p in (cell / "project").rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts}
        added = sorted(present - set(case["files"]))
        if meta["case"] in {"history-active", "formatter-review", "label-change", "rolling-schema"}:
            unexpected.extend(added)
        checks = []
        if meta["case"] in {"boundary-fix", "fix-present"}:
            code = "from eligibility import eligible; assert not eligible(17); assert eligible(18); assert eligible(19)"
            process = subprocess.run(["python3", "-B", "-c", code], cwd=cell / "project", text=True, capture_output=True, timeout=10)
            checks.append({"name": "eligibility boundaries 17/18/19", "passed": process.returncode == 0, "output": (process.stdout + process.stderr).replace(str(directory.resolve()), "<EVIDENCE>")})
        if meta["case"] == "boundary-fix":
            # Independent regression check: original tests against final code, then
            # final tests against the known faulty boundary in a disposable copy.
            with tempfile.TemporaryDirectory(prefix="qh-score-") as temp:
                work = Path(temp) / "project"
                shutil.copytree(cell / "project", work, ignore=shutil.ignore_patterns("__pycache__"))
                original_test = work / "test_original_behavior.py"
                original_test.write_text(case["files"]["test_eligibility.py"])
                result = subprocess.run(["python3", "-B", "-m", "unittest", "-v", "test_original_behavior"],
                                        cwd=work, capture_output=True, text=True, timeout=10)
                checks.append({"name": "original behavior regression", "passed": result.returncode == 0,
                               "output": (result.stdout + result.stderr).replace(temp, "<SCORING_TEMP>")})
                original_test.unlink()
                (work / "eligibility.py").write_text(case["files"]["eligibility.py"])
                result = subprocess.run(["python3", "-B", "-m", "unittest", "discover", "-v"],
                                        cwd=work, capture_output=True, text=True, timeout=10)
                checks.append({"name": "persisted tests reject original boundary", "passed": result.returncode != 0
                               and "FAIL:" in result.stderr and "eligible(18)" in result.stderr,
                               "output": (result.stdout + result.stderr).replace(temp, "<SCORING_TEMP>")})
        if meta["case"] == "label-change":
            expected = case["files"]["checkout.html"].replace(">Buy<", ">Place order<")
            checks.append({"name": "only requested label changes", "passed": (cell / "project/checkout.html").read_text() == expected})
        commands = json.loads((cell / "commands.json").read_text())
        rows.append({"cell": cell.name, "completed": meta["completed"], "changed_original_files": changed,
                     "changes_requiring_scope_review": sorted(set(unexpected)), "added_files": added, "behavior_checks": checks,
                     "executed_commands": len(commands), "nonzero_command_results": sum(c.get("exit_code") not in (None, 0) for c in commands),
                     "semantic_review": "required; nonzero results can be intentional reproductions"})
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.directory), indent=2))
