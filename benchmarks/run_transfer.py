#!/usr/bin/env python3
"""Execute the frozen Exorcist transfer plan; never resume or overwrite a run."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {"original": "be9d038", "candidate": "e2eb92b"}
ORDERS = (("baseline", "original", "candidate"),
          ("candidate", "baseline", "original"),
          ("original", "candidate", "baseline"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    snapshots = output / "snapshots"
    provenance = {}
    for condition, revision in VERSIONS.items():
        destination = snapshots / condition / "exorcist"
        destination.mkdir(parents=True)
        provenance[condition] = {"revision": revision, "files": {}}
        for name in ("SKILL.md", "agents/openai.yaml"):
            content = subprocess.check_output(["git", "show", f"{revision}:skills/exorcist/{name}"], cwd=ROOT)
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            provenance[condition]["files"][name] = hashlib.sha256(content).hexdigest()
    (output / "snapshots.json").write_text(json.dumps(provenance, indent=2) + "\n")
    records = []
    for block, order in enumerate(ORDERS, 1):
        for condition in order:
            run_output = output / f"block-{block}-{condition}"
            command = [sys.executable, str(ROOT / "benchmarks/run.py"),
                       "--output", str(run_output), "--cases-file", str(ROOT / "benchmarks/exorcist-transfer-cases.json"),
                       "--arms", "baseline" if condition == "baseline" else "skill",
                       "--jobs", "1", "--repeats", "1", "--timeout", "240",
                       "--model", "gpt-6-astra", "--effort", "medium", "--seed", str(20260911 + block)]
            if condition != "baseline":
                command.extend(["--skills-root", str(snapshots / condition)])
            print(f"Starting block {block}: {condition}", flush=True)
            result = subprocess.run(command, cwd=ROOT)
            manifest = run_output / "run.json"
            state = json.loads(manifest.read_text()) if manifest.exists() else {}
            records.append(dict(block=block, condition=condition, exit_code=result.returncode,
                                stopped_after_limit=state.get("stopped_after_limit")))
            (output / "blocks.json").write_text(json.dumps(records, indent=2) + "\n")
            if state.get("stopped_after_limit") or not state.get("finished_at"):
                raise SystemExit("Stopped: account limit or incomplete runner; no automatic restart.")
    raise SystemExit(1 if any(row["exit_code"] for row in records) else 0)


if __name__ == "__main__":
    main()
