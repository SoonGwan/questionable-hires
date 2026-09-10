#!/usr/bin/env python3
"""Audit execution and source preservation; semantic findings still need review."""

import argparse
import json
from pathlib import Path
import subprocess

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
        checks = []
        if meta["case"] in {"boundary-fix", "fix-present"}:
            code = "from eligibility import eligible; assert not eligible(17); assert eligible(18); assert eligible(19)"
            process = subprocess.run(["python3", "-B", "-c", code], cwd=cell / "project", text=True, capture_output=True, timeout=10)
            checks.append({"name": "eligibility boundaries 17/18/19", "passed": process.returncode == 0, "output": process.stdout + process.stderr})
        if meta["case"] == "label-change":
            expected = case["files"]["checkout.html"].replace(">Buy<", ">Place order<")
            checks.append({"name": "only requested label changes", "passed": (cell / "project/checkout.html").read_text() == expected})
        commands = json.loads((cell / "commands.json").read_text())
        rows.append({"cell": cell.name, "completed": meta["completed"], "changed_original_files": changed,
                     "changes_requiring_scope_review": unexpected, "behavior_checks": checks,
                     "executed_commands": len(commands), "nonzero_command_results": sum(c.get("exit_code") not in (None, 0) for c in commands),
                     "semantic_review": "required; nonzero results can be intentional reproductions"})
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.directory), indent=2))
