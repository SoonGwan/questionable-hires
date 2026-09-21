#!/usr/bin/env python3
"""Export reviewed synthetic-run evidence without private workspace paths."""

import argparse
import hashlib
import json
from pathlib import Path
import re


def redact_paths(text, workspace=None):
    if workspace is not None:
        text = text.replace(str(workspace), '<WORKSPACE>')
        text = text.replace('/private<WORKSPACE>', '<WORKSPACE>')
    text = text.replace(str(Path.home()), '<HOME>')
    # A home placeholder alone still exposes the local account directory UUID.
    # Keep unrelated run/test UUIDs intact; account placeholders are not identities.
    text = re.sub(r'(/codex-accounts/)[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}(?=/)',
                  r'\1<ACCOUNT>', text)
    # Keep JSON escapes and Markdown delimiters outside a redacted path. Also
    # handle malformed macOS links and the task-owned /tmp/qh-* scratch roots.
    return re.sub(r'''/(?:private/)?(?:var/(?:folders/|[a-z0-9]{2}/[A-Za-z0-9_-]+/T/)|tmp/qh-)[^\s"'<>\\)\]}]+''',
                  '<TEMP>', text)


def export(source, target, project_files=None):
    target.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((source / "run.json").read_text())
    (target / "run.json").write_text(redact_paths(json.dumps(manifest, indent=2)) + "\n")
    rows = []
    for cell in sorted(source.glob("*--*")):
        meta_path = cell / "metadata.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        workspace = Path(meta.pop("workspace", str(cell / "project")))
        snapshot = cell / "project"
        if not snapshot.exists():
            snapshot = workspace
        dest = target / cell.name
        dest.mkdir()
        def redact(text):
            return redact_paths(text, workspace)
        events_path = cell / "events.jsonl"
        event_text = events_path.read_text() if events_path.exists() else ""
        events = []
        for line in event_text.splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        (dest / "events.jsonl").write_text(redact(event_text))
        stderr = cell / "stderr.txt"
        (dest / "stderr.txt").write_text(redact(stderr.read_text()) if stderr.exists() else "")
        provenance = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in cell.iterdir() if p.is_file()}
        (dest / "source-sha256.json").write_text(json.dumps(provenance, indent=2) + "\n")
        commands = [e["item"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "command_execution"]
        # Keep source files that a reader can use to inspect the final behavior.
        project = dest / "project"
        project.mkdir()
        for file in snapshot.rglob("*"):
            relative = file.relative_to(snapshot)
            if project_files is not None and relative.as_posix() not in project_files:
                continue
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
        if project_files is not None:
            exported = sorted(str(file.relative_to(project)) for file in project.rglob('*') if file.is_file())
            (dest / 'project-export.json').write_text(json.dumps({
                'selection': sorted(set(project_files)), 'exported': exported,
                'missing': sorted(set(project_files) - set(exported)),
                'limitation': 'Selected source excerpts, not a complete project. Execution logs are not filtered.'
            }, indent=2) + '\n')
        answer_path = cell / "answer.md"
        answer = redact(answer_path.read_text()) if answer_path.exists() else ""
        def link(match):
            label, target = match.groups()
            if target == '<TEMP>':
                return label  # Masked location is not a usable source link.
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            source_path, separator, fragment = target.partition("#")
            location = re.fullmatch(r"(.+?):(\d+)", source_path)
            path, line = location.groups() if location else (source_path, None)
            if path.startswith("<WORKSPACE>/"):
                path = path[len("<WORKSPACE>/"):]
            if (project / path).is_file():
                suffix = f"#{fragment}" if separator else (f"#L{line}" if line else "")
                return f"[{label}](project/{path}{suffix})"
            return label if location else match.group(0)
        answer = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, answer)
        (dest / "answer.md").write_text(answer)
        diff_path = cell / "changes.diff"
        (dest / "changes.diff").write_text(redact(diff_path.read_text()) if diff_path.exists() else "")
        initial = cell / 'initial.diff'
        if initial.exists():
            (dest / 'initial.diff').write_text(redact(initial.read_text()))
        (dest / "commands.json").write_text(redact(json.dumps(commands, indent=2)) + "\n")
        meta = json.loads(redact(json.dumps(meta)))
        (dest / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        rows.append(meta)
    (target / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project-file", action="append", help="Only export these relative project files; logs remain complete")
    args = parser.parse_args()
    print(f"Exported {export(args.run, args.output, args.project_file)} cells. Review all artifacts before committing.")
