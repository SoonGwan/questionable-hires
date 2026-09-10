#!/usr/bin/env python3
"""Export reviewed synthetic-run evidence without private workspace paths."""

import argparse
import json
from pathlib import Path
import re


def export(source, target):
    target.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((source / "run.json").read_text())
    (target / "run.json").write_text(json.dumps(manifest, indent=2) + "\n")
    rows = []
    for cell in sorted(source.glob("*--*")):
        meta_path = cell / "metadata.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        workspace = Path(meta.pop("workspace"))
        dest = target / cell.name
        dest.mkdir()
        def redact(text):
            text = text.replace(str(workspace), "<WORKSPACE>")
            text = text.replace("/private<WORKSPACE>", "<WORKSPACE>")
            text = text.replace(str(Path.home()), "<HOME>")
            # Generated mutation directories sometimes use system temp locations.
            return re.sub(r"/(?:private/)?var/folders/[^\s\"'<>]+", "<TEMP>", text)
        events = [json.loads(line) for line in (cell / "events.jsonl").read_text().splitlines() if line.startswith("{")]
        commands = [e["item"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "command_execution"]
        # Keep source files that a reader can use to inspect the final behavior.
        project = dest / "project"
        for file in workspace.rglob("*"):
            relative = file.relative_to(workspace)
            if not file.is_file() or file.is_symlink() or any(part in {".git", ".agents", "__pycache__"} for part in relative.parts):
                continue
            if file.stat().st_size > 1_000_000:
                continue
            try:
                contents = file.read_text()
            except (UnicodeError, OSError):
                continue
            copy = project / relative
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_text(redact(contents))
        answer = redact((cell / "answer.md").read_text())
        def link(match):
            label, path, line = match.groups()
            if path.startswith("<WORKSPACE>/"):
                path = path[len("<WORKSPACE>/"):]
            if (project / path).is_file():
                return f"[{label}](project/{path}#L{line})"
            return label
        answer = re.sub(r"\[([^\]]+)\]\(([^)]+?):(\d+)\)", link, answer)
        def plain_link(match):
            label, path = match.groups()
            if path.startswith("<WORKSPACE>/"):
                path = path[len("<WORKSPACE>/"):]
            if (project / path).is_file():
                return f"[{label}](project/{path})"
            return match.group(0)
        answer = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", plain_link, answer)
        (dest / "answer.md").write_text(answer)
        (dest / "changes.diff").write_text(redact((cell / "changes.diff").read_text()))
        (dest / "commands.json").write_text(redact(json.dumps(commands, indent=2)) + "\n")
        (dest / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        rows.append(meta)
    (target / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(f"Exported {export(args.run, args.output)} cells. Review all artifacts before committing.")
